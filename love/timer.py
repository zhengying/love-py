"""
LOVE2D Timer Module

Provides time-related functions for game loops.
"""

from love._love2d_core import timer as _timer
from love._love2d_core.timer import (
    getTime,
    getDelta,
    getFPS,
    step,
    sleep,
)


def get_time() -> float:
    """Get time since application start in seconds."""
    return getTime()


def get_delta() -> float:
    """Get delta time (seconds since last frame)."""
    return getDelta()


def get_fps() -> int:
    """Get current FPS."""
    return getFPS()


def step_timer() -> float:
    """Advance the timer and get delta time."""
    return step()


def sleep_seconds(s: float) -> None:
    """Sleep for specified seconds."""
    sleep(s)


__all__ = [
    "getTime",
    "getDelta",
    "getFPS",
    "step",
    "sleep",
    # Pythonic aliases
    "get_time",
    "get_delta",
    "get_fps",
    "step_timer",
    "sleep_seconds",
]
