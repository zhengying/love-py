"""
LOVE2D Graphics Module

Provides drawing functionality including shapes, images, text, and transformations.
"""

from love._love2d_core import graphics as _graphics

# Re-export all graphics functions
from love._love2d_core.graphics import (
    clear,
    present,
    setColor,
    getColor,
    setBackgroundColor,
    getBackgroundColor,
    rectangle,
    circle,
    line,
    push,
    pop,
    origin,
    translate,
    rotate,
    scale,
    getWidth,
    getHeight,
    getDimensions,
)

# Type aliases for better Python integration
DrawMode = str  # "fill" or "line"


def set_color(r: float, g: float, b: float, a: float = 1.0) -> None:
    """
    Set the drawing color.
    
    Args:
        r: Red component (0-1)
        g: Green component (0-1)
        b: Blue component (0-1)
        a: Alpha component (0-1, default 1.0)
    """
    setColor(r, g, b, a)


def get_color() -> tuple[float, float, float, float]:
    """Get the current drawing color as (r, g, b, a)."""
    return getColor()


def set_background_color(r: float, g: float, b: float, a: float = 1.0) -> None:
    """
    Set the background color.
    
    Args:
        r: Red component (0-1)
        g: Green component (0-1)
        b: Blue component (0-1)
        a: Alpha component (0-1, default 1.0)
    """
    setBackgroundColor(r, g, b, a)


def get_background_color() -> tuple[float, float, float, float]:
    """Get the background color as (r, g, b, a)."""
    return getBackgroundColor()


# Image class placeholder (to be implemented with actual image loading)
class Image:
    """Represents an image drawable."""
    
    def __init__(self, filename: str):
        """
        Load an image from file.
        
        Args:
            filename: Path to image file
        """
        self.filename = filename
        self._width = 0
        self._height = 0
        # TODO: Implement actual image loading
    
    def getWidth(self) -> int:
        """Get image width in pixels."""
        return self._width
    
    def getHeight(self) -> int:
        """Get image height in pixels."""
        return self._height
    
    def getDimensions(self) -> tuple[int, int]:
        """Get image dimensions as (width, height)."""
        return (self._width, self._height)


def new_image(filename: str) -> Image:
    """
    Create a new Image from a file.
    
    Args:
        filename: Path to image file
        
    Returns:
        New Image object
    """
    return Image(filename)


def draw(drawable, x: float = 0, y: float = 0, 
         r: float = 0, sx: float = 1, sy: float = 1,
         ox: float = 0, oy: float = 0, 
         kx: float = 0, ky: float = 0) -> None:
    """
    Draw a drawable object (Image, Canvas, etc.).
    
    Args:
        drawable: Object to draw
        x: X position
        y: Y position
        r: Rotation (radians)
        sx: X scale
        sy: Y scale
        ox: X origin offset
        oy: Y origin offset
        kx: X shear
        ky: Y shear
    """
    # TODO: Implement actual drawing with transformations
    pass


def print_text(text: str, x: float = 0, y: float = 0,
               r: float = 0, sx: float = 1, sy: float = 1,
               ox: float = 0, oy: float = 0) -> None:
    """
    Draw text on screen.
    
    Args:
        text: Text to draw
        x: X position
        y: Y position
        r: Rotation (radians)
        sx: X scale
        sy: Y scale
        ox: X origin offset
        oy: Y origin offset
    """
    # TODO: Implement text drawing
    pass


# Font class placeholder
class Font:
    """Represents a font for drawing text."""
    
    def __init__(self, filename: str, size: int = 12):
        self.filename = filename
        self.size = size


def new_font(filename: str, size: int = 12) -> Font:
    """Create a new Font."""
    return Font(filename, size)


def set_font(font: Font) -> None:
    """Set the active font for drawing text."""
    # TODO: Implement
    pass


def get_font() -> Font:
    """Get the active font."""
    # TODO: Implement
    return Font("", 12)


__all__ = [
    # Core functions
    "clear",
    "present",
    "setColor",
    "getColor",
    "setBackgroundColor",
    "getBackgroundColor",
    "rectangle",
    "circle",
    "line",
    "push",
    "pop",
    "origin",
    "translate",
    "rotate",
    "scale",
    "getWidth",
    "getHeight",
    "getDimensions",
    # Pythonic aliases
    "set_color",
    "get_color",
    "set_background_color",
    "get_background_color",
    # Classes
    "Image",
    "Font",
    # Object creation
    "new_image",
    "new_font",
    "draw",
    "print_text",
    "set_font",
    "get_font",
]
