"""
LOVE2D Window Module

Provides window management functionality.
"""

from love._love2d_core import window as _window
from love._love2d_core.window import (
    setMode,
    getMode,
    setFullscreen,
    getFullscreen,
    close,
    setTitle,
    getTitle,
    getWidth,
    getHeight,
    getDimensions,
    setVSync,
    getVSync,
    hasFocus,
    hasMouseFocus,
)

# Pythonic aliases


def set_mode(width: int, height: int, **flags) -> bool:
    """
    Set the window mode.
    
    Args:
        width: Window width in pixels
        height: Window height in pixels
        **flags: Optional flags (fullscreen, resizable, borderless, etc.)
        
    Returns:
        True if successful
    """
    return setMode(width, height, flags)


def get_mode() -> tuple[int, int, dict]:
    """
    Get the current window mode.
    
    Returns:
        Tuple of (width, height, flags)
    """
    return getMode()


def set_fullscreen(fullscreen: bool) -> None:
    """Toggle fullscreen mode."""
    setFullscreen(fullscreen)


def get_fullscreen() -> bool:
    """Check if window is in fullscreen mode."""
    return getFullscreen()


def set_title(title: str) -> None:
    """Set the window title."""
    setTitle(title)


def get_title() -> str:
    """Get the window title."""
    return getTitle()


def get_width() -> int:
    """Get window width."""
    return getWidth()


def get_height() -> int:
    """Get window height."""
    return getHeight()


def get_dimensions() -> tuple[int, int]:
    """Get window dimensions as (width, height)."""
    return getDimensions()


def set_vsync(vsync: int) -> None:
    """
    Set vertical sync.
    
    Args:
        vsync: 0 to disable, 1 to enable, -1 for adaptive
    """
    setVSync(vsync)


def get_vsync() -> int:
    """Get vertical sync state."""
    return getVSync()


def has_focus() -> bool:
    """Check if window has keyboard focus."""
    return hasFocus()


def has_mouse_focus() -> bool:
    """Check if window has mouse focus."""
    return hasMouseFocus()


__all__ = [
    "setMode",
    "getMode",
    "setFullscreen",
    "getFullscreen",
    "close",
    "setTitle",
    "getTitle",
    "getWidth",
    "getHeight",
    "getDimensions",
    "setVSync",
    "getVSync",
    "hasFocus",
    "hasMouseFocus",
    # Pythonic aliases
    "set_mode",
    "get_mode",
    "set_fullscreen",
    "get_fullscreen",
    "set_title",
    "get_title",
    "get_width",
    "get_height",
    "get_dimensions",
    "set_vsync",
    "get_vsync",
    "has_focus",
    "has_mouse_focus",
]
