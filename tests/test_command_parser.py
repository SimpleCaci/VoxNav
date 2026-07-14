import io
import unittest
from contextlib import redirect_stdout

import main
from command_parser import CommandParser
from config import FAST_MOUSE_STEP_PX
from state import AppState


class FakeExecutor:
    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        def record(*args):
            self.calls.append((name, *args))
        return record

    def handle_special_dictation_command(self, text):
        return False

    def launch_application(self, app_name):
        self.calls.append(("launch_application", app_name))
        return app_name == "notepad"


class CommandParserTests(unittest.TestCase):
    def make_parser(self):
        self.executor = FakeExecutor()
        self.events = []
        return CommandParser(
            AppState(),
            self.executor,
            event_sink=lambda stage, message: self.events.append((stage, message)),
        )

    def test_exact_command_reports_pipeline(self):
        parser = self.make_parser()

        parser.handle_transcript("  COPY  ")

        self.assertEqual(self.executor.calls, [("send_hotkey", "ctrl+c")])
        self.assertEqual(
            [stage for stage, _ in self.events],
            ["heard", "matched", "executed"],
        )
        self.assertEqual(self.events[0][1], "copy")

    def test_movement_modifier_uses_fast_step(self):
        parser = self.make_parser()

        parser.handle_transcript("move right faster")

        self.assertEqual(
            self.executor.calls,
            [("move_mouse", FAST_MOUSE_STEP_PX, 0)],
        )
        self.assertIn(
            ("executed", f"moved pointer by ({FAST_MOUSE_STEP_PX}, 0)"),
            self.events,
        )

    def test_unknown_application_is_explained(self):
        parser = self.make_parser()

        parser.handle_transcript("open mystery app")

        self.assertEqual(
            [stage for stage, _ in self.events],
            ["heard", "matched", "ignored"],
        )
        self.assertIn("allowlist", self.events[-1][1])


class PreviewModeTests(unittest.TestCase):
    def test_text_mode_runs_without_desktop_actions(self):
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main.main(["--text", "copy"])

        self.assertEqual(exit_code, 0)
        self.assertIn("safe command preview", output.getvalue())
        self.assertIn("HEARD", output.getvalue())
        self.assertIn("EXECUTED", output.getvalue())


if __name__ == "__main__":
    unittest.main()
