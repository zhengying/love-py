"""
LOVE2D Mouse Module

Handles mouse input.
"""

from love._love2d_core import mouse as _mouse
from love._love2d_core.mouse import (
    getPosition,
    getX,
    getY,
    setPosition,
    isDown,
    isVisible,
    setVisible,
    isGrabbed,
    setGrabbed,
)


def get_position() -> tuple[int, int]:
    """Get mouse position as (x, y)."""
    return getPosition()


def get_x() -> int:
    """Get mouse X position."""
    return getX()


def get_y() -> int:
    """Get mouse Y position."""
    return getY()


def set_position(x: int, y: int) -> None:
    """Set mouse position."""
    setPosition(x, y)


def is_down(*buttons: int) -> bool:
    """
    Check if mouse button(s) are pressed.
    
    Args:
        *buttons: Button numbers (1=left, 2=middle, 3=right, 4=x1, 5=x2)
        
    Returns:
        True if any button is pressed
    """
    return isDown(*buttons)


def is_visible() -> bool:
    """Check if cursor is visible."""
    return isVisible()


def set_visible(visible: bool) -> None:
    """Show or hide cursor."""
    setVisible(visible)


def is_grabbed() -> bool:
    """Check if cursor is grabbed."""
    return isGrabbed()


def set_grabbed(grabbed: bool) -> None:
    """Grab or release cursor."""
    setGrabbed(grabbed)


# Button constants
LEFT = 1
MIDDLE = 2
RIGHT = 3
X1 = 4
X2 = 5


__all__ = [
    "getPosition",
    "getX",
    "getY",
    "setPosition",
    "isDown",
    "isVisible",
    "setVisible",
    "isGrabbed",
    "setGrabbed",
    # Pythonic aliases
    "get_position",
    "get_x",
    "get_y",
    "set_position",
    "is_down",
    "is_visible",
    "set_visible",
    "is_grabbed",
    "set_grabbed",
    # Button constants
    "LEFT",
    "MIDDLE",
    "RIGHT",
    "X1",
    "X2",
]
