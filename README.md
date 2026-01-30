# LOVE2D Python

Python bindings for the LÖVE 2D game framework - use Python instead of Lua for game development!

## Architecture

This project follows the same architecture as the original LÖVE2D:

```
┌─────────────────────────────────────────────────────────────┐
│                    C++ Executable (love)                     │
│                    38KB Mach-O 64-bit                        │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  src/love.cpp - Main Entry Point                       │  │
│  │  • Runs SDL2 main loop                                 │  │
│  │  • Handles events (keyboard, mouse, quit)              │  │
│  │  • Manages OpenGL context                              │  │
│  │  • Calls Python callbacks                              │  │
│  └───────────────────────────────────────────────────────┘  │
│                         ↓                                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Python C-API Integration                              │  │
│  │  • Py_Initialize()                                     │  │
│  │  • PyRun_SimpleFile() - Loads game.py                  │  │
│  │  • PyObject_CallObject() - Invokes callbacks           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                Python Game Script (game.py)                  │
│                                                              │
│  def love_load():      # Called once at startup             │
│  def love_update(dt):  # Called every frame                 │
│  def love_draw():      # Called every frame                 │
│  def love_quit():      # Called on exit                     │
│  def love_keypressed(key, scancode, isrepeat)               │
│  def love_mousepressed(x, y, button, istouch, presses)      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│           C++ Extension Module (_love2d_core.so)             │
│              Built via pybind11 + CMake                      │
│                                                              │
│  • love2d_bindings.cpp - Module initialization              │
│  • graphics_module.cpp - OpenGL rendering                   │
│  • window_module.cpp - SDL2 window management               │
│  • event_module.cpp - SDL2 event queue                      │
│  • timer_module.cpp - SDL2 timing                           │
│  • keyboard_module.cpp - SDL2 keyboard                      │
│  • mouse_module.cpp - SDL2 mouse                            │
│  • image_module.cpp - stb_image + OpenGL textures           │
│  • audio_module.cpp - Placeholder                           │
│  • filesystem_module.cpp - C++17 filesystem                 │
└─────────────────────────────────────────────────────────────┘
```

**Key Design Decision:** C++ owns the main loop (not Python), matching the original LÖVE2D design for proper frame timing.

## Build Instructions

### Prerequisites

- Python 3.8+
- CMake 3.15+
- SDL2 development libraries
- OpenGL development libraries
- C++17 compatible compiler

### macOS

```bash
# Install dependencies
brew install cmake python sdl2

# Clone and build
cd love2d_py

# Option 1: Using pip (recommended)
pip install .

# Option 2: Using CMake directly
mkdir -p build && cd build
cmake ..
make -j4

# The executable will be at bin/love
# The Python extension will be at love/_love2d_core.so
```

### Linux (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y cmake python3 python3-dev python3-pip libsdl2-dev libgl1-mesa-dev

# Clone and build
cd love2d_py

# Option 1: Using pip (recommended)
pip3 install .

# Option 2: Using CMake directly
mkdir -p build && cd build
cmake ..
make -j4
```

### Windows

```powershell
# Install dependencies (using vcpkg or manually)
# - CMake
# - Python 3.8+
# - SDL2 development libraries
# - Visual Studio 2019 or newer

# Clone and build
cd love2d_py

# Using pip
pip install .

# Or using CMake directly
mkdir build
cd build
cmake .. -A x64
cmake --build . --config Release
```

## Quick Start

### Running Examples

```bash
# Visual rendering test
./bin/love examples/visual_test.py

# Interactive game with keyboard/mouse
./bin/love examples/interactive_game.py

# Transformations demo
./bin/love examples/transformations_test.py
```

### Creating a Game

Create `my_game.py`:

```python
import love
import random

circles = []

def love_load():
    """Called once at startup"""
    love.window.set_title("My Awesome Game")
    love.graphics.set_background_color(0.1, 0.1, 0.2)

def love_update(dt):
    """Called every frame with delta time"""
    # Spawn random circles
    if random.random() < 0.02:
        circles.append({
            'x': random.randint(50, 750),
            'y': random.randint(50, 550),
            'r': random.randint(10, 30),
            'color': (random.random(), random.random(), random.random())
        })

def love_draw():
    """Called every frame to render"""
    love.graphics.clear()
    
    for circle in circles:
        love.graphics.set_color(*circle['color'])
        love.graphics.circle('fill', circle['x'], circle['y'], circle['r'])

def love_mousepressed(x, y, button, istouch, presses):
    """Called when mouse is pressed"""
    circles.append({
        'x': x, 'y': y,
        'r': random.randint(20, 50),
        'color': (1, 1, 1)
    })

def love_keypressed(key, scancode, isrepeat):
    """Called when key is pressed"""
    if key == 'escape':
        love.event.quit()
```

Run it:
```bash
./bin/love my_game.py
```

## Project Structure

```
love2d_py/
├── love/                      # Python module
│   ├── __init__.py           # Main love module
│   └── _love2d_core.so       # C++ extension (built)
├── bin/
│   └── love                  # C++ executable (built)
├── src/                      # C++ source files
│   ├── love.cpp              # Main C++ executable entry point
│   ├── love2d_bindings.cpp   # pybind11 Python extension module
│   ├── love2d_common.h       # Shared state structure
│   ├── graphics_module.cpp   # Graphics API (OpenGL)
│   ├── window_module.cpp     # Window management (SDL2)
│   ├── event_module.cpp      # Event handling (SDL2)
│   ├── timer_module.cpp      # Timer/FPS functions
│   ├── keyboard_module.cpp   # Keyboard input
│   ├── mouse_module.cpp      # Mouse input
│   ├── audio_module.cpp      # Audio (placeholder)
│   ├── filesystem_module.cpp # Filesystem (C++17)
│   ├── image_module.cpp      # Image loading (stb_image + OpenGL)
│   ├── callback_manager.cpp  # Game loop callback management
│   └── stb_image.h           # STB image loading library
├── examples/                 # Example games
│   ├── visual_test.py        # Basic rendering test
│   ├── interactive_game.py   # Input handling demo
│   └── transformations_test.py # Graphics transformations
├── setup.py                  # Python setuptools with CMake
├── CMakeLists.txt            # CMake build configuration
├── ARCHITECTURE.md           # Detailed architecture documentation
├── API_IMPLEMENTATION_PLAN.md # API tracking (L1-L5)
└── WORKING.md                # Current status and working features
```

## What's Implemented

### ✅ Core Features (L1 - Critical)

**Game Loop:**
- `love.load()` - Game initialization callback
- `love.update(dt)` - Update game state
- `love.draw()` - Render game
- `love.quit()` - Handle game quit
- `love.keypressed()` - Key press callback
- `love.mousepressed()` - Mouse press callback

**Graphics:**
- `love.graphics.clear(r, g, b, a)` - Clear screen
- `love.graphics.setColor(r, g, b, a)` - Set drawing color
- `love.graphics.getColor()` - Get current color
- `love.graphics.setBackgroundColor(r, g, b, a)` - Set background
- `love.graphics.getBackgroundColor()` - Get background
- `love.graphics.rectangle(mode, x, y, w, h)` - Draw rectangle
- `love.graphics.circle(mode, x, y, radius)` - Draw circle
- `love.graphics.line(x1, y1, x2, y2)` - Draw line
- `love.graphics.push()` / `pop()` - Transform stack
- `love.graphics.origin()` - Reset transform
- `love.graphics.translate(dx, dy)` - Translate
- `love.graphics.rotate(angle)` - Rotate
- `love.graphics.scale(sx, sy)` - Scale
- `love.graphics.present()` - Swap buffers

**Window:**
- `love.window.setMode(w, h, flags)` - Create window
- `love.window.getMode()` - Get window settings
- `love.window.setTitle(title)` - Set title
- `love.window.getTitle()` - Get title
- `love.window.close()` - Close window
- `love.window.setFullscreen(bool)` - Toggle fullscreen
- `love.window.getFullscreen()` - Get fullscreen state
- `love.window.setVSync(vsync)` - Set vsync
- `love.window.getVSync()` - Get vsync state
- `love.window.hasFocus()` - Check keyboard focus
- `love.window.hasMouseFocus()` - Check mouse focus

**Timer:**
- `love.timer.getTime()` - Get elapsed time
- `love.timer.getDelta()` - Get delta time
- `love.timer.getFPS()` - Get current FPS
- `love.timer.step()` - Update delta time
- `love.timer.sleep(seconds)` - Sleep

**Keyboard:**
- `love.keyboard.isDown(key, ...)` - Check key press (varargs)
- `love.keyboard.isScancodeDown(scancode)` - Check scancode
- `love.keyboard.setTextInput(enable)` - Start/stop text input
- `love.keyboard.hasTextInput()` - Check text input state

**Mouse:**
- `love.mouse.getPosition()` - Get mouse position
- `love.mouse.getX()` / `getY()` - Individual coordinates
- `love.mouse.setPosition(x, y)` - Set position
- `love.mouse.isDown(button, ...)` - Check button press
- `love.mouse.isVisible()` - Check visibility
- `love.mouse.setVisible(bool)` - Set visibility
- `love.mouse.isGrabbed()` - Check grab state
- `love.mouse.setGrabbed(bool)` - Set grab state

**Event:**
- `love.event.pump()` - Poll for events
- `love.event.poll()` - Get next event
- `love.event.quit()` - Queue quit
- `love.event.push()` - Push custom event
- `love.event.clear()` - Clear events

**Filesystem:**
- `love.filesystem.read(filename, bytes)` - Read file
- `love.filesystem.write(filename, data)` - Write file
- `love.filesystem.exists(path)` - Check existence
- `love.filesystem.isFile(path)` - Check if file
- `love.filesystem.isDirectory(path)` - Check if directory
- `love.filesystem.getDirectoryItems(dir)` - List directory
- `love.filesystem.createDirectory(name)` - Create directory
- `love.filesystem.getInfo(path)` - Get file info
- `love.filesystem.getWorkingDirectory()` - Get working dir

**Image:**
- `love.image.newImage(filename)` - Load image
- `Image:getWidth()` / `getHeight()` - Get dimensions
- `love.image.draw(image, x, y, ...)` - Draw image

### ⚠️ Partially Implemented

**Audio (Placeholder):**
- Audio module exists but is non-functional
- Needs SDL_mixer or OpenAL integration

### ❌ Not Yet Implemented

**L2 - Essential:**
- Font loading and text rendering (FreeType)
- Additional graphics state (line width, point size)
- Blend modes
- Image filtering
- Canvases (render targets)

**L3 - Advanced:**
- Shaders (GLSL)
- Sprite batches
- Meshes
- Particle systems
- Stencil/scissor operations

**L4 - Expert:**
- Joystick/gamepad input
- Touch input
- Video playback
- Threading

**L5 - Specialized:**
- Physics (Box2D)
- Networking (enet)
- Advanced audio effects

## Next Steps

### Immediate (To Complete L1)

1. **Wire up remaining callbacks in C++ executable:**
   - `love_keyreleased`
   - `love_mousereleased`
   - `love_mousemoved`

2. **Add text rendering:**
   - Integrate FreeType for font loading
   - Implement `love.graphics.print()` and `love.graphics.printf()`

3. **Complete audio implementation:**
   - Integrate SDL_mixer
   - Implement actual audio playback

### Medium Term (L2)

1. Image filtering and blend modes
2. Canvas/render targets for offscreen rendering
3. Additional graphics state management
4. More comprehensive filesystem operations

### Long Term (L3-L5)

1. Shader support
2. Advanced graphics features
3. Joystick/gamepad support
4. Physics integration
5. Networking

## Testing

Run the examples to test the API:

```bash
# Basic rendering test
./bin/love examples/visual_test.py

# Input handling test (keyboard + mouse)
./bin/love examples/interactive_game.py

# Transformations test
./bin/love examples/transformations_test.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests/examples if applicable
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Original LÖVE2D framework (love2d.org)
- pybind11 for Python C++ bindings
- SDL2 for cross-platform windowing and input
- stb_image for image loading
