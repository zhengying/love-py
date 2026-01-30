"""
LOVE2D Python - Game API Module

This module provides the graphics, window, and input functions
for LOVE2D games running under the C++ executable.

Usage (in game script):
    import love_py
    
    def love_draw():
        love_py.graphics.clear(0.2, 0.2, 0.2)
        love_py.graphics.set_color(1, 0, 0)
        love_py.graphics.rectangle('fill', 100, 100, 50, 50)
"""

# Import the core bindings
try:
    from . import _love2d_core
except ImportError:
    # Fallback for when imported directly (not as package)
    import _love2d_core

# Graphics module
graphics = _love2d_core.graphics

# Window module  
window = _love2d_core.window

# Event module
event = _love2d_core.event

# Timer module
timer = _love2d_core.timer

# Keyboard module
keyboard = _love2d_core.keyboard

# Mouse module
mouse = _love2d_core.mouse

# Audio module
audio = _love2d_core.audio

# Filesystem module
filesystem = _love2d_core.filesystem

__version__ = "11.5.0"

__all__ = [
    'graphics',
    'window', 
    'event',
    'timer',
    'keyboard',
    'mouse',
    'audio',
    'filesystem',
    '__version__',
]
