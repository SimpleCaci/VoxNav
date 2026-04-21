"""Desktop action execution helpers for VoxNav."""

import os
import subprocess
import threading
import time
from typing import Optional

import keyboard
import pyautogui

from config import (
    APP_COMMANDS,
    CONTINUOUS_MOVE_INTERVAL_SECONDS,
    CONTINUOUS_MOVE_STEP_PX,
    DEFAULT_MOUSE_STEP_PX,
    DEFAULT_TYPING_INTERVAL_SECONDS,
    FAST_MOUSE_STEP_PX,
    SLOW_MOUSE_STEP_PX,
    TYPE_TRAILING_SPACE,
)
from state import AppState


class ActionExecutor:
    """Executes mouse, keyboard, media, typing, and app-launch actions."""

    def __init__(self, app_state: AppState) -> None:
        self._app_state = app_state
        self._continuous_move_thread: Optional[threading.Thread] = None

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.02

    def left_click(self) -> None:
        """Performs a left mouse click."""
        pyautogui.click()

    def double_click(self) -> None:
        """Performs a double left mouse click."""
        pyautogui.doubleClick()

    def right_click(self) -> None:
        """Performs a right mouse click."""
        pyautogui.rightClick()

    def scroll_up(self) -> None:
        """Scrolls upward."""
        pyautogui.scroll(400)

    def scroll_down(self) -> None:
        """Scrolls downward."""
        pyautogui.scroll(-400)

    def move_mouse(self, dx: int, dy: int) -> None:
        """Moves the mouse relative to its current position.

        Args:
            dx: Horizontal movement in pixels.
            dy: Vertical movement in pixels.
        """
        pyautogui.moveRel(dx, dy, duration=0.05)

    def send_hotkey(self, hotkey: str) -> None:
        """Sends a keyboard hotkey combination.

        Args:
            hotkey: Keyboard hotkey string such as 'ctrl+t'.
        """
        keyboard.send(hotkey)

    def type_text(self, text: str) -> None:
        """Types text into the active window.

        Args:
            text: The text to type.
        """
        output_text = text
        if TYPE_TRAILING_SPACE:
            output_text += " "

        pyautogui.write(output_text, interval=DEFAULT_TYPING_INTERVAL_SECONDS)

    def handle_special_dictation_command(self, text: str) -> bool:
        """Handles editing and punctuation commands during dictation.

        Args:
            text: The recognized speech text.

        Returns:
            True if the command was handled; otherwise False.
        """
        special_commands = {
            "new line": lambda: keyboard.send("enter"),
            "new paragraph": lambda: (
                keyboard.send("enter"),
                keyboard.send("enter"),
            ),
            "comma": lambda: pyautogui.write(","),
            "period": lambda: pyautogui.write("."),
            "question mark": lambda: pyautogui.write("?"),
            "exclamation mark": lambda: pyautogui.write("!"),
            "colon": lambda: pyautogui.write(":"),
            "semicolon": lambda: pyautogui.write(";"),
            "quote": lambda: pyautogui.write('"'),
            "open quote": lambda: pyautogui.write('"'),
            "close quote": lambda: pyautogui.write('"'),
            "apostrophe": lambda: pyautogui.write("'"),
            "backspace": lambda: keyboard.send("backspace"),
            "delete word": lambda: keyboard.send("ctrl+backspace"),
            "select all": lambda: keyboard.send("ctrl+a"),
            "tab": lambda: keyboard.send("tab"),
        }

        action = special_commands.get(text)
        if action is None:
            return False

        action()
        return True

    def set_mouse_speed(self, speed_label: str) -> None:
        """Sets the mouse speed preset.

        Args:
            speed_label: One of 'slow', 'fast', or 'normal'.
        """
        if speed_label == "slow":
            self._app_state.mouse_step_px = SLOW_MOUSE_STEP_PX
        elif speed_label == "fast":
            self._app_state.mouse_step_px = FAST_MOUSE_STEP_PX
        else:
            self._app_state.mouse_step_px = DEFAULT_MOUSE_STEP_PX

        print(f"Mouse speed set to: {speed_label}")

    def start_continuous_movement(self, direction: str) -> None:
        """Starts continuously moving the mouse until stopped.

        Args:
            direction: One of 'up', 'down', 'left', or 'right'.
        """
        if self._app_state.continuous_move_enabled:
            self.stop_continuous_movement()

        self._app_state.continuous_move_direction = direction
        self._app_state.continuous_move_enabled = True

        self._continuous_move_thread = threading.Thread(
            target=self._continuous_move_loop,
            daemon=True,
        )
        self._continuous_move_thread.start()

        print(f"Started continuous movement: {direction}")

    def stop_continuous_movement(self) -> None:
        """Stops continuous mouse movement."""
        self._app_state.continuous_move_enabled = False
        self._app_state.continuous_move_direction = None

    def launch_application(self, app_name: str) -> bool:
        """Launches a configured application.

        Args:
            app_name: The spoken application name.

        Returns:
            True if launched successfully; otherwise False.
        """
        raw_command = APP_COMMANDS.get(app_name)
        if raw_command is None:
            return False

        expanded_command = os.path.expandvars(raw_command)

        try:
            subprocess.Popen(expanded_command, shell=True)
            print(f"Opened application: {app_name}")
            return True
        except Exception as error:
            print(f"Failed to open {app_name}: {error}")
            return False

    def _continuous_move_loop(self) -> None:
        """Continuously moves the mouse in the selected direction."""
        while self._app_state.continuous_move_enabled:
            direction = self._app_state.continuous_move_direction

            if direction == "up":
                self.move_mouse(0, -CONTINUOUS_MOVE_STEP_PX)
            elif direction == "down":
                self.move_mouse(0, CONTINUOUS_MOVE_STEP_PX)
            elif direction == "left":
                self.move_mouse(-CONTINUOUS_MOVE_STEP_PX, 0)
            elif direction == "right":
                self.move_mouse(CONTINUOUS_MOVE_STEP_PX, 0)

            time.sleep(CONTINUOUS_MOVE_INTERVAL_SECONDS)