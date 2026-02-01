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
│  │  • Runs SDL3 main loop                                 │  │
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
```

**Key Design Decision:** C++ owns the main loop (not Python), matching the original LÖVE2D design for proper frame timing.

## Build Instructions

### Prerequisites

- CMake 3.15+
- A C++17 compatible compiler
- OpenGL development libraries

Platform notes:
- macOS: the build uses the vendored embedded Python archive under `external/deps/python/*`, so a system Python/pip installation is not required.
- Linux/Windows: builds currently rely on a system Python (headers + library) to embed Python.

## Packaging & Deployment

This repository builds two different macOS outputs:
- `bin/love`: a command-line executable
- `bin/love.app`: a macOS `.app` bundle with embedded runtime dependencies

### Launching

- Run a script file:
  - `./bin/love path/to/game.py`
  - `./bin/love.app/Contents/MacOS/love path/to/game.py`
- Run a directory (auto-loads `main.py`):
  - `./bin/love path/to/game_dir`
  - `./bin/love.app/Contents/MacOS/love path/to/game_dir`
  - The launcher will look for `path/to/game_dir/main.py`, then `chdir` into `game_dir` so relative assets work.
- Launch with no arguments (macOS `.app` only):
  - Runs the bundled welcome script [no_game.py](file:///Users/zhengying/Documents/labs/love-python/love2d_py/resources/no_game.py)

### macOS `.app` bundle

- Build target:
  - `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release`
  - `cmake --build build --target love_app`
- Output:
  - `bin/love.app`
- Bundle layout (key parts):
  - `Contents/MacOS/love`: the executable
  - `Contents/Frameworks/SDL3.framework`: SDL3 runtime
  - `Contents/Frameworks/freetype.framework`: FreeType runtime
  - `Contents/Resources/python`: embedded Python runtime (copied from the vendored archive)
  - `Contents/Resources/resources`: bundled game resources (includes `font.ttf` and `no_game.py`)
- Python runtime selection on macOS:
  - At runtime, [love.cpp](file:///Users/zhengying/Documents/labs/love-python/love2d_py/src/love.cpp) prefers `Contents/Resources/python` as `PyConfig.home`.
  - You can override with `LOVE_PYTHON_HOME=/path/to/python` if needed.
- Dynamic linking:
  - The bundle uses `@rpath` for `SDL3.framework`, `freetype.framework`, and `libpython3.11.dylib`.
  - `rpath` entries are set to:
    - `@executable_path/../Frameworks`
    - `@executable_path/../Resources/python/lib`

### Vendored Python (macOS)

- Archives live under:
  - `external/deps/python/macos-arm64/python-standalone.tar.zst`
  - `external/deps/python/macos-x86_64/python-standalone.tar.zst`
- The build extracts the archive into `build*/embedded-python/python` and then copies it into the `.app`.
- The build also copies the embedded runtime to `bin/python/` so `bin/love` can run without a system Python.
- If you update the archive:
  - Keep the `python/` top-level directory inside the tarball (the build expects this layout).
  - Ensure it contains `python/lib/libpython*.dylib` and `python/include/python*/Python.h`.

### Builtin Python libraries (bundled with the app)

This project supports bundling your own Python libraries (and stubs for IDE completion) into the embedded runtime.

- Source directory (in repo): `python_builtin/`
- Destination (macOS):
  - `bin/love.app/Contents/Resources/python/builtin/`
  - `bin/python/builtin/` (for `bin/love`)
- Runtime behavior:
  - On startup, the launcher adds `<pythonHome>/builtin` to `sys.path`, so game scripts can `import` those packages.

### CI artifacts

- Windows and macOS build artifacts are produced by the workflow:
  - [.github/workflows/windows-build.yml](.github/workflows/windows-build.yml)
- Artifact names:
  - `love2d_py-windows-x64`: contains a `dist/` directory with `love.exe`, `python*.dll`, and vendored DLLs
  - `love2d_py-macos-bundle`: contains `dist/love.app`

### macOS

```bash
# Install dependencies
brew install cmake

# Clone and build
cd love2d_py

# Using CMake directly
mkdir -p build && cd build
cmake ..
make -j4

# The executable will be at bin/love
# The app bundle will be at bin/love.app
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
