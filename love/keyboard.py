"""
LOVE2D Keyboard Module

Handles keyboard input.
"""

from love._love2d_core import keyboard as _keyboard
from love._love2d_core.keyboard import (
    isDown,
    isScancodeDown,
    setKeyRepeat,
    hasKeyRepeat,
    setTextInput,
    hasTextInput,
    hasScreenKeyboard,
)


def is_down(*keys: str) -> bool:
    """
    Check if any of the specified keys are pressed.
    
    Args:
        *keys: Key names to check (e.g., 'a', 'space', 'return', 'escape')
        
    Returns:
        True if any key is pressed
    """
    return isDown(*keys)


def is_scancode_down(scancode: str) -> bool:
    """
    Check if a scancode is pressed.
    
    Args:
        scancode: Scancode name
        
    Returns:
        True if scancode is pressed
    """
    return isScancodeDown(scancode)


def set_key_repeat(enable: bool) -> None:
    """Enable or disable key repeat."""
    setKeyRepeat(enable)


def has_key_repeat() -> bool:
    """Check if key repeat is enabled."""
    return hasKeyRepeat()


def set_text_input(enable: bool) -> None:
    """Enable or disable text input events."""
    setTextInput(enable)


def has_text_input() -> bool:
    """Check if text input is active."""
    return hasTextInput()


def has_screen_keyboard() -> bool:
    """Check if screen keyboard is available."""
    return hasScreenKeyboard()


# Key constants for convenience
class KeyConstant:
    """Key code constants."""
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'
    F = 'f'
    G = 'g'
    H = 'h'
    I = 'i'
    J = 'j'
    K = 'k'
    L = 'l'
    M = 'm'
    N = 'n'
    O = 'o'
    P = 'p'
    Q = 'q'
    R = 'r'
    S = 's'
    T = 't'
    U = 'u'
    V = 'v'
    W = 'w'
    X = 'x'
    Y = 'y'
    Z = 'z'
    RETURN = 'return'
    ESCAPE = 'escape'
    SPACE = 'space'
    TAB = 'tab'
    BACKSPACE = 'backspace'
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    LSHIFT = 'lshift'
    RSHIFT = 'rshift'
    LCTRL = 'lctrl'
    RCTRL = 'rctrl'
    LALT = 'lalt'
    RALT = 'ralt'


__all__ = [
    "isDown",
    "isScancodeDown",
    "setKeyRepeat",
    "hasKeyRepeat",
    "setTextInput",
    "hasTextInput",
    "hasScreenKeyboard",
    # Pythonic aliases
    "is_down",
    "is_scancode_down",
    "set_key_repeat",
    "has_key_repeat",
    "set_text_input",
    "has_text_input",
    "has_screen_keyboard",
    # Constants class
    "KeyConstant",
]
