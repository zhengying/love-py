"""
LOVE2D for Python - Main Package

This package provides Python bindings for the LÖVE 2D game framework.
It replaces Lua as the scripting language with Python.

Usage:
    import love
    
    def love.load():
        love.graphics.setBackgroundColor(0.2, 0.2, 0.2)
    
    def love.update(dt):
        pass
    
    def love.draw():
        love.graphics.rectangle('fill', 100, 100, 50, 50)
    
    love.run()
"""

__version__ = "11.5.0"
__author__ = "LOVE2D Python Community"

# Import all submodules for easy access
try:
    from . import graphics
    from . import window
    from . import event
    from . import timer
    from . import keyboard
    from . import mouse
    from . import audio
    from . import filesystem
    from . import callbacks as _callbacks
    from ._love2d_core import getVersion
except ImportError as e:
    raise ImportError(
        "LOVE2D C++ bindings not found. "
        "Please build the project with: python setup.py build_ext --inplace"
    ) from e

# Re-export for convenience
getVersion = getVersion

# Game loop management
load = None
update = None
draw = None
quit = None
keypressed = None
keyreleased = None
mousepressed = None
mousereleased = None
mousemoved = None


def conf(t):
    """
    Configuration callback. Override to configure the game.
    
    Args:
        t: Configuration table (use t.window.width, t.window.height, etc.)
    """
    pass


def run():
    """
    Run the game loop.
    
    This function initializes LOVE2D, calls the load callback,
    and enters the main game loop (update/draw).
    """
    # Initialize
    from ._love2d_core import init
    if not init():
        raise RuntimeError("Failed to initialize LOVE2D")
    
    # Set up callbacks
    if load:
        _callbacks.setLoad(load)
    if update:
        _callbacks.setUpdate(update)
    if draw:
        _callbacks.setDraw(draw)
    if quit:
        _callbacks.setQuit(quit)
    if keypressed:
        _callbacks.setKeyPressed(keypressed)
    if keyreleased:
        _callbacks.setKeyReleased(keyreleased)
    if mousepressed:
        _callbacks.setMousePressed(mousepressed)
    if mousereleased:
        _callbacks.setMouseReleased(mousereleased)
    if mousemoved:
        _callbacks.setMouseMoved(mousemoved)
    
    # Run game loop
    _callbacks.run()


def quit_game():
    """Queue a quit event to stop the game loop."""
    event.quit()


# Backwards compatibility aliases
quit = quit_game


__all__ = [
    "__version__",
    "getVersion",
    "graphics",
    "window",
    "event",
    "timer",
    "keyboard",
    "mouse",
    "audio",
    "filesystem",
    "load",
    "update",
    "draw",
    "quit",
    "keypressed",
    "keyreleased",
    "mousepressed",
    "mousereleased",
    "mousemoved",
    "conf",
    "run",
    "quit_game",
]
