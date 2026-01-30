# LOVE2D Python API Implementation Plan

## Overview

This document tracks the implementation progress of the LÖVE 11.5 API in Python.
APIs are organized by priority level (L1-L5) with corresponding test requirements.

**Legend:**
- `[ ]` - Not implemented
- `[~]` - In progress
- `[x]` - Implemented with tests passing
- `[-]` - Skipped/Not applicable

---

## L1 - CRITICAL (Core Game Loop) 🎯

**Goal:** Minimum viable game framework. Must have these to run any game.

### L1.1 Core Callbacks & Game Loop
- [x] `love.load()` - Game initialization callback
- [x] `love.update(dt)` - Update game state
- [x] `love.draw()` - Render game
- [x] `love.quit()` - Handle game quit
- [x] `love.run()` - Start the game loop

**Test Requirements:**
- [x] Test callback registration
- [x] Test game loop execution
- [x] Test quit handling

### L1.2 Window Management
- [x] `love.window.setMode(width, height, flags)` - Create/resize window
- [x] `love.window.getMode()` - Get window settings
- [x] `love.window.setTitle(title)` - Set window title
- [x] `love.window.close()` - Close window
- [x] `love.window.getDimensions()` - Get window size
- [x] `love.window.getWidth()` / `love.window.getHeight()` - Individual dimensions

**Test Requirements:**
- [x] Test window creation
- [x] Test window resizing
- [x] Test title setting

### L1.3 Graphics - Basic Drawing
- [x] `love.graphics.clear(r, g, b, a)` - Clear screen
- [x] `love.graphics.present()` - Display rendered frame
- [x] `love.graphics.setColor(r, g, b, a)` - Set drawing color
- [x] `love.graphics.getColor()` - Get current color
- [x] `love.graphics.setBackgroundColor(r, g, b, a)` - Set background color
- [x] `love.graphics.getBackgroundColor()` - Get background color
- [x] `love.graphics.rectangle(mode, x, y, w, h)` - Draw rectangle
- [x] `love.graphics.circle(mode, x, y, radius)` - Draw circle
- [x] `love.graphics.line(x1, y1, x2, y2, ...)` - Draw line

**Test Requirements:**
- [ ] Test color setting/retrieval
- [ ] Test rectangle drawing
- [ ] Test circle drawing
- [ ] Test line drawing
- [ ] Visual test: renders correctly

### L1.4 Timer
- [x] `love.timer.getDelta()` - Get delta time
- [x] `love.timer.getFPS()` - Get current FPS
- [x] `love.timer.getTime()` - Get elapsed time

**Test Requirements:**
- [ ] Test delta time calculation
- [ ] Test FPS calculation
- [ ] Test timing accuracy

### L1.5 Input - Keyboard
- [x] `love.keyboard.isDown(key, ...)` - Check key press
- [x] `love.keyboard.KeyConstant` - Key code constants
- [ ] `love.keypressed(key, scancode, isrepeat)` - Key press callback
- [ ] `love.keyreleased(key, scancode)` - Key release callback

**Test Requirements:**
- [ ] Test key detection
- [ ] Test callback invocation

### L1.6 Input - Mouse
- [x] `love.mouse.getPosition()` - Get mouse position
- [x] `love.mouse.getX()` / `love.mouse.getY()` - Individual coordinates
- [x] `love.mouse.isDown(button, ...)` - Check button press
- [ ] `love.mousepressed(x, y, button, istouch, presses)` - Press callback
- [ ] `love.mousereleased(x, y, button, istouch, presses)` - Release callback

**Test Requirements:**
- [ ] Test position retrieval
- [ ] Test button detection
- [ ] Test callback invocation

### L1.7 Event System
- [x] `love.event.pump()` - Poll for events
- [x] `love.event.poll()` - Get next event
- [x] `love.event.quit()` - Queue quit event

**Test Requirements:**
- [ ] Test event polling
- [ ] Test quit event

---

## L2 - ESSENTIAL (Complete Game Framework) 🎮

**Goal:** Feature-complete for most 2D games.

### L2.1 Graphics - Images
- [ ] `love.graphics.newImage(filename)` - Load image
- [ ] `Image:getWidth()` / `Image:getHeight()` - Get image dimensions
- [ ] `Image:getDimensions()` - Get both dimensions
- [ ] `Image:getFilter()` / `Image:setFilter()` - Image filtering
- [ ] `love.graphics.draw(image, x, y, r, sx, sy, ox, oy, kx, ky)` - Draw image
- [ ] `love.graphics.setBlendMode(mode)` - Set blend mode
- [ ] `love.graphics.getBlendMode()` - Get blend mode

**Test Requirements:**
- [ ] Test image loading
- [ ] Test image drawing
- [ ] Test blend modes

### L2.2 Graphics - Text
- [ ] `love.graphics.newFont(filename, size)` - Load font
- [ ] `love.graphics.setFont(font)` - Set active font
- [ ] `love.graphics.getFont()` - Get active font
- [ ] `love.graphics.print(text, x, y, r, sx, sy, ...)` - Draw text
- [ ] `love.graphics.printf(text, x, y, limit, align, ...)` - Formatted text
- [ ] `Font:getWidth(text)` - Get text width
- [ ] `Font:getHeight()` - Get font height

**Test Requirements:**
- [ ] Test font loading
- [ ] Test text rendering
- [ ] Test text formatting

### L2.3 Graphics - Advanced Shapes
- [ ] `love.graphics.ellipse(mode, x, y, rx, ry)` - Draw ellipse
- [ ] `love.graphics.arc(mode, x, y, r, angle1, angle2)` - Draw arc
- [ ] `love.graphics.polygon(mode, vertices)` - Draw polygon
- [ ] `love.graphics.points(x1, y1, ...)` - Draw points

**Test Requirements:**
- [ ] Test each shape type

### L2.4 Graphics - Transformations
- [x] `love.graphics.push()` - Save transform state
- [x] `love.graphics.pop()` - Restore transform state
- [x] `love.graphics.origin()` - Reset transformation
- [x] `love.graphics.translate(dx, dy)` - Translate
- [x] `love.graphics.rotate(angle)` - Rotate
- [x] `love.graphics.scale(sx, sy)` - Scale
- [ ] `love.graphics.shear(kx, ky)` - Shear
- [ ] `love.graphics.applyTransform(transform)` - Apply transform object
- [ ] `love.graphics.replaceTransform(transform)` - Replace transform

**Test Requirements:**
- [ ] Test transform stack
- [ ] Test individual transformations

### L2.5 Graphics - State Management
- [ ] `love.graphics.setLineWidth(width)` - Set line width
- [ ] `love.graphics.getLineWidth()` - Get line width
- [ ] `love.graphics.setLineStyle(style)` - Set line style
- [ ] `love.graphics.setPointSize(size)` - Set point size
- [ ] `love.graphics.setBlendMode(mode, alphamode)` - Set blend with alpha
- [ ] `love.graphics.getBlendMode()` - Get full blend mode

**Test Requirements:**
- [ ] Test each state setting

### L2.6 Audio
- [ ] `love.audio.newSource(filename, type)` - Create audio source
- [ ] `love.audio.play(source)` - Play audio
- [ ] `love.audio.stop(source)` - Stop audio
- [ ] `love.audio.pause(source)` - Pause audio
- [ ] `love.audio.resume(source)` - Resume audio
- [ ] `love.audio.setVolume(volume)` - Set master volume
- [ ] `love.audio.getVolume()` - Get master volume
- [ ] `Source:play()` / `Source:stop()` / `Source:pause()` / `Source:resume()`
- [ ] `Source:setVolume(volume)` / `Source:getVolume()`
- [ ] `Source:setLooping(loop)` / `Source:isLooping()`
- [ ] `Source:isPlaying()` - Check if playing

**Test Requirements:**
- [ ] Test audio loading
- [ ] Test playback controls
- [ ] Test volume control

### L2.7 Filesystem
- [ ] `love.filesystem.read(filename, bytes)` - Read file
- [ ] `love.filesystem.write(filename, data)` - Write file
- [ ] `love.filesystem.exists(path)` - Check if exists
- [ ] `love.filesystem.isFile(path)` - Check if file
- [ ] `love.filesystem.isDirectory(path)` - Check if directory
- [ ] `love.filesystem.createDirectory(name)` - Create directory
- [ ] `love.filesystem.getDirectoryItems(dir)` - List directory
- [ ] `love.filesystem.getSaveDirectory()` - Get save directory
- [ ] `love.filesystem.getWorkingDirectory()` - Get working directory

**Test Requirements:**
- [ ] Test file read/write
- [ ] Test directory operations
- [ ] Test path operations

### L2.8 Window - Additional Features
- [ ] `love.window.setFullscreen(fullscreen, type)` - Set fullscreen
- [ ] `love.window.getFullscreen()` - Get fullscreen state
- [ ] `love.window.setVSync(vsync)` - Set vsync
- [ ] `love.window.getVSync()` - Get vsync state
- [ ] `love.window.hasFocus()` - Check keyboard focus
- [ ] `love.window.hasMouseFocus()` - Check mouse focus
- [ ] `love.window.setIcon(imagedata)` - Set window icon

**Test Requirements:**
- [ ] Test each feature

### L2.9 Math
- [ ] `love.math.random()` / `love.math.random(m)` / `love.math.random(m, n)`
- [ ] `love.math.randomSeed(seed)` - Set random seed
- [ ] `love.math.setRandomSeed(seed)` - Alternative seed setter
- [ ] `love.math.newRandomGenerator(seed)` - Create RNG object

**Test Requirements:**
- [ ] Test random number generation
- [ ] Test seed setting

---

## L3 - ADVANCED (Professional Features) 🚀

**Goal:** Professional-grade game development features.

### L3.1 Graphics - Canvases (Render Targets)
- [ ] `love.graphics.newCanvas(width, height)` - Create canvas
- [ ] `love.graphics.setCanvas(canvas)` - Set render target
- [ ] `love.graphics.getCanvas()` - Get current canvas
- [ ] `Canvas:renderTo(func)` - Render to canvas
- [ ] `Canvas:generateMipmaps()` - Generate mipmaps
- [ ] `Canvas:getImageData()` - Get pixel data

**Test Requirements:**
- [ ] Test canvas creation
- [ ] Test offscreen rendering
- [ ] Test canvas switching

### L3.2 Graphics - Shaders
- [ ] `love.graphics.newShader(code)` - Create shader
- [ ] `love.graphics.setShader(shader)` - Set shader
- [ ] `love.graphics.getShader()` - Get current shader
- [ ] `Shader:send(name, value)` - Send uniform
- [ ] `Shader:sendColor(name, ...)` - Send color uniform
- [ ] `Shader:getWarnings()` - Get shader warnings

**Test Requirements:**
- [ ] Test shader compilation
- [ ] Test uniform setting
- [ ] Test shader effects

### L3.3 Graphics - Quads & Sprites
- [ ] `love.graphics.newQuad(x, y, w, h, sw, sh)` - Create quad
- [ ] `love.graphics.drawq(image, quad, x, y, ...)` - Draw with quad (deprecated, use draw)
- [ ] `Quad:setViewport(x, y, w, h)` - Set viewport
- [ ] `Quad:getViewport()` - Get viewport
- [ ] `love.graphics.newSpriteBatch(image, max)` - Create sprite batch
- [ ] `SpriteBatch:add(x, y, r, sx, sy, ...)` - Add sprite
- [ ] `SpriteBatch:clear()` - Clear batch
- [ ] `SpriteBatch:flush()` - Flush batch

**Test Requirements:**
- [ ] Test quad operations
- [ ] Test sprite batch

### L3.4 Graphics - Meshes
- [ ] `love.graphics.newMesh(vertices, mode, usage)` - Create mesh
- [ ] `Mesh:setVertices(vertices)` - Set vertices
- [ ] `Mesh:setVertexMap(map)` - Set vertex map
- [ ] `Mesh:setTexture(texture)` - Set texture
- [ ] `love.graphics.draw(mesh, ...)` - Draw mesh

**Test Requirements:**
- [ ] Test mesh creation
- [ ] Test vertex manipulation

### L3.5 Graphics - Particle Systems
- [ ] `love.graphics.newParticleSystem(texture, max)` - Create particle system
- [ ] `ParticleSystem:setPosition(x, y)` - Set emitter position
- [ ] `ParticleSystem:setEmissionRate(rate)` - Set emission rate
- [ ] `ParticleSystem:setParticleLifetime(min, max)` - Set lifetime
- [ ] `ParticleSystem:setColors(...)` - Set colors
- [ ] `ParticleSystem:setSizes(...)` - Set sizes
- [ ] `ParticleSystem:update(dt)` - Update particles
- [ ] `love.graphics.draw(particles, ...)` - Draw particles

**Test Requirements:**
- [ ] Test particle system creation
- [ ] Test particle emission

### L3.6 Graphics - Stencil & Scissor
- [ ] `love.graphics.setStencilTest(cmpmode, refvalue)` - Set stencil test
- [ ] `love.graphics.getStencilTest()` - Get stencil test
- [ ] `love.graphics.setScissor(x, y, w, h)` - Set scissor rectangle
- [ ] `love.graphics.getScissor()` - Get scissor rectangle
- [ ] `love.graphics.clearStencil()` - Clear stencil buffer

**Test Requirements:**
- [ ] Test stencil operations
- [ ] Test scissor operations

### L3.7 Math - Advanced
- [ ] `love.math.newTransform()` - Create transform object
- [ ] `Transform:translate(x, y)` - Translate transform
- [ ] `Transform:rotate(angle)` - Rotate transform
- [ ] `Transform:scale(sx, sy)` - Scale transform
- [ ] `Transform:apply(other)` - Apply another transform
- [ ] `Transform:reset()` - Reset to identity
- [ ] `Transform:getMatrix()` - Get matrix values
- [ ] `love.math.noise(x, y, z, w)` - Simplex noise
- [ ] `love.math.newBezierCurve(points)` - Create Bezier curve

**Test Requirements:**
- [ ] Test transform operations
- [ ] Test noise generation

### L3.8 Audio - Advanced
- [ ] `love.audio.newSource(type)` - Create empty source
- [ ] `Source:queue(data)` - Queue audio data
- [ ] `Source:setPitch(pitch)` / `Source:getPitch()`
- [ ] `Source:setPosition(x, y, z)` / `Source:getPosition()`
- [ ] `Source:setVelocity(x, y, z)` / `Source:getVelocity()`
- [ ] `Source:setDirection(x, y, z)` / `Source:getDirection()`
- [ ] `Source:setCone(innerAngle, outerAngle, outerVolume)` / `Source:getCone()`
- [ ] `love.audio.setPosition(x, y, z)` - Set listener position
- [ ] `love.audio.setOrientation(fx, fy, fz, ux, uy, uz)` - Set listener orientation
- [ ] `love.audio.getSourceCount()` - Get total sources
- [ ] `love.audio.getActiveSourceCount()` - Get active sources

**Test Requirements:**
- [ ] Test advanced source features
- [ ] Test spatial audio
- [ ] Test streaming

### L3.9 Filesystem - Advanced
- [ ] `love.filesystem.append(filename, data)` - Append to file
- [ ] `love.filesystem.getInfo(path, filtertype)` - Get file info
- [ ] `love.filesystem.getSize(filename)` - Get file size
- [ ] `love.filesystem.getLastModified(filename)` - Get modification time
- [ ] `love.filesystem.setIdentity(name, append)` - Set save directory
- [ ] `love.filesystem.getIdentity()` - Get save directory name
- [ ] `love.filesystem.mount(path, mountpoint)` - Mount directory
- [ ] `love.filesystem.unmount(path)` - Unmount directory

**Test Requirements:**
- [ ] Test file info retrieval
- [ ] Test mount operations

---

## L4 - EXPERT (Specialized Features) 🔧

**Goal:** Specialized/advanced features for complex games.

### L4.1 Graphics - Framebuffers & Multiple Canvases
- [ ] `love.graphics.setCanvas(canvas1, canvas2, ...)` - Multiple render targets
- [ ] `love.graphics.getCanvas()` - Get all active canvases
- [ ] `Canvas:getFormat()` - Get pixel format
- [ ] `Canvas:getMSAA()` - Get MSAA level

### L4.2 Graphics - Mipmaps & Anisotropy
- [ ] `Image:generateMipmaps()` - Generate mipmaps
- [ ] `Image:setMipmapFilter(filter, sharpness)` - Set mipmap filter
- [ ] `Image:setFilter(min, mag, anisotropy)` - Set filter with anisotropy

### L4.3 Graphics - Video
- [ ] `love.graphics.newVideo(filename)` - Load video
- [ ] `Video:play()` / `Video:pause()` / `Video:seek(position)`
- [ ] `Video:isPlaying()` / `Video:tell()` / `Video:getDuration()`
- [ ] `love.graphics.draw(video, ...)` - Draw video frame

### L4.4 Joystick Input
- [ ] `love.joystick.getJoysticks()` - Get all joysticks
- [ ] `Joystick:isConnected()` - Check connection
- [ ] `Joystick:getName()` - Get joystick name
- [ ] `Joystick:getAxis(axis)` - Get axis value
- [ ] `Joystick:isDown(button)` - Check button
- [ ] `Joystick:getHat(hat)` - Get hat direction
- [ ] `love.joystickadded(joystick)` - Joystick connected callback
- [ ] `love.joystickremoved(joystick)` - Joystick disconnected callback
- [ ] `love.joystickpressed(joystick, button)` - Button press callback
- [ ] `love.joystickreleased(joystick, button)` - Button release callback

### L4.5 Gamepad Input
- [ ] `Joystick:isGamepad()` - Check if gamepad
- [ ] `Joystick:getGamepadAxis(axis)` - Get gamepad axis
- [ ] `Joystick:isGamepadDown(button)` - Check gamepad button
- [ ] `love.gamepadpressed(joystick, button)` - Gamepad press callback
- [ ] `love.gamepadreleased(joystick, button)` - Gamepad release callback
- [ ] `love.gamepadaxis(joystick, axis, value)` - Gamepad axis callback

### L4.6 Touch Input
- [ ] `love.touch.getTouches()` - Get active touches
- [ ] `love.touch.getPosition(id)` - Get touch position
- [ ] `love.touch.getPressure(id)` - Get touch pressure
- [ ] `love.touchpressed(id, x, y, dx, dy, pressure)` - Touch press callback
- [ ] `love.touchreleased(id, x, y, dx, dy, pressure)` - Touch release callback
- [ ] `love.touchmoved(id, x, y, dx, dy, pressure)` - Touch move callback

### L4.7 Threading
- [ ] `love.thread.newThread(code)` - Create thread
- [ ] `Thread:start(...)` - Start thread
- [ ] `Thread:wait()` - Wait for thread
- [ ] `Thread:getError()` - Get thread error
- [ ] `love.thread.getChannel(name)` - Get channel
- [ ] `Channel:push(value)` - Push value to channel
- [ ] `Channel:pop()` - Pop value from channel
- [ ] `Channel:peek()` - Peek at value
- [ ] `Channel:clear()` - Clear channel

### L4.8 System
- [ ] `love.system.getOS()` - Get operating system
- [ ] `love.system.getProcessorCount()` - Get CPU count
- [ ] `love.system.getClipboardText()` - Get clipboard
- [ ] `love.system.setClipboardText(text)` - Set clipboard
- [ ] `love.system.openURL(url)` - Open URL in browser
- [ ] `love.system.vibrate(seconds)` - Vibrate device

### L4.9 Data Compression
- [ ] `love.data.compress(container, format, data, level)` - Compress data
- [ ] `love.data.decompress(container, format, data)` - Decompress data
- [ ] `love.data.encode(container, format, data)` - Encode data
- [ ] `love.data.decode(container, format, data)` - Decode data
- [ ] `love.data.hash(hashFunction, data)` - Hash data

---

## L5 - SPECIALIZED (Platform/Edge Cases) 🔮

**Goal:** Platform-specific features and edge cases.

### L5.1 Window - Platform Features
- [ ] `love.window.setDisplaySleepEnabled(enable)` - Control display sleep
- [ ] `love.window.isDisplaySleepEnabled()` - Check display sleep
- [ ] `love.window.setPosition(x, y, display)` - Set window position
- [ ] `love.window.getPosition()` - Get window position
- [ ] `love.window.getDesktopDimensions(display)` - Get desktop size
- [ ] `love.window.getDisplayCount()` - Get display count
- [ ] `love.window.getDisplayName(display)` - Get display name
- [ ] `love.window.getDisplayOrientation(display)` - Get orientation
- [ ] `love.window.toPixels(value)` - Convert to pixels
- [ ] `love.window.fromPixels(value)` - Convert from pixels
- [ ] `love.window.maximize()` / `love.window.minimize()` / `love.window.restore()`

### L5.2 Graphics - Advanced Shaders
- [ ] Multiple shader stages (vertex, geometry, fragment)
- [ ] Shader uniforms: arrays, structs
- [ ] Compute shaders (if supported)
- [ ] `Shader:getWarnings()` detailed shader compilation info

### L5.3 Audio - Effects
- [ ] `love.audio.setEffect(name, settings)` - Set audio effect
- [ ] `love.audio.getEffect(name)` - Get effect settings
- [ ] `love.audio.removeEffect(name)` - Remove effect
- [ ] `Source:setEffect(name, filter)` - Apply effect to source
- [ ] `Source:setFilter(settings)` - Set filter
- [ ] `Source:getFilter()` - Get filter

### L5.4 Physics (Box2D) - If implemented
- [ ] `love.physics.newWorld(xg, yg, sleep)` - Create physics world
- [ ] `World:update(dt)` - Update physics
- [ ] `World:setCallbacks(...)` - Set collision callbacks
- [ ] `love.physics.newBody(world, x, y, type)` - Create body
- [ ] `Body:applyForce(fx, fy)` - Apply force
- [ ] `Body:setPosition(x, y)` / `Body:getPosition()`
- [ ] `Body:setAngle(angle)` / `Body:getAngle()`
- [ ] `love.physics.newFixture(body, shape, density)` - Create fixture
- [ ] `love.physics.newRectangleShape(w, h)` - Rectangle shape
- [ ] `love.physics.newCircleShape(r)` - Circle shape
- [ ] `love.physics.newPolygonShape(vertices)` - Polygon shape

### L5.5 Network (enet) - If implemented
- [ ] `love.network.newClient(host, port)` - Create client
- [ ] `love.network.newServer(port, maxPeers)` - Create server
- [ ] `Client:send(data, channel, flag)` - Send data
- [ ] `Server:broadcast(data, channel, flag)` - Broadcast
- [ ] Connection/disconnection callbacks

### L5.6 Image Module (Direct pixel access)
- [ ] `love.image.newImageData(width, height)` - Create image data
- [ ] `love.image.newImageData(filename)` - Load image data
- [ ] `ImageData:getWidth()` / `ImageData:getHeight()`
- [ ] `ImageData:getPixel(x, y)` - Get pixel color
- [ ] `ImageData:setPixel(x, y, r, g, b, a)` - Set pixel
- [ ] `ImageData:paste(source, x, y)` - Paste image data
- [ ] `ImageData:encode(format)` - Encode to file
- [ ] `Image:newImageData()` - Get image data from image

### L5.7 Font Module (Glyph data)
- [ ] `love.font.newRasterizer(filename, size)` - Create rasterizer
- [ ] `Rasterizer:getGlyphData(glyph)` - Get glyph data
- [ ] `Rasterizer:getGlyphCount()` - Get glyph count
- [ ] `Rasterizer:getAdvance()` - Get advance
- [ ] `Rasterizer:getAscent()` / `Rasterizer:getDescent()`
- [ ] `Rasterizer:getHeight()` - Get line height

### L5.8 Sound Module (Raw audio data)
- [ ] `love.sound.newSoundData(samples, rate, bits, channels)` - Create sound data
- [ ] `love.sound.newSoundData(filename)` - Load sound file
- [ ] `SoundData:getSample(i)` - Get sample
- [ ] `SoundData:setSample(i, sample)` - Set sample
- [ ] `SoundData:getSampleRate()` / `SoundData:getBitDepth()` / `SoundData:getChannelCount()`
- [ ] `SoundData:getDuration()` - Get duration
- [ ] `Source:newSource(sounddata, type)` - Create source from sound data

### L5.9 Video Module (Raw video data)
- [ ] `love.video.newVideoStream(filename)` - Create video stream
- [ ] `VideoStream:play()` / `VideoStream:pause()` / `VideoStream:seek()`
- [ ] `VideoStream:isPlaying()` / `VideoStream:tell()` / `VideoStream:getDuration()`
- [ ] `VideoStream:getWidth()` / `VideoStream:getHeight()`
- [ ] `VideoStream:getFrameRate()` / `VideoStream:getFrameCount()`

### L5.10 Miscellaneous
- [ ] `love.getVersion()` - Get LÖVE version
- [ ] `love.isVersionCompatible(version)` - Check compatibility
- [ ] `love.setDeprecationOutput(enable)` - Control deprecation warnings
- [ ] `love.hasDeprecationOutput()` - Check deprecation output
- [ ] `love.conf(t)` - Configuration callback
- [ ] `love.directorydropped(path)` - Directory drop callback
- [ ] `love.filedropped(file)` - File drop callback
- [ ] `love.focus(focus)` - Window focus callback
- [ ] `love.resize(w, h)` - Window resize callback
- [ ] `love.textinput(text)` - Text input callback
- [ ] `love.visible(visible)` - Window visibility callback
- [ ] `love.wheelmoved(x, y)` - Mouse wheel callback

---

## Testing Strategy

### L1 Testing (Critical)
- All tests must pass before release
- Visual tests required for graphics
- Input tests require manual verification
- Automated CI/CD testing

### L2 Testing (Essential)
- 90% code coverage required
- All public APIs must have unit tests
- Integration tests for module interactions
- Performance benchmarks

### L3 Testing (Advanced)
- Feature-specific test suites
- Example projects demonstrating features
- Documentation with working code samples

### L4 Testing (Expert)
- Specialized test environments
- Platform-specific testing
- Edge case documentation

### L5 Testing (Specialized)
- Optional platform testing
- Community testing for edge cases
- Example implementations

---

## Progress Tracking

**Current Stats:**
- L1: ~60% Complete (Basic structure done, needs tests)
- L2: ~5% Complete (Not implemented)
- L3: ~0% Complete (Not implemented)
- L4: ~0% Complete (Not implemented)
- L5: ~0% Complete (Not implemented)

**Next Milestone:** Complete L1 testing and begin L2 implementation.

---

## Notes

- Priority order: L1 > L2 > L3 > L4 > L5
- Each level builds on previous levels
- Tests are mandatory for each implemented API
- Documentation required for all public APIs
- Breaking changes should be avoided after L1 completion
- Performance considerations important from L2 onwards
