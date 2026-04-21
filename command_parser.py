"""Command parsing logic for VoxNav."""

from typing import Callable
from typing import Dict

from actions import ActionExecutor
from config import (
    DICTATION_START_COMMANDS,
    DICTATION_STOP_COMMANDS,
    FAST_MOUSE_STEP_PX,
    SLOW_MOUSE_STEP_PX,
    STOP_COMMANDS,
)
from state import AppState


class CommandParser:
    """Routes recognized speech to command or dictation actions."""

    def __init__(self, app_state: AppState, action_executor: ActionExecutor) -> None:
        self._app_state = app_state
        self._action_executor = action_executor

        self._command_handlers: Dict[str, Callable[[], None]] = {
            "click": self._action_executor.left_click,
            "double click": self._action_executor.double_click,
            "right click": self._action_executor.right_click,
            "scroll up": self._action_executor.scroll_up,
            "scroll down": self._action_executor.scroll_down,
            "new tab": lambda: self._action_executor.send_hotkey("ctrl+t"),
            "close tab": lambda: self._action_executor.send_hotkey("ctrl+w"),
            "switch tab": lambda: self._action_executor.send_hotkey("ctrl+tab"),
            "next tab": lambda: self._action_executor.send_hotkey("ctrl+tab"),
            "previous tab": lambda: self._action_executor.send_hotkey(
                "ctrl+shift+tab"
            ),
            "reopen tab": lambda: self._action_executor.send_hotkey(
                "ctrl+shift+t"
            ),
            "copy": lambda: self._action_executor.send_hotkey("ctrl+c"),
            "paste": lambda: self._action_executor.send_hotkey("ctrl+v"),
            "cut": lambda: self._action_executor.send_hotkey("ctrl+x"),
            "undo": lambda: self._action_executor.send_hotkey("ctrl+z"),
            "redo": lambda: self._action_executor.send_hotkey("ctrl+y"),
            "select all": lambda: self._action_executor.send_hotkey("ctrl+a"),
            "press enter": lambda: self._action_executor.send_hotkey("enter"),
            "enter": lambda: self._action_executor.send_hotkey("enter"),
            "press escape": lambda: self._action_executor.send_hotkey("esc"),
            "escape": lambda: self._action_executor.send_hotkey("esc"),
            "alt tab": lambda: self._action_executor.send_hotkey("alt+tab"),
            "minimize window": lambda: self._action_executor.send_hotkey("win+down"),
            "close window": lambda: self._action_executor.send_hotkey("alt+f4"),
            "mute": lambda: self._action_executor.send_hotkey("volume mute"),
            "volume up": lambda: self._action_executor.send_hotkey("volume up"),
            "volume down": lambda: self._action_executor.send_hotkey("volume down"),
            "pause music": lambda: self._action_executor.send_hotkey(
                "play/pause media"
            ),
            "play music": lambda: self._action_executor.send_hotkey(
                "play/pause media"
            ),
            "pause": lambda: self._action_executor.send_hotkey("play/pause media"),
            "play": lambda: self._action_executor.send_hotkey("play/pause media"),
            "next track": lambda: self._action_executor.send_hotkey("next track"),
            "previous track": lambda: self._action_executor.send_hotkey(
                "previous track"
            ),
            "faster": lambda: self._action_executor.set_mouse_speed("fast"),
            "slower": lambda: self._action_executor.set_mouse_speed("slow"),
            "normal speed": lambda: self._action_executor.set_mouse_speed("normal"),
        }

    def handle_transcript(self, transcript: str) -> None:
        """Handles recognized speech according to the current mode.

        Args:
            transcript: The normalized recognized speech text.
        """
        if not transcript:
            return

        if self._app_state.dictation_mode_enabled:
            self._handle_dictation_mode(transcript)
            return

        if transcript in DICTATION_START_COMMANDS:
            self.enable_dictation_mode()
            return

        if transcript in STOP_COMMANDS:
            self._action_executor.stop_continuous_movement()
            return

        if self._handle_exact_command(transcript):
            return

        if self._handle_mouse_command(transcript):
            return

        if self._handle_open_command(transcript):
            return

        print(f"No mapped command found for: {transcript}")

    def enable_dictation_mode(self) -> None:
        """Enables dictation mode."""
        self._app_state.dictation_mode_enabled = True
        print("Dictation mode enabled.")

    def disable_dictation_mode(self) -> None:
        """Disables dictation mode."""
        self._app_state.dictation_mode_enabled = False
        print("Dictation mode disabled.")

    def _handle_dictation_mode(self, transcript: str) -> None:
        """Handles speech while dictation mode is enabled.

        Args:
            transcript: The normalized recognized speech text.
        """
        if transcript in DICTATION_STOP_COMMANDS or transcript in STOP_COMMANDS:
            self.disable_dictation_mode()
            return

        if self._action_executor.handle_special_dictation_command(transcript):
            return

        self._action_executor.type_text(transcript)

    def _handle_exact_command(self, transcript: str) -> bool:
        """Handles exact command matches.

        Args:
            transcript: The normalized recognized speech text.

        Returns:
            True if the command was handled; otherwise False.
        """
        handler = self._command_handlers.get(transcript)
        if handler is None:
            return False

        handler()
        return True

    def _handle_mouse_command(self, transcript: str) -> bool:
        """Handles one-shot and continuous mouse commands.

        Args:
            transcript: The normalized recognized speech text.

        Returns:
            True if handled; otherwise False.
        """
        step_px = self._app_state.mouse_step_px

        if "slowly" in transcript or "a little" in transcript:
            step_px = SLOW_MOUSE_STEP_PX
        elif "faster" in transcript or "far" in transcript or "more" in transcript:
            step_px = FAST_MOUSE_STEP_PX

        one_shot_moves = {
            "up": (0, -step_px),
            "move up": (0, -step_px),
            "down": (0, step_px),
            "move down": (0, step_px),
            "left": (-step_px, 0),
            "move left": (-step_px, 0),
            "right": (step_px, 0),
            "move right": (step_px, 0),
        }

        move_vector = one_shot_moves.get(transcript)
        if move_vector is not None:
            dx, dy = move_vector
            self._action_executor.move_mouse(dx, dy)
            return True

        if transcript.startswith("hold "):
            direction = transcript.replace("hold ", "", 1).strip()
            if direction in {"up", "down", "left", "right"}:
                self._action_executor.start_continuous_movement(direction)
                return True

        return False

    def _handle_open_command(self, transcript: str) -> bool:
        """Handles app-launch commands.

        Args:
            transcript: The normalized recognized speech text.

        Returns:
            True if an app command was handled; otherwise False.
        """
        if not transcript.startswith("open "):
            return False

        app_name = transcript.replace("open ", "", 1).strip()
        return self._action_executor.launch_application(app_name)