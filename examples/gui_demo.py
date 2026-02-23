import os
import sys

import love


def _import_love_gui():
    base = os.path.dirname(os.path.abspath(__file__))
    builtin = os.path.abspath(os.path.join(base, "..", "python_builtin"))
    if builtin not in sys.path:
        sys.path.insert(0, builtin)
    import love_gui

    return love_gui


love_gui = _import_love_gui()

_ui = None
_theme = None
_clicks = 0
_progress = 0.35
_slider = None
_bar = None
_label = None
_input = None


def love_conf(t):
    t["window"]["title"] = "LOVE GUI Demo (Python)"
    t["window"]["width"] = 960
    t["window"]["height"] = 640
    t["window"]["resizable"] = True
    t["window"]["vsync"] = True


def love_load():
    global _ui, _theme, _slider, _bar, _label, _input

    love.graphics.setBackgroundColor(0.08, 0.08, 0.10, 1.0)
    _theme = love_gui.create_default_theme(love)
    _ui = love_gui.UI(theme=_theme)

    w, h = love.graphics.getDimensions()
    root = love_gui.Panel(love_gui.Rect(20, 20, w - 40, h - 40))
    _ui.root = root

    header = root.add(love_gui.Label(love_gui.Rect(20, 18, 600, 22), "LOVE GUI demo: 9-slice + widgets"))
    header2 = root.add(love_gui.Label(love_gui.Rect(20, 44, 800, 22), "Click, drag, type, and scroll. ESC quits."))

    def on_click():
        global _clicks
        _clicks += 1
        _label.text = f"Button clicked: {_clicks}"

    btn = root.add(love_gui.Button(love_gui.Rect(20, 82, 200, 40), "Click me", on_click=on_click))
    _label = root.add(love_gui.Label(love_gui.Rect(240, 92, 340, 22), "Button clicked: 0"))

    def on_slider(v: float):
        global _progress
        _progress = v
        _bar.value = v

    _slider = root.add(love_gui.Slider(love_gui.Rect(20, 138, 320, 28), value=_progress, on_change=on_slider))
    _bar = root.add(love_gui.ProgressBar(love_gui.Rect(360, 138, 260, 28), value=_progress))

    _input = root.add(love_gui.TextInput(love_gui.Rect(20, 186, 360, 34), text="", placeholder="Type here..."))

    root.add(love_gui.Label(love_gui.Rect(20, 238, 360, 22), "ScrollView:"))
    scroll_panel = root.add(love_gui.Panel(love_gui.Rect(20, 266, 420, 320)))
    scroll = scroll_panel.add(love_gui.ScrollView(love_gui.Rect(10, 10, 400, 300)))

    y = 0.0
    for i in range(30):
        item = love_gui.Button(love_gui.Rect(0, y, 380, 32), f"Item {i + 1}")
        scroll.add(item)
        y += 38.0

    root.add(love_gui.Label(love_gui.Rect(470, 238, 360, 22), "9-slice samples:"))

    samples = root.add(love_gui.Panel(love_gui.Rect(470, 266, 450, 320)))
    samples.add(love_gui.Label(love_gui.Rect(20, 18, 280, 22), "Panel scales without stretching corners"))
    samples.add(love_gui.Panel(love_gui.Rect(20, 52, 180, 70)))
    samples.add(love_gui.Panel(love_gui.Rect(220, 52, 200, 110)))
    samples.add(love_gui.Button(love_gui.Rect(20, 150, 180, 46), "Button"))
    samples.add(love_gui.Button(love_gui.Rect(220, 150, 200, 46), "Bigger Button"))

    return None


def love_update(dt):
    if _ui is not None:
        _ui.update(dt)


def love_draw():
    love.graphics.clear()
    if _ui is not None:
        _ui.draw(love)

    w, h = love.graphics.getDimensions()
    if _ui is not None and _ui.root is not None:
        _ui.root.rect.w = w - 40
        _ui.root.rect.h = h - 40


def love_keypressed(key, scancode, isrepeat):
    if key == "escape":
        love.event.quit()
        return
    if _ui is not None:
        _ui.on_keypressed(key, scancode, isrepeat)


def love_textinput(text: str):
    if _ui is not None:
        _ui.on_textinput(text)


def love_mousepressed(x, y, button, istouch, presses):
    if _ui is not None:
        _ui.on_mousepressed(x, y, button, istouch, presses)


def love_mousereleased(x, y, button, istouch, presses):
    if _ui is not None:
        _ui.on_mousereleased(x, y, button, istouch, presses)


def love_mousemoved(x, y, dx, dy, istouch):
    if _ui is not None:
        _ui.on_mousemoved(x, y, dx, dy, istouch)


def love_wheelmoved(x, y):
    if _ui is not None:
        _ui.on_wheelmoved(x, y)
