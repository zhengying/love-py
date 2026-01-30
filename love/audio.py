"""
LOVE2D Audio Module

Handles audio playback.
"""

from love._love2d_core import audio as _audio
from love._love2d_core.audio import (
    newSource,
    play,
    stop,
    pause,
    resume,
    setVolume,
    getVolume,
    Source,
)

from typing import Optional


def new_source(filename: str, type: str = "static") -> Source:
    """
    Create a new audio source.
    
    Args:
        filename: Path to audio file
        type: Source type ('static', 'stream', or 'queue')
        
    Returns:
        New Source object
    """
    return newSource(filename, type)


def play_source(source: Source) -> None:
    """Play an audio source."""
    play(source)


def stop_source(source: Source) -> None:
    """Stop an audio source."""
    stop(source)


def pause_source(source: Source) -> None:
    """Pause an audio source."""
    pause(source)


def resume_source(source: Source) -> None:
    """Resume a paused audio source."""
    resume(source)


def set_volume(volume: float) -> None:
    """
    Set master volume.
    
    Args:
        volume: Volume level (0.0 to 1.0)
    """
    setVolume(volume)


def get_volume() -> float:
    """Get master volume."""
    return getVolume()


class SourceType:
    """Source type constants."""
    STATIC = "static"
    STREAM = "stream"
    QUEUE = "queue"


__all__ = [
    "newSource",
    "play",
    "stop",
    "pause",
    "resume",
    "setVolume",
    "getVolume",
    "Source",
    # Pythonic aliases
    "new_source",
    "play_source",
    "stop_source",
    "pause_source",
    "resume_source",
    "set_volume",
    "get_volume",
    # Constants
    "SourceType",
]
