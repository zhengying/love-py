"""
LOVE2D Callbacks Module

Internal module for managing game loop callbacks.
This module is used internally by the love package.
"""

from love._love2d_core import callbacks as _callbacks
from love._love2d_core.callbacks import (
    setLoad,
    setUpdate,
    setDraw,
    setQuit,
    setKeyPressed,
    setKeyReleased,
    setMousePressed,
    setMouseReleased,
    setMouseMoved,
    run,
    stop,
)


__all__ = [
    "setLoad",
    "setUpdate",
    "setDraw",
    "setQuit",
    "setKeyPressed",
    "setKeyReleased",
    "setMousePressed",
    "setMouseReleased",
    "setMouseMoved",
    "run",
    "stop",
]
