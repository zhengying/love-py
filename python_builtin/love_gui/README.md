# love_gui (Python) — Usage Guide

`love_gui` is a small immediate-style-ish retained widget toolkit for LÖVE (Love2D) in Python. You create a widget tree, update it every frame, forward input events, and let the UI draw.

## Quick Start

Minimal structure:

```python
import love
import love_gui

ui = None

def love_load():
    global ui
    theme = love_gui.create_default_theme(love)
    ui = love_gui.UI(theme=theme)

    w, h = love.graphics.getDimensions()
    root = love_gui.Panel(love_gui.Rect(20, 20, w - 40, h - 40))
    ui.root = root

    def on_click():
        print("clicked")

    root.add(love_gui.Label(love_gui.Rect(20, 20, 0, 0), "Hello"))
    root.add(love_gui.Button(love_gui.Rect(20, 50, 160, 36), "Click", on_click=on_click))

def love_update(dt):
    ui.update(dt)

def love_draw():
    love.graphics.clear()
    ui.draw(love)

    w, h = love.graphics.getDimensions()
    ui.root.rect.w = w - 40
    ui.root.rect.h = h - 40
```

## Forwarding Input Events

Forward your Love2D input callbacks into `UI`:

```python
def love_mousepressed(x, y, button, istouch, presses):
    ui.on_mousepressed(x, y, button, istouch, presses)

def love_mousereleased(x, y, button, istouch, presses):
    ui.on_mousereleased(x, y, button, istouch, presses)

def love_mousemoved(x, y, dx, dy, istouch):
    ui.on_mousemoved(x, y, dx, dy, istouch)

def love_wheelmoved(x, y):
    ui.on_wheelmoved(x, y)

def love_keypressed(key, scancode, isrepeat):
    ui.on_keypressed(key, scancode, isrepeat)

def love_textinput(text):
    ui.on_textinput(text)
```

Notes:
- `TextInput` receives keyboard events only when focused (handled by `UI`).
- While a `PopupMenu` or `MessageBox` is visible, the UI routes input to it and blocks the underlying widgets.

## Coordinate System (Important)

Each widget has a `Rect(x, y, w, h)` stored in `widget.rect`.

- For normal containers, `rect.x/y` are **relative to the parent**.
- `widget.abs_rect()` converts to absolute coordinates by walking the parent chain.
- For children inside `ScrollView`, their absolute position is offset by the current scroll.

This means you typically position children using coordinates relative to their container.

## Layout

You can position widgets in two ways:

1. **Absolute placement**
   - Directly set `Rect(x, y, w, h)` for each widget.
2. **Auto-layout containers (recommended)**
   - Containers can compute children sizes/positions via `measure()` + `layout()`.
   - `UI.draw()` calls `root.layout_tree(theme)` before drawing, so auto-layout updates every frame.

### VBox / HBox

Simple linear layout:

```python
col = root.add(love_gui.VBox(love_gui.Rect(20, 20, 300, 0), spacing=8, auto_layout=True))
col.add(love_gui.Label(love_gui.Rect(0, 0, 0, 0), "Title"))
col.add(love_gui.Button(love_gui.Rect(0, 0, 0, 0), "OK"))
```

### FlowLayout

Flow layout wraps items to the next line when width is exceeded:

```python
flow = root.add(love_gui.FlowLayout(love_gui.Rect(20, 20, 320, 0), spacing=8, run_spacing=8, align="start"))
flow.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), "Tag 1"))
flow.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), "Longer Tag"))
```

`align` can be `"start"`, `"center"`, or `"end"`.

### FlexLayout

Flex layout distributes available space across items (grow/shrink) and supports wrapping:

```python
row = root.add(
    love_gui.FlexLayout(
        love_gui.Rect(20, 20, 520, 40),
        direction="row",
        wrap="wrap",          # "nowrap" or "wrap"
        spacing=8,
        run_spacing=8,
        justify_content="start",
        align_items="stretch",
    )
)

row.add(love_gui.TextInput(love_gui.Rect(0, 0, 0, 34), placeholder="Search..."), grow=1, basis=160, min_main=120)
row.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), "Fixed"), shrink=0, basis=92)
row.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), "Max 110"), basis=140, max_main=110)
```

Per-item parameters in `FlexLayout.add(...)`:
- `grow`: consumes remaining free space when positive
- `shrink`: participates in shrinking when content overflows
- `basis`: preferred main-axis size
- `min_main` / `max_main`: clamps final main-axis size
- `align`: overrides `align_items` for that one item (`"start"`, `"center"`, `"end"`, `"stretch"`)

## Widgets

Core widgets:
- `Panel`: a 9-slice framed container
- `Label`: draws text
- `Button`: click with `on_click`
- `CheckBox`: toggle with `on_change(checked: bool)`
- `TextInput`: editable text field with focus, cursor, selection logic
- `Slider`: drag to change value `0..1` with `on_change(value: float)`
- `ProgressBar`: displays `value` `0..1`
- `ScrollView`: clips children and supports wheel scrolling + draggable scrollbar

### ScrollView

```python
panel = root.add(love_gui.Panel(love_gui.Rect(20, 120, 420, 320)))
scroll = panel.add(love_gui.ScrollView(love_gui.Rect(10, 10, 400, 300)))

y = 0.0
for i in range(30):
    scroll.add(love_gui.Button(love_gui.Rect(0, y, 380, 32), f"Item {i + 1}"))
    y += 38.0
```

Tip: if your scroll content is taller than the view, the scrollbar appears and the wheel scroll will work even when the pointer is over child widgets (the wheel event bubbles to parents until handled).

## Popups and Modals

### PopupMenu

```python
def open_menu():
    mx, my = love.mouse.getPosition()
    ui.show_popup(
        love,
        float(mx),
        float(my),
        items=[
            love_gui.PopupMenuItem("Copy", lambda: print("copy")),
            love_gui.PopupMenuItem("Paste", lambda: print("paste")),
            love_gui.PopupMenuItem("Disabled", lambda: None, enabled=False),
        ],
    )
```

### MessageBox

```python
ui.show_message_box(
    love,
    "Confirm",
    "Are you sure?",
    show_cancel=True,
    on_confirm=lambda: print("yes"),
    on_cancel=lambda: print("no"),
)
```

## Theme

Create the default theme via:

```python
theme = love_gui.create_default_theme(love)
ui = love_gui.UI(theme=theme)
```

`Theme` mainly contains:
- `font`
- 9-slice skins for panels/buttons/inputs/tracks
- colors such as `text_color` and `accent`

You can provide your own theme as long as it matches the `Theme` dataclass fields.

## Practical Tips

- Always update the root size when the window is resizable (see the Quick Start example).
- Prefer `Panel` + auto-layout containers (`VBox`, `FlowLayout`, `FlexLayout`) over hard-coded coordinates for responsive UIs.
- If you need strict clipping for a region, put that content into a `ScrollView` (even if you never scroll).

