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
_checkbox = None


def love_conf(t):
    t["window"]["title"] = "LOVE GUI Demo (Python)"
    t["window"]["width"] = 960
    t["window"]["height"] = 640
    t["window"]["resizable"] = True
    t["window"]["vsync"] = True


def love_load():
    global _ui, _theme, _slider, _bar, _label, _input, _checkbox

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

    input_h = love_gui.TextInput.preferred_height(_theme, min_height=34)
    row1_y = 186.0
    row_gap = 12.0

    row1 = root.add(
        love_gui.FlexLayout(
            love_gui.Rect(20, row1_y, root.rect.w - 40, input_h),
            direction="row",
            spacing=20.0,
            justify_content="start",
            align_items="stretch",
        )
    )
    _input = row1.add(love_gui.TextInput(love_gui.Rect(0, 0, 0, input_h), text="", placeholder="Type here..."), grow=1.0)

    def open_menu():
        mx, my = love.mouse.getPosition()

        def pick(name: str):
            def f():
                _label.text = f"Popup: {name}"
            return f

        _ui.show_popup(
            love,
            float(mx),
            float(my),
            items=[
                love_gui.PopupMenuItem("Copy", pick("Copy")),
                love_gui.PopupMenuItem("Paste", pick("Paste")),
                love_gui.PopupMenuItem("Disabled item", pick("Disabled"), enabled=False),
                love_gui.PopupMenuItem("Close", pick("Close")),
            ],
        )

    row1.add(love_gui.Button(love_gui.Rect(0, 0, 180, input_h), "Popup menu", on_click=open_menu), basis=180.0)

    def on_check(v: bool):
        _label.text = f"Checkbox: {'on' if v else 'off'}"

    _checkbox = row1.add(
        love_gui.CheckBox(love_gui.Rect(0, 0, 260, input_h), "Enable feature", checked=False, on_change=on_check),
        basis=260.0,
    )

    def open_notice():
        _ui.show_message_box(
            love,
            "Notice",
            "This is a notification message box.\nClick OK to close.",
            show_cancel=False,
            on_confirm=lambda: setattr(_label, "text", "Notice closed"),
        )

    def open_confirm():
        def on_yes():
            _label.text = "Confirm result: yes"

        def on_no():
            _label.text = "Confirm result: no"

        _ui.show_message_box(
            love,
            "Confirm",
            "Are you sure you want to continue?",
            show_cancel=True,
            on_confirm=on_yes,
            on_cancel=on_no,
            confirm_text="Confirm",
            cancel_text="Cancel",
        )

    row2_y = row1_y + input_h + row_gap
    action_h = 34.0
    row2 = root.add(
        love_gui.FlexLayout(
            love_gui.Rect(20, row2_y, 400, action_h),
            direction="row",
            spacing=20.0,
            justify_content="start",
            align_items="stretch",
        )
    )
    row2.add(love_gui.Button(love_gui.Rect(0, 0, 180, action_h), "Show notice", on_click=open_notice), basis=180.0)
    row2.add(love_gui.Button(love_gui.Rect(0, 0, 180, action_h), "Show confirm", on_click=open_confirm), basis=180.0)

    section_label_y = row2_y + action_h + 16.0
    root.add(love_gui.Label(love_gui.Rect(20, section_label_y, 360, 22), "ScrollView:"))

    scroll_panel_y = section_label_y + 28.0
    scroll_panel_h = max(180.0, root.rect.h - scroll_panel_y - 20.0)
    scroll_panel = root.add(love_gui.Panel(love_gui.Rect(20, scroll_panel_y, 420, scroll_panel_h)))
    scroll = scroll_panel.add(love_gui.ScrollView(love_gui.Rect(10, 10, 400, scroll_panel_h - 20)))

    y = 0.0
    for i in range(30):
        item = love_gui.Button(love_gui.Rect(0, y, 380, 32), f"Item {i + 1}")
        scroll.add(item)
        y += 38.0

    root.add(love_gui.Label(love_gui.Rect(470, section_label_y, 360, 22), "Layout demo:"))

    layout_demo = root.add(love_gui.Panel(love_gui.Rect(470, scroll_panel_y, 450, scroll_panel_h)))

    def set_flow_align(align: str):
        flow.align = align

    def on_flex_wrap(v: bool):
        flex.wrap = "wrap" if v else "nowrap"

    controls_h = 72.0
    controls = layout_demo.add(
        love_gui.FlexLayout(
            love_gui.Rect(12, 12, layout_demo.rect.w - 24, controls_h),
            direction="row",
            wrap="wrap",
            spacing=10.0,
            run_spacing=10.0,
            justify_content="start",
            align_items="stretch",
        )
    )
    controls.add(love_gui.Label(love_gui.Rect(0, 0, 0, 22), "Flow:"), basis=44.0)
    controls.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), "start", on_click=lambda: set_flow_align("start")), basis=72.0)
    controls.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), "center", on_click=lambda: set_flow_align("center")), basis=84.0)
    controls.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), "end", on_click=lambda: set_flow_align("end")), basis=70.0)
    controls.add(
        love_gui.CheckBox(love_gui.Rect(0, 0, 0, 34), "Flex wrap", checked=True, on_change=on_flex_wrap),
        basis=140.0,
    )

    columns_y = 12.0 + controls_h + 12.0
    columns_h = max(0.0, layout_demo.rect.h - columns_y - 12.0)
    gap = 12.0
    col_w = max(0.0, (layout_demo.rect.w - 24.0 - gap) * 0.5)

    flow_panel = layout_demo.add(love_gui.Panel(love_gui.Rect(12, columns_y, col_w, columns_h)))
    flex_panel = layout_demo.add(love_gui.Panel(love_gui.Rect(12 + col_w + gap, columns_y, col_w, columns_h)))

    flow_panel.add(love_gui.Label(love_gui.Rect(12, 10, col_w - 24, 22), "FlowLayout"))
    flow_view = flow_panel.add(love_gui.ScrollView(love_gui.Rect(12, 36, col_w - 24, max(0.0, columns_h - 48))))
    content_w = max(0.0, flow_view.rect.w - 14.0)
    flow = flow_view.add(love_gui.FlowLayout(love_gui.Rect(0, 0, content_w, 0), spacing=8.0, run_spacing=8.0, align="start"))
    for text in [
        "One",
        "Two",
        "Three",
        "Longer item",
        "XL",
        "Button",
        "Wrap",
        "Layout",
        "Python",
        "LOVE2D",
        "Tag",
        "Very long tag",
    ]:
        flow.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), text))

    flex_panel.add(love_gui.Label(love_gui.Rect(12, 10, col_w - 24, 22), "FlexLayout"))
    flex_view = flex_panel.add(love_gui.ScrollView(love_gui.Rect(12, 36, col_w - 24, max(0.0, columns_h - 48))))
    flex_content_w = max(0.0, flex_view.rect.w - 14.0)
    flex = flex_view.add(
        love_gui.FlexLayout(
            love_gui.Rect(0, 0, flex_content_w, 0),
            direction="row",
            wrap="wrap",
            spacing=8.0,
            run_spacing=8.0,
            justify_content="start",
            align_items="stretch",
        )
    )
    flex.add(
        love_gui.TextInput(love_gui.Rect(0, 0, 0, 34), text="", placeholder="Search..."),
        grow=1.0,
        basis=160.0,
        min_main=120.0,
    )
    flex.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), "Fixed"), shrink=0.0, basis=92.0)
    flex.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), "Min 80"), basis=96.0, min_main=80.0)
    flex.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), "Max 110"), basis=140.0, max_main=110.0)
    for i in range(1, 8):
        flex.add(love_gui.Button(love_gui.Rect(0, 0, 0, 34), f"Tag {i}"), basis=78.0, min_main=58.0)

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
