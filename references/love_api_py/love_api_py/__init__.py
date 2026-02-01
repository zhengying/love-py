"""
LOVE2D API for Python

This package provides a complete Python representation of the LÖVE game framework API.
All API information is stored in Python dataclasses for easy access and type safety.

Version: 11.5
"""

from .models import (
    LoveAPI,
    Module,
    Function,
    Type,
    Enum,
    EnumConstant,
    Variant,
    Argument,
    Return,
    Callback,
)
from .api_data import API

__version__ = "11.5"
__all__ = [
    "API",
    "LoveAPI", 
    "Module",
    "Function",
    "Type",
    "Enum",
    "EnumConstant",
    "Variant",
    "Argument",
    "Return",
    "Callback",
]
