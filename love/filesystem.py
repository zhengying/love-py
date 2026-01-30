"""
LOVE2D Filesystem Module

Handles file I/O operations.
"""

from love._love2d_core import filesystem as _filesystem
from love._love2d_core.filesystem import (
    read,
    write,
    exists,
    isFile,
    isDirectory,
    getDirectoryItems,
    createDirectory,
    getInfo,
    getSaveDirectory,
    getWorkingDirectory,
)

from typing import List, Optional


def read_file(filename: str, bytes: int = -1) -> str:
    """
    Read file contents.
    
    Args:
        filename: File to read
        bytes: Number of bytes to read (-1 for all)
        
    Returns:
        File contents as string
    """
    return read(filename, bytes)


def write_file(filename: str, data: str) -> int:
    """
    Write data to file.
    
    Args:
        filename: File to write
        data: Data to write
        
    Returns:
        Number of bytes written
    """
    return write(filename, data)


def file_exists(path: str) -> bool:
    """Check if path exists."""
    return exists(path)


def is_file(path: str) -> bool:
    """Check if path is a file."""
    return isFile(path)


def is_directory(path: str) -> bool:
    """Check if path is a directory."""
    return isDirectory(path)


def get_directory_items(dir: str) -> List[str]:
    """List directory contents."""
    return getDirectoryItems(dir)


def create_directory(name: str) -> bool:
    """Create a directory."""
    return createDirectory(name)


def get_file_info(path: str, filtertype: str = "") -> Optional[dict]:
    """Get file/directory information."""
    result = getInfo(path, filtertype)
    return result if result is not None else None


def get_save_directory() -> str:
    """Get the save directory path."""
    return getSaveDirectory()


def get_working_directory() -> str:
    """Get the working directory path."""
    return getWorkingDirectory()


# File mode constants
class FileMode:
    """File open modes."""
    READ = 'r'
    WRITE = 'w'
    APPEND = 'a'
    CLOSED = 'c'


class FileType:
    """File type constants."""
    FILE = 'file'
    DIRECTORY = 'directory'
    SYMLINK = 'symlink'
    OTHER = 'other'


__all__ = [
    "read",
    "write",
    "exists",
    "isFile",
    "isDirectory",
    "getDirectoryItems",
    "createDirectory",
    "getInfo",
    "getSaveDirectory",
    "getWorkingDirectory",
    # Pythonic aliases
    "read_file",
    "write_file",
    "file_exists",
    "is_file",
    "is_directory",
    "get_directory_items",
    "create_directory",
    "get_file_info",
    "get_save_directory",
    "get_working_directory",
    # Constants
    "FileMode",
    "FileType",
]
