"""Readable terminal trace output for the VoxNav command pipeline."""

from datetime import datetime


class ConsoleTrace:
    """Print heard, matched, and executed stages in a compact console timeline."""

    def __call__(self, stage: str, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {stage.upper():8} {message}")
