"""Application state models for VoxNav."""

from dataclasses import dataclass
from typing import Optional

from config import DEFAULT_MOUSE_STEP_PX


@dataclass
class AppState:
    """Stores all mutable runtime state for the application."""

    # Mode state
    dictation_mode_enabled: bool = False

    # Listening lock (prevents overlapping mic usage)
    is_listening: bool = False

    # Mouse control
    mouse_step_px: int = DEFAULT_MOUSE_STEP_PX

    # Continuous movement
    continuous_move_direction: Optional[str] = None
    continuous_move_enabled: bool = False

    # Internal flags
    should_exit: bool = False