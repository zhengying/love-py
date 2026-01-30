# LOVE2D for Python

Python bindings for the LÖVE 2D game framework.

## Overview

This project provides Python bindings for the LÖVE 2D game engine, replacing Lua as the primary scripting language. It uses pybind11 for C++ bindings and SDL2/OpenGL for graphics.

## Project Structure

```
love2d_py/
├── love/                      # Python package
│   ├── __init__.py           # Main package with love.run()
│   ├── graphics.py           # Graphics module (love.graphics.*)
│   ├── window.py             # Window module (love.window.*)
│   ├── event.py              # Event module (love.event.*)
│   ├── timer.py              # Timer module (love.timer.*)
│   ├── keyboard.py           # Keyboard module (love.keyboard.*)
│   ├── mouse.py              # Mouse module (love.mouse.*)
│   ├── audio.py              # Audio module (love.audio.*)
│   ├── filesystem.py         # Filesystem module (love.filesystem.*)
│   └── callbacks.py          # Internal callback management
├── src/                       # C++ binding sources
│   ├── love2d_bindings.cpp   # Main module initialization
│   ├── graphics_module.cpp   # Graphics bindings
│   ├── window_module.cpp     # Window bindings
│   ├── event_module.cpp      # Event bindings
│   ├── timer_module.cpp      # Timer bindings
│   ├── keyboard_module.cpp   # Keyboard bindings
│   ├── mouse_module.cpp      # Mouse bindings
│   ├── audio_module.cpp      # Audio bindings
│   ├── filesystem_module.cpp # Filesystem bindings
│   └── callback_manager.cpp  # Game loop management
├── examples/                  # Example games
│   └── basic_game.py         # Simple example game
├── tests/                     # Test suite
├── CMakeLists.txt            # CMake configuration
├── setup.py                  # Python build script
└── pyproject.toml            # Project metadata
```

## Installation

### Prerequisites

- Python 3.8 or higher
- CMake 3.15 or higher
- C++17 compatible compiler
- SDL2 development libraries
- OpenGL development libraries

### macOS

```bash
# Install dependencies
brew install cmake sdl2 pybind11

# Build and install
pip install .
```

### Linux (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt-get install cmake libsdl2-dev libsdl2-mixer-dev \
    libgl1-mesa-dev python3-dev pybind11-dev

# Build and install
pip install .
```

### Windows

```bash
# Install dependencies (using vcpkg or manually)
# Then build:
pip install .
```

## Usage

```python
import love

def love.load():
    love.window.set_mode(800, 600)
    love.graphics.set_background_color(0.2, 0.2, 0.2)

def love.update(dt):
    if love.keyboard.is_down('escape'):
        love.event.quit()

def love.draw():
    love.graphics.set_color(1, 0, 0)
    love.graphics.rectangle('fill', 100, 100, 50, 50)

# Set callbacks and run
love.load = love.load
love.update = love.update
love.draw = love.draw
love.run()
```

## Development

### Building

```bash
# Development build (in-place)
python setup.py build_ext --inplace

# Using CMake directly
mkdir build
cd build
cmake ..
cmake --build . --parallel
```

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
black love/ examples/
flake8 love/ examples/
```

## API Reference

### Implemented Modules

- [x] `love.graphics` - Drawing primitives, colors, transformations
- [x] `love.window` - Window management
- [x] `love.event` - Event handling
- [x] `love.timer` - Time and FPS
- [x] `love.keyboard` - Keyboard input
- [x] `love.mouse` - Mouse input
- [x] `love.audio` - Audio playback (placeholder)
- [x] `love.filesystem` - File I/O

### Callbacks

- [x] `love.load()` - Game initialization
- [x] `love.update(dt)` - Game logic
- [x] `love.draw()` - Rendering
- [x] `love.quit()` - Cleanup
- [x] `love.keypressed(key, scancode, isrepeat)` - Key press
- [x] `love.keyreleased(key, scancode)` - Key release
- [x] `love.mousepressed(x, y, button, istouch, presses)` - Mouse press
- [x] `love.mousereleased(x, y, button, istouch, presses)` - Mouse release
- [x] `love.mousemoved(x, y, dx, dy, istouch)` - Mouse move

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.
