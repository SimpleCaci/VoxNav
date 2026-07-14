"""Entry point for the VoxNav desktop assistant MVP."""

import argparse

from command_console import ConsoleTrace
from command_parser import CommandParser
from config import (
    HOTKEY_LISTEN_ONCE,
    HOTKEY_STOP_CURRENT_ACTION,
    HOTKEY_TOGGLE_DICTATION,
)
from preview_executor import PreviewExecutor
from state import AppState


class VoxNavApp:
    """Coordinate speech input, command parsing, and action execution."""

    def __init__(self) -> None:
        import keyboard

        from actions import ActionExecutor
        from speech_service import SpeechService

        self._keyboard = keyboard
        self._app_state = AppState()
        self._speech_service = SpeechService()
        self._action_executor = ActionExecutor(self._app_state)
        self._command_parser = CommandParser(
            self._app_state,
            self._action_executor,
            event_sink=ConsoleTrace(),
        )

    def run(self) -> None:
        """Start the application and block until exit."""
        print("Starting VoxNav command console...")
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

        self._keyboard.wait()

    def _register_hotkeys(self) -> None:
        self._keyboard.add_hotkey(HOTKEY_LISTEN_ONCE, self._listen_and_handle)
        self._keyboard.add_hotkey(
            HOTKEY_TOGGLE_DICTATION,
            self._toggle_dictation_mode,
        )
        self._keyboard.add_hotkey(
            HOTKEY_STOP_CURRENT_ACTION,
            self._stop_current_action,
        )

    def _listen_and_handle(self) -> None:
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
        if self._app_state.dictation_mode_enabled:
            self._command_parser.disable_dictation_mode()
        else:
            self._command_parser.enable_dictation_mode()

    def _stop_current_action(self) -> None:
        self._action_executor.stop_continuous_movement()
        self._command_parser.disable_dictation_mode()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Control Windows by voice or safely preview command parsing."
    )
    parser.add_argument(
        "--text",
        action="append",
        metavar="COMMAND",
        help=(
            "Preview a command without controlling the desktop. "
            "Repeat the option to trace a sequence."
        ),
    )
    return parser


def run_preview(commands: list[str]) -> None:
    """Trace commands through the real parser with a no-side-effect executor."""
    print("VoxNav safe command preview — no desktop actions will run.")
    parser = CommandParser(
        AppState(),
        PreviewExecutor(),
        event_sink=ConsoleTrace(),
    )
    for command in commands:
        parser.handle_transcript(command)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.text:
        run_preview(args.text)
        return 0

    VoxNavApp().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
