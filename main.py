"""Entry point for the VoxNav desktop assistant MVP."""

import keyboard

from actions import ActionExecutor
from command_parser import CommandParser
from config import (
    HOTKEY_LISTEN_ONCE,
    HOTKEY_STOP_CURRENT_ACTION,
    HOTKEY_TOGGLE_DICTATION,
)
from speech_service import SpeechService
from state import AppState


class VoxNavApp:
    """Coordinates speech input, command parsing, and action execution."""

    def __init__(self) -> None:
        self._app_state = AppState()
        self._speech_service = SpeechService()
        self._action_executor = ActionExecutor(self._app_state)
        self._command_parser = CommandParser(
            self._app_state,
            self._action_executor,
        )

    def run(self) -> None:
        """Starts the application and blocks until exit."""
        print("Starting VoxNav...")
        self._speech_service.calibrate_microphone()
        self._register_hotkeys()

        print(f"Press {HOTKEY_LISTEN_ONCE.upper()} to listen once.")
        print(
            f"Press {HOTKEY_TOGGLE_DICTATION.upper()} to toggle dictation mode "
            "manually."
        )
        print(
            f"Press {HOTKEY_STOP_CURRENT_ACTION.upper()} to stop continuous "
            "movement or exit dictation mode."
        )
        print("Press CTRL+C in the terminal to exit.")

        keyboard.wait()

    def _register_hotkeys(self) -> None:
        """Registers global hotkeys for app control."""
        keyboard.add_hotkey(HOTKEY_LISTEN_ONCE, self._listen_and_handle)
        keyboard.add_hotkey(HOTKEY_TOGGLE_DICTATION, self._toggle_dictation_mode)
        keyboard.add_hotkey(HOTKEY_STOP_CURRENT_ACTION, self._stop_current_action)

    def _listen_and_handle(self) -> None:
        """Listens for one phrase and routes it to the parser."""
        if self._app_state.is_listening:
            return

        self._app_state.is_listening = True
        try:
            transcript = self._speech_service.listen_once()
            if transcript is not None:
                self._command_parser.handle_transcript(transcript)
        finally:
            self._app_state.is_listening = False

    def _toggle_dictation_mode(self) -> None:
        """Toggles dictation mode on or off."""
        if self._app_state.dictation_mode_enabled:
            self._command_parser.disable_dictation_mode()
        else:
            self._command_parser.enable_dictation_mode()

    def _stop_current_action(self) -> None:
        """Stops continuous movement and disables dictation mode."""
        self._action_executor.stop_continuous_movement()
        self._command_parser.disable_dictation_mode()


def main() -> None:
    """Application entry point."""
    app = VoxNavApp()
    app.run()


if __name__ == "__main__":
    main()