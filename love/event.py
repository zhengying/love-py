"""
LOVE2D Event Module

Handles OS events like keyboard input, mouse movement, and window events.
"""

from love._love2d_core import event as _event
from love._love2d_core.event import (
    pump,
    poll,
    quit,
    push,
    clear,
)

from typing import Optional


def poll_event() -> Optional[dict]:
    """
    Get the next event from the queue.
    
    Returns:
        Event dictionary or None if no events
    """
    result = poll()
    if result is None:
        return None
    return dict(result)


__all__ = [
    "pump",
    "poll",
    "quit",
    "push",
    "clear",
    "poll_event",
]
