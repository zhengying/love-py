# LOVE2D Python - 当前实现状态

更新时间：2026-02-02

## 目标与参考

本项目目标是实现 LÖVE 11.5 的 Python 版本 API。

API 参考位于：
- `references/love-api-orignal_11_5/`：官方 LÖVE 11.5 API 的 Lua 描述（按模块拆分）
- `references/love_api_py/`：API 数据与检查工具（Python）

实现规划/勾选表位于：
- `API_IMPLEMENTATION_PLAN.md`

## 当前运行架构（真实生效路径）

当前可执行文件 `bin/love` 与 `bin/love.app` 走的是“嵌入 Python + 注入 love 模块”的路径：

- 主入口：`src/love.cpp`
- 启动时会创建并注入 `love` 模块（包含若干子模块）
- 你的游戏脚本需要定义回调函数（见下方“回调”）

说明：`src/love2d_bindings.cpp` 以及 `src/*_module.cpp` 里的 pybind11 绑定目前并不是 `bin/love` 的主要 API 来源；当前对外暴露的 `love.*` 以 `src/love.cpp` 内的模块注入为准。

## 构建与打包（macOS）

推荐用脚本：

```bash
./mac_build.sh love   # 生成 bin/love
./mac_build.sh app    # 生成 bin/love.app
./mac_build.sh all    # 两者都生成
```

对应的 CMake targets：
- `love`
- `love_app`

## 运行方式

```bash
./bin/love examples/test_simple.py

./bin/love.app/Contents/MacOS/love examples/test_simple.py
```

## 已实现模块与关键 API（以 src/love.cpp 为准）

当前注入的模块列表：
- `love`
- `love.graphics`
- `love.window`
- `love.timer`
- `love.keyboard`
- `love.mouse`
- `love.event`
- `love.filesystem`
- `love.image`
- `love.font`

### love（全局）

- `love.getVersion() -> (major, minor, revision, codename)`
- `love.setDeprecationOutput(enabled: bool)`
- `love.hasDeprecationOutput() -> bool`
- `love.isVersionCompatible(version: str) -> bool`

### love.window

- `love.window.setMode(width, height, flags: dict = {}) -> bool`
- `love.window.getMode() -> (width, height, flags)`
- `love.window.setTitle(title: str)`
- `love.window.close()`
- `love.window.getWidth() / getHeight() / getDimensions()`

说明：`flags` 当前只解析 `fullscreen/resizable/vsync`，并且返回的 flags 也只覆盖上述字段。

### love.timer

- `love.timer.getTime() -> float`
- `love.timer.getDelta() -> float`
- `love.timer.getFPS() -> float`
- `love.timer.sleep(seconds: float)`

### love.keyboard

- `love.keyboard.isDown(key1: str, key2: str, ...) -> bool`

说明：当前 `key` 使用 `SDL_GetScancodeFromName` 解析（更接近 scancode 名称），与 LÖVE 的 KeyConstant/Scancode 体系仍有差距。

### love.mouse

- `love.mouse.getPosition() -> (x, y)`
- `love.mouse.getX() / getY()`
- `love.mouse.isDown(button: int) -> bool`

### love.event

- `love.event.quit()`

说明：目前没有 `pump/poll/push` 等完整事件队列 API（但引擎内部会处理 SDL 事件并触发 Python 回调，见下方“回调”）。

### love.graphics（2D 最小子集 + 图片/字体绘制）

- 基础图元：`clear / setColor / getColor / setBackgroundColor / getBackgroundColor / rectangle / circle / line`
- 变换：`push / pop / origin / translate / rotate / scale`
- 尺寸：`getWidth / getHeight / getDimensions`
- 图片绘制：`drawImage(image, x=0, y=0, r=0, sx=1, sy=1, ox=0, oy=0)`
- 字体与文本：`newFont(filename, size=12)`, `setFont(font)`, `getFont()`, `print(text, x, y, r=0, sx=1, sy=1)`

说明：`print` 依赖当前字体；如果没有显式设置字体，需要先调用 `love.graphics.getFont()` 触发默认字体加载。

### love.image / love.font

- `love.image.newImage(filename) -> Image`
- `love.font.newFont(filename, size=12) -> Font`

说明：与原版 LÖVE 的 `love.graphics.newImage()` / `love.graphics.draw()` 命名不一致，目前是 `love.image.newImage()` + `love.graphics.drawImage()` 组合。

### love.filesystem（最小子集）

- `read(filename) -> str`
- `write(filename, data: bytes) -> bool`
- `exists(path) -> bool`
- `isFile(path) -> bool`
- `isDirectory(path) -> bool`
- `createDirectory(name) -> bool`
- `getWorkingDirectory() -> str`
- `getDirectoryItems(dir) -> list[str]`

## 回调支持（脚本入口）

脚本中可定义以下函数（存在则被引擎调用）：

- `love_load()`
- `love_update(dt)`
- `love_draw()`
- `love_quit()`

输入回调（当前引擎事件循环会调用）：
- `love_keypressed(key, scancode, isrepeat)`
- `love_keyreleased(key, scancode)`
- `love_mousepressed(x, y, button, istouch, presses)`
- `love_mousereleased(x, y, button, istouch, presses)`
- `love_mousemoved(x, y, dx, dy, istouch)`

## 重要缺失（高优先级）

以下模块尚未进入当前注入的 `love` API（即：脚本里 import/调用不到对应模块）：

- `love.audio`（目前是最大缺口之一）
- `love.system`
- `love.math`
- `love.joystick` / `love.touch`
- `love.thread`
- `love.data`
- `love.physics`
- `love.sound`
- `love.video`

图形高级能力缺失：
- Canvas / Shader / Mesh / SpriteBatch / Stencil / Scissor 等都未实现
- 形状类（ellipse/arc/polygon/points）、混合模式、线宽等状态也未覆盖

## 仓库约定（开发时）

- `bin/` 是构建产物目录，不应提交
- `external/` 是 vendored 依赖目录，仅保留在工作区，不应提交
