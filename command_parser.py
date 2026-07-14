"""Command parsing logic for VoxNav."""

from collections.abc import Callable
from typing import Any

from config import (
    DICTATION_START_COMMANDS,
    DICTATION_STOP_COMMANDS,
    FAST_MOUSE_STEP_PX,
    SLOW_MOUSE_STEP_PX,
    STOP_COMMANDS,
)
from state import AppState

EventSink = Callable[[str, str], None]


class CommandParser:
    """Route normalized transcripts and report each decision stage."""

    def __init__(
        self,
        app_state: AppState,
        action_executor: Any,
        event_sink: EventSink | None = None,
    ) -> None:
        self._app_state = app_state
        self._action_executor = action_executor
        self._event_sink = event_sink or (lambda stage, message: None)

        self._command_handlers: dict[str, Callable[[], None]] = {
            "click": self._action_executor.left_click,
            "double click": self._action_executor.double_click,
            "right click": self._action_executor.right_click,
            "scroll up": self._action_executor.scroll_up,
            "scroll down": self._action_executor.scroll_down,
            "new tab": lambda: self._action_executor.send_hotkey("ctrl+t"),
            "close tab": lambda: self._action_executor.send_hotkey("ctrl+w"),
            "switch tab": lambda: self._action_executor.send_hotkey("ctrl+tab"),
            "next tab": lambda: self._action_executor.send_hotkey("ctrl+tab"),
            "previous tab": lambda: self._action_executor.send_hotkey("ctrl+shift+tab"),
            "reopen tab": lambda: self._action_executor.send_hotkey("ctrl+shift+t"),
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
            "pause music": lambda: self._action_executor.send_hotkey("play/pause media"),
            "play music": lambda: self._action_executor.send_hotkey("play/pause media"),
            "pause": lambda: self._action_executor.send_hotkey("play/pause media"),
            "play": lambda: self._action_executor.send_hotkey("play/pause media"),
            "next track": lambda: self._action_executor.send_hotkey("next track"),
            "previous track": lambda: self._action_executor.send_hotkey("previous track"),
            "faster": lambda: self._action_executor.set_mouse_speed("fast"),
            "slower": lambda: self._action_executor.set_mouse_speed("slow"),
            "normal speed": lambda: self._action_executor.set_mouse_speed("normal"),
        }

    def _emit(self, stage: str, message: str) -> None:
        self._event_sink(stage, message)

    def handle_transcript(self, transcript: str) -> None:
        """Handle recognized speech according to the current mode."""
        transcript = " ".join(transcript.strip().lower().split())
        if not transcript:
            return

        self._emit("heard", transcript)

        if self._app_state.dictation_mode_enabled:
            self._handle_dictation_mode(transcript)
            return

        if transcript in DICTATION_START_COMMANDS:
            self._emit("matched", "dictation mode")
            self.enable_dictation_mode()
            return

        if transcript in STOP_COMMANDS:
            self._emit("matched", "emergency stop")
            self._action_executor.stop_continuous_movement()
            self._emit("executed", "continuous movement stopped")
            return

        if self._handle_exact_command(transcript):
            return

        if self._handle_mouse_command(transcript):
            return

        if self._handle_open_command(transcript):
            return

        self._emit("ignored", f'no mapped command for "{transcript}"')

    def enable_dictation_mode(self) -> None:
        self._app_state.dictation_mode_enabled = True
        self._emit("executed", "dictation mode enabled")

    def disable_dictation_mode(self) -> None:
        self._app_state.dictation_mode_enabled = False
        self._emit("executed", "dictation mode disabled")

    def _handle_dictation_mode(self, transcript: str) -> None:
        if transcript in DICTATION_STOP_COMMANDS or transcript in STOP_COMMANDS:
            self._emit("matched", "leave dictation mode")
            self.disable_dictation_mode()
            return

        if self._action_executor.handle_special_dictation_command(transcript):
            self._emit("matched", f"dictation control: {transcript}")
            self._emit("executed", f"dictation control: {transcript}")
            return

        self._emit("matched", "dictation text")
        self._action_executor.type_text(transcript)
        self._emit("executed", f"typed {len(transcript)} characters")

    def _handle_exact_command(self, transcript: str) -> bool:
        handler = self._command_handlers.get(transcript)
        if handler is None:
            return False

        self._emit("matched", f"exact command: {transcript}")
        handler()
        self._emit("executed", transcript)
        return True

    def _handle_mouse_command(self, transcript: str) -> bool:
        step_px = self._app_state.mouse_step_px
        command = transcript

        if "slowly" in transcript or "a little" in transcript:
            step_px = SLOW_MOUSE_STEP_PX
        elif "faster" in transcript or "far" in transcript or "more" in transcript:
            step_px = FAST_MOUSE_STEP_PX

        for modifier in (" slowly", " a little", " faster", " far", " more"):
            command = command.replace(modifier, "")
        command = command.strip()

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

        move_vector = one_shot_moves.get(command)
        if move_vector is not None:
            dx, dy = move_vector
            self._emit("matched", f"pointer movement: {command}")
            self._action_executor.move_mouse(dx, dy)
            self._emit("executed", f"moved pointer by ({dx}, {dy})")
            return True

        if command.startswith("hold "):
            direction = command.replace("hold ", "", 1).strip()
            if direction in {"up", "down", "left", "right"}:
                self._emit("matched", f"continuous pointer movement: {direction}")
                self._action_executor.start_continuous_movement(direction)
                self._emit("executed", f"holding pointer {direction}")
                return True

        return False

    def _handle_open_command(self, transcript: str) -> bool:
        if not transcript.startswith("open "):
            return False

        app_name = transcript.replace("open ", "", 1).strip()
        self._emit("matched", f"application launch: {app_name}")
        if self._action_executor.launch_application(app_name):
            self._emit("executed", f"opened {app_name}")
        else:
            self._emit("ignored", f'"{app_name}" is not in the application allowlist')
        return True
