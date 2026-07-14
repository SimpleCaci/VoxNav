"""A no-side-effect action executor for command previews."""

from typing import Any


class PreviewExecutor:
    """Record actions without controlling the real keyboard or pointer."""

    def __init__(self) -> None:
        self.actions: list[str] = []

    def __getattr__(self, name: str):
        def record(*args: Any) -> None:
            rendered = ", ".join(repr(value) for value in args)
            self.actions.append(f"{name}({rendered})")
        return record

    def handle_special_dictation_command(self, text: str) -> bool:
        controls = {
            "new line",
            "new paragraph",
            "comma",
            "period",
            "question mark",
            "exclamation mark",
            "colon",
            "semicolon",
            "quote",
            "open quote",
            "close quote",
            "apostrophe",
            "backspace",
            "delete word",
            "select all",
            "tab",
        }
        if text not in controls:
            return False
        self.actions.append(f"dictation_control({text!r})")
        return True

    def launch_application(self, app_name: str) -> bool:
        self.actions.append(f"launch_application({app_name!r})")
        return app_name in {"chrome", "notepad", "calculator"}
