"""Configuration values for the VoxNav application."""

from pathlib import Path

# Audio / speech settings.
LISTEN_TIMEOUT_SECONDS = 4
PHRASE_TIME_LIMIT_SECONDS = 6
AMBIENT_NOISE_ADJUST_SECONDS = 1

# Mouse movement settings.
DEFAULT_MOUSE_STEP_PX = 50
FAST_MOUSE_STEP_PX = 120
SLOW_MOUSE_STEP_PX = 20

CONTINUOUS_MOVE_INTERVAL_SECONDS = 0.04
CONTINUOUS_MOVE_STEP_PX = 12

# Typing / dictation settings.
DEFAULT_TYPING_INTERVAL_SECONDS = 0.01
TYPE_TRAILING_SPACE = True

# Global hotkeys.
HOTKEY_LISTEN_ONCE = "f8"
HOTKEY_TOGGLE_DICTATION = "f9"
HOTKEY_STOP_CURRENT_ACTION = "esc"

# Command words.
DICTATION_START_COMMANDS = {
    "dictate",
    "start dictation",
    "enter dictation mode",
}

DICTATION_STOP_COMMANDS = {
    "stop dictation",
    "exit dictation mode",
    "leave dictation mode",
}

STOP_COMMANDS = {
    "stop",
    "cancel",
    "halt",
}

# Mouse direction vocabulary.
DIRECTION_KEYWORDS = {
    "up",
    "down",
    "left",
    "right",
}

# Special dictation phrases.
DICTATION_SPECIAL_COMMANDS = {
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

# Supported application launch paths / commands.
APP_COMMANDS = {
    "chrome": (r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",),
    "spotify": (r"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe",),
    "discord": (
        r"C:\\Users\\%USERNAME%\\AppData\\Local\\Discord\\Update.exe",
        "--processStart",
        "Discord.exe",
    ),
    "notepad": ("notepad.exe",),
    "calculator": ("calc.exe",),
    "explorer": ("explorer.exe",),
    "file explorer": ("explorer.exe",),
    "paint": ("mspaint.exe",),
}

# Optional project paths.
PROJECT_ROOT = Path(__file__).resolve().parent