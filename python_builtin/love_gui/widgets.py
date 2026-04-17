from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

from .types import Constraints, Insets, Rect, Size


def _clamp(v: float, lo: float, hi: float) -> float:
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v


def _rects_intersect(a: Rect, b: Rect) -> bool:
    if a.w <= 0 or a.h <= 0 or b.w <= 0 or b.h <= 0:
        return False
    return not (a.right <= b.x or b.right <= a.x or a.bottom <= b.y or b.bottom <= a.y)


def _round_half_up(v: float) -> float:
    if v >= 0.0:
        return float(int(v + 0.5))
    return float(int(v - 0.5))


def _pixel_align_rect(r: Rect) -> Rect:
    x0 = _round_half_up(r.x)
    y0 = _round_half_up(r.y)
    x1 = _round_half_up(r.x + r.w)
    y1 = _round_half_up(r.y + r.h)
    return Rect(x0, y0, max(0.0, x1 - x0), max(0.0, y1 - y0))


def _push_scissor(love: Any, x: float, y: float, w: float, h: float) -> Any:
    prev = love.graphics.getScissor()
    ix = int(_round_half_up(x))
    iy = int(_round_half_up(y))
    iw = int(max(0.0, _round_half_up(w)))
    ih = int(max(0.0, _round_half_up(h)))
    if prev is None:
        love.graphics.setScissor(ix, iy, iw, ih)
    else:
        love.graphics.intersectScissor(ix, iy, iw, ih)
    return prev


def _pop_scissor(love: Any, prev: Any) -> None:
    if prev is None:
        love.graphics.setScissor()
        return
    love.graphics.setScissor(prev[0], prev[1], prev[2], prev[3])


class Widget:
    def __init__(self, rect: Rect) -> None:
        self.rect = rect
        self.parent: Optional["Container"] = None
        self.visible = True
        self.enabled = True
        self.focusable = False

        self._hovered = False
        self._pressed = False
        self._press_flash = 0.0

    def abs_rect(self) -> Rect:
        x = self.rect.x
        y = self.rect.y
        p = self.parent
        while p is not None:
            x += p.rect.x
            y += p.rect.y
            if isinstance(p, ScrollView):
                x -= p.scroll_x
                y -= p.scroll_y
            p = p.parent
        return _pixel_align_rect(Rect(x, y, self.rect.w, self.rect.h))

    def set_hovered(self, hovered: bool) -> None:
        self._hovered = hovered

    def set_pressed(self, pressed: bool) -> None:
        self._pressed = pressed
        if pressed:
            self._press_flash = max(self._press_flash, 0.06)

    def is_pressed_visual(self) -> bool:
        return self._pressed or self._press_flash > 0.0

    def hit_test(self, x: float, y: float) -> Optional["Widget"]:
        if not self.visible or not self.enabled:
            return None
        if self.abs_rect().contains(x, y):
            return self
        return None

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        return constraints.constrain(Size(float(self.rect.w), float(self.rect.h)))

    def layout(self, rect: Rect) -> None:
        self.rect = rect

    def layout_tree(self, theme: Any) -> None:
        return None

    def update(self, dt: float) -> None:
        self._press_flash = max(0.0, self._press_flash - float(dt))
        return None

    def draw(self, love: Any, theme: Any) -> None:
        return None

    def on_mousepressed(self, x: float, y: float, button: int, presses: int) -> bool:
        return False

    def on_mousereleased(self, x: float, y: float, button: int, presses: int) -> bool:
        return False

    def on_mousemoved(self, x: float, y: float, dx: float, dy: float) -> bool:
        return False

    def on_wheelmoved(self, x: float, y: float) -> bool:
        return False

    def on_keypressed(self, key: str, scancode: Any, isrepeat: bool) -> bool:
        return False

    def on_textinput(self, text: str) -> bool:
        return False


class Container(Widget):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)
        self.children: list[Widget] = []

    def add(self, child: Widget) -> Widget:
        child.parent = self
        self.children.append(child)
        return child

    def hit_test(self, x: float, y: float) -> Optional[Widget]:
        if not self.visible or not self.enabled:
            return None
        for child in reversed(self.children):
            hit = child.hit_test(x, y)
            if hit is not None:
                return hit
        if self.abs_rect().contains(x, y):
            return self
        return None

    def update(self, dt: float) -> None:
        super().update(dt)
        for child in self.children:
            child.update(dt)

    def draw(self, love: Any, theme: Any) -> None:
        for child in self.children:
            if child.visible:
                child.draw(love, theme)

    def layout_tree(self, theme: Any) -> None:
        for child in self.children:
            child.layout_tree(theme)


class Panel(Container):
    def __init__(self, rect: Rect, padding: Insets | None = None) -> None:
        super().__init__(rect)
        self.padding = padding if padding is not None else Insets.all(10)

    def draw(self, love: Any, theme: Any) -> None:
        r = self.abs_rect()
        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        theme.panel.draw(love, r.x, r.y, r.w, r.h)
        super().draw(love, theme)


class Label(Widget):
    def __init__(self, rect: Rect, text: str) -> None:
        super().__init__(rect)
        self.text = text

    def draw(self, love: Any, theme: Any) -> None:
        r = self.abs_rect()
        love.graphics.setColor(*theme.text_color)
        love.graphics.print(self.text, _round_half_up(r.x), _round_half_up(r.y))

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        font = getattr(theme, "font", None)
        if font is None:
            return super().measure(theme, constraints)
        w = float(font.getWidth(self.text)) if self.text else 0.0
        h = float(font.getHeight())
        return constraints.constrain(Size(w, h))


class Button(Widget):
    def __init__(self, rect: Rect, text: str, on_click: Optional[Callable[[], None]] = None) -> None:
        super().__init__(rect)
        self.text = text
        self.on_click = on_click
        self._pressed_inside = False

    def draw(self, love: Any, theme: Any) -> None:
        r = self.abs_rect()
        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        if self.is_pressed_visual() and self._hovered:
            theme.button_pressed.draw(love, r.x, r.y, r.w, r.h)
        elif self._hovered:
            theme.button_hover.draw(love, r.x, r.y, r.w, r.h)
        else:
            theme.button.draw(love, r.x, r.y, r.w, r.h)

        love.graphics.setColor(*theme.text_color)
        tw = float(theme.font.getWidth(self.text))
        th = float(theme.font.getHeight())
        tx = r.x + max(6.0, (r.w - tw) * 0.5)
        ty = r.y + max(4.0, (r.h - th) * 0.5)
        love.graphics.print(self.text, _round_half_up(tx), _round_half_up(ty))

    def on_mousepressed(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        self.set_pressed(True)
        self._pressed_inside = True
        return True

    def on_mousereleased(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        was_pressed = self._pressed and self._pressed_inside
        self.set_pressed(False)
        self._pressed_inside = False
        if was_pressed and self._hovered and self.on_click is not None:
            self.on_click()
        return True

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        font = getattr(theme, "font", None)
        if font is None:
            return super().measure(theme, constraints)
        tw = float(font.getWidth(self.text)) if self.text else 0.0
        th = float(font.getHeight())
        w = tw + 24.0
        h = th + 16.0
        return constraints.constrain(Size(w, h))


class CheckBox(Widget):
    def __init__(
        self,
        rect: Rect,
        label: str,
        checked: bool = False,
        on_change: Optional[Callable[[bool], None]] = None,
    ) -> None:
        super().__init__(rect)
        self.focusable = True
        self.label = label
        self.checked = bool(checked)
        self.on_change = on_change
        self._pressed_inside = False

    @staticmethod
    def preferred_height(theme: Any, min_height: float = 0.0) -> float:
        return max(float(min_height), float(theme.font.getHeight()) + 8.0)

    def _toggle(self) -> None:
        self.checked = not self.checked
        if self.on_change is not None:
            self.on_change(self.checked)

    def draw(self, love: Any, theme: Any) -> None:
        r = self.abs_rect()
        box = min(22.0, r.h)
        box_r = _pixel_align_rect(Rect(r.x, r.y + (r.h - box) * 0.5, box, box))

        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        if self.is_pressed_visual() and self._hovered:
            theme.button_pressed.draw(love, box_r.x, box_r.y, box_r.w, box_r.h)
        elif self._hovered:
            theme.button_hover.draw(love, box_r.x, box_r.y, box_r.w, box_r.h)
        else:
            theme.input.draw(love, box_r.x, box_r.y, box_r.w, box_r.h)

        if self.checked:
            inner = box_r.inset(Insets.all(6.0))
            love.graphics.setColor(*theme.accent)
            love.graphics.rectangle(
                "fill",
                _round_half_up(inner.x),
                _round_half_up(inner.y),
                max(1.0, _round_half_up(inner.w)),
                max(1.0, _round_half_up(inner.h)),
            )

        love.graphics.setColor(*theme.text_color)
        tx = box_r.right + 10.0
        ty = r.y + max(0.0, (r.h - float(theme.font.getHeight())) * 0.5)
        love.graphics.print(self.label, _round_half_up(tx), _round_half_up(ty))

    def on_mousepressed(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        self.set_pressed(True)
        self._pressed_inside = True
        return True

    def on_mousereleased(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        was_pressed = self._pressed and self._pressed_inside
        self.set_pressed(False)
        self._pressed_inside = False
        if was_pressed and self._hovered:
            self._toggle()
        return True

    def on_keypressed(self, key: str, scancode: Any, isrepeat: bool) -> bool:
        if key in ("space", "return", "enter", "kpenter"):
            self._toggle()
            return True
        return False

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        font = getattr(theme, "font", None)
        if font is None:
            return super().measure(theme, constraints)
        th = float(font.getHeight())
        h = max(22.0, th + 8.0)
        tw = float(font.getWidth(self.label)) if self.label else 0.0
        w = 22.0 + 10.0 + tw
        return constraints.constrain(Size(w, h))


class ProgressBar(Widget):
    def __init__(self, rect: Rect, value: float = 0.0) -> None:
        super().__init__(rect)
        self.value = _clamp(value, 0.0, 1.0)

    def draw(self, love: Any, theme: Any) -> None:
        r = self.abs_rect()
        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        theme.track.draw(love, r.x, r.y, r.w, r.h)
        inner = r.inset(theme.track.insets)
        fill_w = max(0.0, inner.w * _clamp(self.value, 0.0, 1.0))
        if fill_w > 0:
            theme.fill.draw(love, inner.x, inner.y, fill_w, inner.h)

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        h = 28.0
        w = 160.0
        return constraints.constrain(Size(w, h))


class Slider(Widget):
    def __init__(self, rect: Rect, value: float = 0.0, on_change: Optional[Callable[[float], None]] = None) -> None:
        super().__init__(rect)
        self.value = _clamp(value, 0.0, 1.0)
        self.on_change = on_change
        self._dragging = False

    def _knob_rect(self) -> Rect:
        r = self.abs_rect()
        knob_w = min(26.0, r.w)
        knob_h = min(r.h, 26.0)
        x = r.x + (r.w - knob_w) * self.value
        y = r.y + (r.h - knob_h) * 0.5
        return _pixel_align_rect(Rect(x, y, knob_w, knob_h))

    def draw(self, love: Any, theme: Any) -> None:
        r = self.abs_rect()
        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        theme.track.draw(love, r.x, r.y, r.w, r.h)
        inner = r.inset(theme.track.insets)
        fill_w = max(0.0, inner.w * _clamp(self.value, 0.0, 1.0))
        if fill_w > 0:
            theme.fill.draw(love, inner.x, inner.y, fill_w, inner.h)
        kr = self._knob_rect()
        if self._pressed:
            theme.button_pressed.draw(love, kr.x, kr.y, kr.w, kr.h)
        elif self._hovered:
            theme.button_hover.draw(love, kr.x, kr.y, kr.w, kr.h)
        else:
            theme.button.draw(love, kr.x, kr.y, kr.w, kr.h)

    def _set_from_mouse(self, x: float) -> None:
        r = self.abs_rect()
        if r.w <= 1:
            return
        knob_w = min(26.0, r.w)
        v = (x - r.x - knob_w * 0.5) / max(1.0, (r.w - knob_w))
        v = _clamp(v, 0.0, 1.0)
        if v != self.value:
            self.value = v
            if self.on_change is not None:
                self.on_change(v)

    def on_mousepressed(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        self.set_pressed(True)
        self._dragging = True
        self._set_from_mouse(x)
        return True

    def on_mousemoved(self, x: float, y: float, dx: float, dy: float) -> bool:
        if self._dragging:
            self._set_from_mouse(x)
            return True
        return False

    def on_mousereleased(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        self.set_pressed(False)
        self._dragging = False
        return True

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        h = 28.0
        w = 200.0
        return constraints.constrain(Size(w, h))


class TextInput(Widget):
    def __init__(self, rect: Rect, text: str = "", placeholder: str = "") -> None:
        super().__init__(rect)
        self.focusable = True
        self.text = text
        self.placeholder = placeholder
        self.cursor = len(text)
        self._focused = False
        self._scroll_x = 0.0
        self._last_font: Any | None = None
        self._last_inner: Rect | None = None
        self._last_pad_x: float = 0.0

    @staticmethod
    def preferred_height(theme: Any, min_height: float = 0.0) -> float:
        font_h = float(theme.font.getHeight())
        insets_h = float(theme.input.insets.top) + float(theme.input.insets.bottom)
        inner_pad = 6.0
        return max(float(min_height), font_h + insets_h + inner_pad * 2.0)

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        font = getattr(theme, "font", None)
        if font is None:
            return super().measure(theme, constraints)
        insets = getattr(getattr(theme, "input", None), "insets", Insets.all(0.0))
        pad_x = 10.0
        content = self.text if self.text else self.placeholder
        tw = float(font.getWidth(content)) if content else 0.0
        w = tw + pad_x * 2.0 + float(insets.left) + float(insets.right)
        h = float(self.preferred_height(theme, min_height=0.0))
        w = max(120.0, w)
        return constraints.constrain(Size(w, h))

    def set_focused(self, focused: bool) -> None:
        self._focused = focused
        if focused:
            self.cursor = _clamp(self.cursor, 0, len(self.text))
        if not focused and not self.text:
            self._scroll_x = 0.0

    def _cursor_index_from_x(self, font: Any, x: float) -> int:
        if not self.text:
            return 0
        pos = 0.0
        best_i = 0
        target = max(0.0, x)
        for i, ch in enumerate(self.text):
            w = float(font.getWidth(ch))
            if pos + w * 0.5 >= target:
                best_i = i
                break
            pos += w
            best_i = i + 1
        return int(_clamp(best_i, 0, len(self.text)))

    def _cursor_x(self, font: Any) -> float:
        if self.cursor <= 0:
            return 0.0
        s = self.text[: self.cursor]
        return float(font.getWidth(s))

    def draw(self, love: Any, theme: Any) -> None:
        r = self.abs_rect()
        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        theme.input.draw(love, r.x, r.y, r.w, r.h)

        pad_x = 10.0
        inner = r.inset(theme.input.insets)
        self._last_font = theme.font
        self._last_inner = inner
        self._last_pad_x = pad_x
        font_h = float(theme.font.getHeight())
        if hasattr(theme.font, "getAscent") and hasattr(theme.font, "getDescent"):
            ascent = float(theme.font.getAscent())
            descent = float(theme.font.getDescent())
            line_h = max(0.0, ascent - descent)
        else:
            line_h = font_h
        pad_y = max(0.0, (inner.h - line_h) * 0.5)
        text_y = inner.y + pad_y
        prev_scissor = _push_scissor(love, inner.x, inner.y, inner.w, inner.h)

        avail = max(0.0, inner.w - pad_x * 2.0)
        text_w = float(theme.font.getWidth(self.text)) if self.text else 0.0
        cursor_px = float(theme.font.getWidth(self.text[: self.cursor])) if self.text else 0.0

        if self._focused:
            if cursor_px - self._scroll_x > avail:
                self._scroll_x = cursor_px - avail + 2.0
            if cursor_px - self._scroll_x < 0.0:
                self._scroll_x = max(0.0, cursor_px - 2.0)
            self._scroll_x = _clamp(self._scroll_x, 0.0, max(0.0, text_w - avail))
        else:
            self._scroll_x = max(0.0, text_w - avail)

        if self.text:
            love.graphics.setColor(*theme.text_color)
            love.graphics.print(
                self.text,
                _round_half_up(inner.x + pad_x - self._scroll_x),
                _round_half_up(text_y),
            )
        elif not self._focused:
            self._scroll_x = 0.0
            love.graphics.setColor(*theme.text_muted)
            love.graphics.print(
                self.placeholder,
                _round_half_up(inner.x + pad_x),
                _round_half_up(text_y),
            )

        if self._focused:
            t = float(love.timer.getTime())
            on = int(t * 2) % 2 == 0
            if on:
                cx = inner.x + pad_x - self._scroll_x + cursor_px
                love.graphics.setColor(*theme.text_color)
                cursor_h = min(inner.h, max(1.0, line_h))
                love.graphics.rectangle(
                    "fill",
                    _round_half_up(cx),
                    _round_half_up(text_y),
                    2,
                    cursor_h,
                )

        _pop_scissor(love, prev_scissor)

    def on_mousepressed(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        if self._last_font is None or self._last_inner is None:
            self.cursor = len(self.text)
            return True

        inner = self._last_inner
        target_x = x - (inner.x + self._last_pad_x) + self._scroll_x
        self.cursor = self._cursor_index_from_x(self._last_font, target_x)
        return True

    def on_keypressed(self, key: str, scancode: Any, isrepeat: bool) -> bool:
        if not self._focused:
            return False
        if key == "backspace":
            if self.cursor > 0 and self.text:
                self.text = self.text[: self.cursor - 1] + self.text[self.cursor :]
                self.cursor -= 1
            return True
        if key == "delete":
            if self.cursor < len(self.text):
                self.text = self.text[: self.cursor] + self.text[self.cursor + 1 :]
            return True
        if key == "left":
            self.cursor = max(0, self.cursor - 1)
            return True
        if key == "right":
            self.cursor = min(len(self.text), self.cursor + 1)
            return True
        if key == "home":
            self.cursor = 0
            return True
        if key == "end":
            self.cursor = len(self.text)
            return True
        return False

    def on_textinput(self, text: str) -> bool:
        if not self._focused:
            return False
        if not text:
            return False
        self.text = self.text[: self.cursor] + text + self.text[self.cursor :]
        self.cursor += len(text)
        return True


@dataclass(frozen=True)
class PopupMenuItem:
    label: str
    on_select: Callable[[], None]
    enabled: bool = True


def _wrap_text(font: Any, text: str, max_width: float) -> list[str]:
    if max_width <= 0.0:
        return [text] if text else [""]
    out: list[str] = []
    for para in text.split("\n"):
        words = para.split(" ")
        line = ""
        for w in words:
            if line == "":
                candidate = w
            else:
                candidate = f"{line} {w}"

            if float(font.getWidth(candidate)) <= max_width:
                line = candidate
                continue

            if line:
                out.append(line)
                line = ""

            if float(font.getWidth(w)) <= max_width or not w:
                line = w
                continue

            chunk = ""
            for ch in w:
                cand = f"{chunk}{ch}"
                if float(font.getWidth(cand)) <= max_width or not chunk:
                    chunk = cand
                else:
                    out.append(chunk)
                    chunk = ch
            line = chunk

        out.append(line)
    if not out:
        out.append("")
    return out


class MessageBox(Widget):
    def __init__(
        self,
        title: str,
        message: str,
        *,
        ok_text: str = "OK",
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        show_cancel: bool = False,
        on_confirm: Optional[Callable[[], None]] = None,
        on_cancel: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(Rect(0.0, 0.0, 0.0, 0.0))
        self.title = title
        self.message = message
        self.ok_text = ok_text
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text
        self.show_cancel = bool(show_cancel)
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        self.close_requested = False
        self._result: str | None = None
        self._lines: list[str] = []
        self._btn_rects: list[Rect] = []
        self._btn_labels: list[str] = []
        self._hover_btn: int | None = None
        self._pressed_btn: int | None = None

    def _set_result(self, result: str) -> None:
        self._result = result
        if result == "confirm":
            if self.on_confirm is not None:
                self.on_confirm()
        elif result == "cancel":
            if self.on_cancel is not None:
                self.on_cancel()
        self.close_requested = True

    def _layout(self, love: Any, theme: Any) -> None:
        pad = 16.0
        title_gap = 10.0
        msg_gap = 14.0
        btn_h = 34.0
        btn_w = 120.0
        btn_gap = 10.0
        min_w = 320.0

        sw = float(love.graphics.getWidth())
        sh = float(love.graphics.getHeight())
        max_w = max(240.0, sw - 60.0)
        content_max_w = max(120.0, max_w - pad * 2.0)

        title_w = float(theme.font.getWidth(self.title)) if self.title else 0.0
        self._lines = _wrap_text(theme.font, self.message, content_max_w)
        msg_w = 0.0
        for ln in self._lines:
            msg_w = max(msg_w, float(theme.font.getWidth(ln)))

        btn_count = 2 if self.show_cancel else 1
        btn_row_w = btn_w * btn_count + btn_gap * (btn_count - 1)
        w = max(min_w, title_w + pad * 2.0, msg_w + pad * 2.0, btn_row_w + pad * 2.0)
        w = min(w, max_w)

        line_h = float(theme.font.getHeight())
        title_h = line_h if self.title else 0.0
        msg_h = line_h * float(len(self._lines))
        h = pad * 2.0 + title_h + (title_gap if self.title and self.message else 0.0) + msg_h + msg_gap + btn_h

        x = (sw - w) * 0.5
        y = (sh - h) * 0.5
        self.rect = _pixel_align_rect(Rect(x, y, w, h))

        r = self.abs_rect()
        btn_y = r.bottom - pad - btn_h
        row_total_w = btn_row_w
        start_x = r.x + (r.w - row_total_w) * 0.5

        self._btn_rects = []
        self._btn_labels = []
        if self.show_cancel:
            self._btn_rects.append(_pixel_align_rect(Rect(start_x, btn_y, btn_w, btn_h)))
            self._btn_labels.append(self.cancel_text)
            self._btn_rects.append(_pixel_align_rect(Rect(start_x + btn_w + btn_gap, btn_y, btn_w, btn_h)))
            self._btn_labels.append(self.confirm_text)
        else:
            self._btn_rects.append(_pixel_align_rect(Rect(start_x, btn_y, btn_w, btn_h)))
            self._btn_labels.append(self.ok_text)

    def _btn_index_at(self, x: float, y: float) -> int | None:
        for i, r in enumerate(self._btn_rects):
            if r.contains(x, y):
                return i
        return None

    def _outside_close(self) -> None:
        if self.show_cancel:
            self._set_result("cancel")
            return
        self._set_result("confirm")

    def draw(self, love: Any, theme: Any) -> None:
        self._layout(love, theme)
        r = self.abs_rect()

        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        theme.panel.draw(love, r.x, r.y, r.w, r.h)

        pad = 16.0
        y = r.y + pad
        if self.title:
            love.graphics.setColor(*theme.text_color)
            love.graphics.print(self.title, _round_half_up(r.x + pad), _round_half_up(y))
            y += float(theme.font.getHeight()) + 10.0

        love.graphics.setColor(*theme.text_color)
        for ln in self._lines:
            love.graphics.print(ln, _round_half_up(r.x + pad), _round_half_up(y))
            y += float(theme.font.getHeight())

        for i, br in enumerate(self._btn_rects):
            love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
            if self._pressed_btn == i and self._hover_btn == i:
                theme.button_pressed.draw(love, br.x, br.y, br.w, br.h)
            elif self._hover_btn == i:
                theme.button_hover.draw(love, br.x, br.y, br.w, br.h)
            else:
                theme.button.draw(love, br.x, br.y, br.w, br.h)

            label = self._btn_labels[i]
            love.graphics.setColor(*theme.text_color)
            tw = float(theme.font.getWidth(label))
            th = float(theme.font.getHeight())
            tx = br.x + max(6.0, (br.w - tw) * 0.5)
            ty = br.y + max(4.0, (br.h - th) * 0.5)
            love.graphics.print(label, _round_half_up(tx), _round_half_up(ty))

    def on_mousemoved(self, x: float, y: float, dx: float, dy: float) -> bool:
        self._hover_btn = self._btn_index_at(x, y)
        return True

    def on_mousepressed(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return True
        self._pressed_btn = self._btn_index_at(x, y)
        return True

    def on_mousereleased(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            self._pressed_btn = None
            return True

        idx = self._btn_index_at(x, y)
        pressed = self._pressed_btn
        self._pressed_btn = None
        if idx is None or pressed is None or idx != pressed:
            return True

        if self.show_cancel:
            if idx == 0:
                self._set_result("cancel")
            else:
                self._set_result("confirm")
            return True

        self._set_result("confirm")
        return True

    def on_keypressed(self, key: str, scancode: Any, isrepeat: bool) -> bool:
        if key == "escape":
            self._outside_close()
            return True
        if key in ("return", "enter", "kpenter"):
            self._set_result("confirm")
            return True
        return False


class PopupMenu(Widget):
    def __init__(self, x: float, y: float, items: list[PopupMenuItem], min_width: float = 140.0) -> None:
        super().__init__(Rect(float(x), float(y), 0.0, 0.0))
        self.items = items
        self.min_width = float(min_width)
        self._hover_index: int | None = None
        self._pressed_index: int | None = None
        self._item_rects: list[Rect] = []
        self._last_font: Any | None = None
        self.close_requested = False

    def _layout(self, theme: Any) -> None:
        pad = 6.0
        row_h = max(22.0, float(theme.font.getHeight()) + 8.0)
        max_w = 0.0
        for it in self.items:
            max_w = max(max_w, float(theme.font.getWidth(it.label)))
        w = max(self.min_width, max_w + pad * 2.0)
        h = pad * 2.0 + row_h * float(len(self.items))
        self.rect = Rect(self.rect.x, self.rect.y, w, h)

        r = self.abs_rect()
        inner = r.inset(theme.panel.insets)
        x0 = inner.x
        y0 = inner.y
        iw = inner.w
        self._item_rects = []
        for i in range(len(self.items)):
            self._item_rects.append(Rect(x0, y0 + row_h * i, iw, row_h))

    def hit_test(self, x: float, y: float) -> Optional["Widget"]:
        if not self.visible or not self.enabled:
            return None
        if self.abs_rect().contains(x, y):
            return self
        return None

    def draw(self, love: Any, theme: Any) -> None:
        self._last_font = theme.font
        self._layout(theme)
        r = self.abs_rect()

        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        theme.panel.draw(love, r.x, r.y, r.w, r.h)

        pad_x = 10.0
        for i, it in enumerate(self.items):
            ir = self._item_rects[i]
            if self._hover_index == i and it.enabled:
                theme.button_hover.draw(love, ir.x, ir.y, ir.w, ir.h)
            if self._pressed_index == i and it.enabled:
                theme.button_pressed.draw(love, ir.x, ir.y, ir.w, ir.h)

            love.graphics.setColor(*((theme.text_color if it.enabled else theme.text_muted)))
            tx = ir.x + pad_x
            ty = ir.y + max(0.0, (ir.h - float(theme.font.getHeight())) * 0.5)
            love.graphics.print(it.label, _round_half_up(tx), _round_half_up(ty))

    def _index_at(self, x: float, y: float) -> int | None:
        if not self._item_rects:
            return None
        for i, r in enumerate(self._item_rects):
            if r.contains(x, y):
                return i
        return None

    def on_mousemoved(self, x: float, y: float, dx: float, dy: float) -> bool:
        idx = self._index_at(x, y)
        self._hover_index = idx
        return True

    def on_mousepressed(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            self.close_requested = True
            return True
        idx = self._index_at(x, y)
        self._pressed_index = idx
        return True

    def on_mousereleased(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            self._pressed_index = None
            return True
        idx = self._index_at(x, y)
        pressed = self._pressed_index
        self._pressed_index = None
        if idx is None or pressed is None or idx != pressed:
            return True
        it = self.items[idx]
        if not it.enabled:
            return True
        it.on_select()
        self.close_requested = True
        return True

    def on_keypressed(self, key: str, scancode: Any, isrepeat: bool) -> bool:
        if key == "escape":
            self.close_requested = True
            return True
        return False


class ScrollView(Container):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)
        self.scroll_x = 0.0
        self.scroll_y = 0.0
        self.scroll_speed = 38.0
        self.scrollbar_width = 12.0
        self._sb_hover = False
        self._sb_dragging = False
        self._sb_drag_offset = 0.0
        self._sb_thumb_y = 0.0
        self._sb_thumb_h = 0.0
        self._sb_track_rect: Rect | None = None

    def content_bounds(self) -> Rect:
        if not self.children:
            return Rect(0.0, 0.0, 0.0, 0.0)
        min_x = min(c.rect.x for c in self.children)
        min_y = min(c.rect.y for c in self.children)
        max_r = max(c.rect.x + c.rect.w for c in self.children)
        max_b = max(c.rect.y + c.rect.h for c in self.children)
        return Rect(min_x, min_y, max(0.0, max_r - min_x), max(0.0, max_b - min_y))

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        w = max(160.0, float(self.rect.w))
        h = max(120.0, float(self.rect.h))
        return constraints.constrain(Size(w, h))

    def _apply_scroll_limits(self) -> None:
        bounds = self.content_bounds()
        max_x = max(0.0, bounds.w - self.rect.w)
        max_y = max(0.0, bounds.h - self.rect.h)
        self.scroll_x = _clamp(self.scroll_x, 0.0, max_x)
        self.scroll_y = _clamp(self.scroll_y, 0.0, max_y)

    def _update_scrollbar_geometry(self) -> None:
        view = self.abs_rect()
        bounds = self.content_bounds()
        max_y = max(0.0, bounds.h - self.rect.h)
        if max_y <= 0.0 or view.h <= 0.0:
            self._sb_track_rect = None
            self._sb_thumb_y = 0.0
            self._sb_thumb_h = 0.0
            return

        w = min(self.scrollbar_width, view.w)
        track = Rect(view.x + view.w - w, view.y, w, view.h)
        self._sb_track_rect = track

        thumb_h = max(18.0, track.h * (track.h / max(track.h, bounds.h)))
        thumb_h = min(thumb_h, track.h)
        travel = max(0.0, track.h - thumb_h)
        t = 0.0 if max_y <= 0.0 else _clamp(self.scroll_y / max_y, 0.0, 1.0)
        self._sb_thumb_h = thumb_h
        self._sb_thumb_y = track.y + travel * t

    def _is_over_scrollbar(self, x: float, y: float) -> bool:
        self._update_scrollbar_geometry()
        if self._sb_track_rect is None:
            return False
        return self._sb_track_rect.contains(x, y)

    def _is_over_thumb(self, x: float, y: float) -> bool:
        if self._sb_track_rect is None or self._sb_thumb_h <= 0.0:
            return False
        thumb = Rect(self._sb_track_rect.x, self._sb_thumb_y, self._sb_track_rect.w, self._sb_thumb_h)
        return thumb.contains(x, y)

    def on_wheelmoved(self, x: float, y: float) -> bool:
        bounds = self.content_bounds()
        if bounds.h <= self.rect.h + 0.5:
            return False
        self.scroll_y -= float(y) * self.scroll_speed
        self._apply_scroll_limits()
        return True

    def on_mousepressed(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        if not self._is_over_scrollbar(x, y):
            return False

        if self._is_over_thumb(x, y):
            self._sb_dragging = True
            self._sb_drag_offset = y - self._sb_thumb_y
            self.set_pressed(True)
            return True

        track = self._sb_track_rect
        if track is None:
            return False

        bounds = self.content_bounds()
        max_y = max(0.0, bounds.h - self.rect.h)
        travel = max(0.0, track.h - self._sb_thumb_h)
        if travel <= 0.0 or max_y <= 0.0:
            return True

        click_t = (y - track.y - self._sb_thumb_h * 0.5) / travel
        self.scroll_y = _clamp(click_t, 0.0, 1.0) * max_y
        self._apply_scroll_limits()
        self.set_pressed(True)
        return True

    def on_mousemoved(self, x: float, y: float, dx: float, dy: float) -> bool:
        self._sb_hover = self._is_over_scrollbar(x, y)
        if not self._sb_dragging:
            return False

        track = self._sb_track_rect
        if track is None:
            return True

        bounds = self.content_bounds()
        max_y = max(0.0, bounds.h - self.rect.h)
        travel = max(0.0, track.h - self._sb_thumb_h)
        if travel <= 0.0 or max_y <= 0.0:
            return True

        t = (y - track.y - self._sb_drag_offset) / travel
        self.scroll_y = _clamp(t, 0.0, 1.0) * max_y
        self._apply_scroll_limits()
        return True

    def on_mousereleased(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        if self._sb_dragging or self._pressed:
            self._sb_dragging = False
            self.set_pressed(False)
            return True
        return False

    def hit_test(self, x: float, y: float) -> Optional[Widget]:
        if not self.visible or not self.enabled:
            return None
        if not self.abs_rect().contains(x, y):
            return None
        if self._is_over_scrollbar(x, y):
            return self
        for child in reversed(self.children):
            hit = child.hit_test(x, y)
            if hit is not None:
                return hit
        return self

    def draw(self, love: Any, theme: Any) -> None:
        view = self.abs_rect()
        prev_scissor = _push_scissor(love, view.x, view.y, view.w, view.h)
        for child in self.children:
            if not child.visible:
                continue
            cr = child.abs_rect()
            if _rects_intersect(cr, view):
                child.draw(love, theme)
        _pop_scissor(love, prev_scissor)

        self._update_scrollbar_geometry()
        track = self._sb_track_rect
        if track is None:
            return

        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        theme.track.draw(love, track.x, track.y, track.w, track.h)

        if self._sb_thumb_h > 0.0:
            thumb = Rect(track.x, self._sb_thumb_y, track.w, self._sb_thumb_h)
            if self._sb_dragging:
                theme.button_pressed.draw(love, thumb.x, thumb.y, thumb.w, thumb.h)
            elif self._sb_hover:
                theme.button_hover.draw(love, thumb.x, thumb.y, thumb.w, thumb.h)
            else:
                theme.button.draw(love, thumb.x, thumb.y, thumb.w, thumb.h)


class VBox(Container):
    def __init__(self, rect: Rect, spacing: float = 8.0, padding: Insets | None = None, auto_layout: bool = False) -> None:
        super().__init__(rect)
        self.spacing = spacing
        self.padding = padding if padding is not None else Insets.all(0.0)
        self.auto_layout = bool(auto_layout)

    def layout(self, theme: Any) -> None:
        avail_w = max(0.0, self.rect.w - self.padding.left - self.padding.right)
        y = self.padding.top
        for child in self.children:
            sz = child.measure(theme, Constraints(max_w=avail_w))
            child.rect.x = self.padding.left
            child.rect.y = y
            child.rect.w = avail_w
            child.rect.h = sz.h
            y += sz.h + self.spacing

    def layout_tree(self, theme: Any) -> None:
        if self.auto_layout:
            self.layout(theme)
        super().layout_tree(theme)

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        avail_w = constraints.max_w if constraints.max_w is not None else float(self.rect.w)
        avail_w = max(0.0, avail_w - self.padding.left - self.padding.right)
        y = self.padding.top + self.padding.bottom
        w = 0.0
        for i, child in enumerate(self.children):
            sz = child.measure(theme, Constraints(max_w=avail_w))
            w = max(w, sz.w)
            y += sz.h
            if i != len(self.children) - 1:
                y += self.spacing
        w += self.padding.left + self.padding.right
        return constraints.constrain(Size(w, y))


class HBox(Container):
    def __init__(self, rect: Rect, spacing: float = 8.0, padding: Insets | None = None, auto_layout: bool = False) -> None:
        super().__init__(rect)
        self.spacing = spacing
        self.padding = padding if padding is not None else Insets.all(0.0)
        self.auto_layout = bool(auto_layout)

    def layout(self, theme: Any) -> None:
        avail_h = max(0.0, self.rect.h - self.padding.top - self.padding.bottom)
        x = self.padding.left
        for child in self.children:
            sz = child.measure(theme, Constraints(max_h=avail_h))
            child.rect.x = x
            child.rect.y = self.padding.top
            child.rect.w = sz.w
            child.rect.h = avail_h
            x += sz.w + self.spacing

    def layout_tree(self, theme: Any) -> None:
        if self.auto_layout:
            self.layout(theme)
        super().layout_tree(theme)

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        avail_h = constraints.max_h if constraints.max_h is not None else float(self.rect.h)
        avail_h = max(0.0, avail_h - self.padding.top - self.padding.bottom)
        x = self.padding.left + self.padding.right
        h = 0.0
        for i, child in enumerate(self.children):
            sz = child.measure(theme, Constraints(max_h=avail_h))
            h = max(h, sz.h)
            x += sz.w
            if i != len(self.children) - 1:
                x += self.spacing
        h += self.padding.top + self.padding.bottom
        return constraints.constrain(Size(x, h))


class FlowLayout(Container):
    def __init__(
        self,
        rect: Rect,
        spacing: float = 8.0,
        run_spacing: float = 8.0,
        padding: Insets | None = None,
        align: str = "start",
        auto_layout: bool = True,
    ) -> None:
        super().__init__(rect)
        self.spacing = float(spacing)
        self.run_spacing = float(run_spacing)
        self.padding = padding if padding is not None else Insets.all(0.0)
        self.align = align
        self.auto_layout = bool(auto_layout)

    def layout(self, theme: Any) -> None:
        avail_w = max(0.0, self.rect.w - self.padding.left - self.padding.right)
        x0 = self.padding.left
        constraints = Constraints(max_w=avail_w)

        lines: list[list[Widget]] = []
        line: list[Widget] = []
        line_w = 0.0
        line_h = 0.0
        sizes: dict[Widget, Size] = {}

        for child in self.children:
            sz = child.measure(theme, constraints)
            sizes[child] = sz
            add_w = sz.w if not line else sz.w + self.spacing
            if line and line_w + add_w > avail_w + 0.01:
                lines.append(line)
                line = []
                line_w = 0.0
                line_h = 0.0

            if line:
                line_w += self.spacing
            line.append(child)
            line_w += sz.w
            line_h = max(line_h, sz.h)

        if line:
            lines.append(line)

        y = self.padding.top
        for ln in lines:
            ln_w = 0.0
            ln_h = 0.0
            for i, child in enumerate(ln):
                sz = sizes.get(child, Size(float(child.rect.w), float(child.rect.h)))
                if i:
                    ln_w += self.spacing
                ln_w += sz.w
                ln_h = max(ln_h, sz.h)

            if self.align == "center":
                x = x0 + max(0.0, (avail_w - ln_w) * 0.5)
            elif self.align == "end":
                x = x0 + max(0.0, avail_w - ln_w)
            else:
                x = x0

            for child in ln:
                sz = sizes.get(child, Size(float(child.rect.w), float(child.rect.h)))
                child.rect.x = x
                child.rect.y = y
                child.rect.w = sz.w
                child.rect.h = sz.h
                x += sz.w + self.spacing
            y += ln_h + self.run_spacing

    def layout_tree(self, theme: Any) -> None:
        if self.auto_layout:
            self.layout(theme)
        super().layout_tree(theme)

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        max_w = constraints.max_w
        if max_w is None:
            w = self.padding.left + self.padding.right
            h = self.padding.top + self.padding.bottom
            line_h = 0.0
            for i, child in enumerate(self.children):
                sz = child.measure(theme, Constraints())
                w += sz.w
                if i != len(self.children) - 1:
                    w += self.spacing
                line_h = max(line_h, sz.h)
            h += line_h
            return constraints.constrain(Size(w, h))

        avail_w = max(0.0, float(max_w) - self.padding.left - self.padding.right)
        x = 0.0
        line_h = 0.0
        total_h = 0.0
        max_line_w = 0.0
        for child in self.children:
            sz = child.measure(theme, Constraints(max_w=avail_w))
            add = sz.w if x == 0.0 else sz.w + self.spacing
            if x > 0.0 and x + add > avail_w + 0.01:
                max_line_w = max(max_line_w, x)
                total_h += line_h + self.run_spacing
                x = 0.0
                line_h = 0.0
                add = sz.w
            x = x + add if x > 0.0 else sz.w
            line_h = max(line_h, sz.h)
        max_line_w = max(max_line_w, x)
        total_h += line_h
        w = max_line_w + self.padding.left + self.padding.right
        h = total_h + self.padding.top + self.padding.bottom
        return constraints.constrain(Size(w, h))


@dataclass(frozen=True)
class FlexItem:
    grow: float = 0.0
    shrink: float = 1.0
    basis: float | None = None
    align: str | None = None
    min_main: float | None = None
    max_main: float | None = None


class FlexLayout(Container):
    def __init__(
        self,
        rect: Rect,
        *,
        direction: str = "row",
        wrap: str = "nowrap",
        spacing: float = 8.0,
        run_spacing: float | None = None,
        padding: Insets | None = None,
        justify_content: str = "start",
        align_items: str = "stretch",
        auto_layout: bool = True,
    ) -> None:
        super().__init__(rect)
        self.direction = direction
        self.wrap = wrap
        self.spacing = float(spacing)
        self.run_spacing = float(self.spacing if run_spacing is None else run_spacing)
        self.padding = padding if padding is not None else Insets.all(0.0)
        self.justify_content = justify_content
        self.align_items = align_items
        self.auto_layout = bool(auto_layout)
        self._flex: dict[Widget, FlexItem] = {}

    def _gap_for_line(self, count: int) -> float:
        if count <= 1:
            return 0.0
        return self.spacing * float(count - 1)

    def _clamp_main(self, v: float, spec: FlexItem) -> float:
        out = max(0.0, float(v))
        if spec.min_main is not None:
            out = max(out, float(spec.min_main))
        if spec.max_main is not None:
            out = min(out, float(spec.max_main))
        return out

    def _solve_main_sizes(self, line: list[tuple[Widget, FlexItem, float]], main_avail: float) -> dict[Widget, float]:
        target = max(0.0, float(main_avail))
        target -= self._gap_for_line(len(line))
        target = max(0.0, target)

        sizes: dict[Widget, float] = {}
        for child, spec, basis in line:
            sizes[child] = self._clamp_main(float(basis), spec)

        total = sum(sizes.values())
        if target > total:
            remaining = target - total
            for _ in range(len(line) + 2):
                grow_items = [(c, s) for (c, s, _b) in line if s.grow > 0.0 and (s.max_main is None or sizes[c] < float(s.max_main) - 0.001)]
                if not grow_items or remaining <= 0.001:
                    break
                total_grow = sum(float(s.grow) for (_c, s) in grow_items)
                if total_grow <= 0.0:
                    break
                used = 0.0
                for c, s in grow_items:
                    share = remaining * (float(s.grow) / total_grow)
                    before = sizes[c]
                    after = self._clamp_main(before + share, s)
                    delta = max(0.0, after - before)
                    sizes[c] = after
                    used += delta
                if used <= 0.0001:
                    break
                remaining = max(0.0, remaining - used)
            return sizes

        if target < total:
            overflow = total - target
            for _ in range(len(line) + 2):
                shrink_items: list[tuple[Widget, FlexItem, float]] = []
                total_weight = 0.0
                for c, s, b in line:
                    if float(s.shrink) <= 0.0:
                        continue
                    min_v = 0.0 if s.min_main is None else float(s.min_main)
                    if sizes[c] <= min_v + 0.001:
                        continue
                    w = max(0.0, float(s.shrink)) * max(0.0001, float(b))
                    shrink_items.append((c, s, w))
                    total_weight += w
                if not shrink_items or total_weight <= 0.0 or overflow <= 0.001:
                    break

                used = 0.0
                for c, s, w in shrink_items:
                    share = overflow * (w / total_weight)
                    before = sizes[c]
                    after = self._clamp_main(before - share, s)
                    delta = max(0.0, before - after)
                    sizes[c] = after
                    used += delta
                if used <= 0.0001:
                    break
                overflow = max(0.0, overflow - used)
            return sizes

        return sizes

    def add(
        self,
        child: Widget,
        *,
        grow: float = 0.0,
        shrink: float = 1.0,
        basis: float | None = None,
        align: str | None = None,
        min_main: float | None = None,
        max_main: float | None = None,
    ) -> Widget:
        w = super().add(child)
        self._flex[w] = FlexItem(
            grow=float(grow),
            shrink=float(shrink),
            basis=basis,
            align=align,
            min_main=min_main,
            max_main=max_main,
        )
        return w

    def layout(self, theme: Any) -> None:
        is_row = self.direction != "column"
        main_avail = max(
            0.0,
            (self.rect.w - self.padding.left - self.padding.right) if is_row else (self.rect.h - self.padding.top - self.padding.bottom),
        )
        cross_avail = max(
            0.0,
            (self.rect.h - self.padding.top - self.padding.bottom) if is_row else (self.rect.w - self.padding.left - self.padding.right),
        )

        items: list[tuple[Widget, FlexItem, float, float]] = []
        for child in self.children:
            spec = self._flex.get(child, FlexItem())
            basis = spec.basis
            if basis is None:
                pref = child.measure(theme, Constraints(max_w=main_avail if is_row else None, max_h=None if is_row else main_avail))
                basis = float(pref.w if is_row else pref.h)
            basis = max(0.0, float(basis))
            pref_cross = child.measure(theme, Constraints(max_w=None if is_row else cross_avail, max_h=cross_avail if is_row else None))
            cross = max(0.0, float(pref_cross.h if is_row else pref_cross.w))
            items.append((child, spec, basis, cross))

        if self.wrap == "wrap" and len(items) > 0:
            lines: list[list[tuple[Widget, FlexItem, float, float]]] = []
            line: list[tuple[Widget, FlexItem, float, float]] = []
            used = 0.0
            for it in items:
                basis = it[2]
                add = basis if not line else basis + self.spacing
                if line and used + add > main_avail + 0.01:
                    lines.append(line)
                    line = []
                    used = 0.0
                    add = basis
                if line:
                    used += self.spacing
                line.append(it)
                used += basis
            if line:
                lines.append(line)

            cross_cursor = self.padding.top if is_row else self.padding.left
            for ln in lines:
                line_specs = [(c, s, b) for (c, s, b, _cr) in ln]
                main_sizes = self._solve_main_sizes(line_specs, main_avail)
                total_main = sum(main_sizes.values())
                gaps = max(0, len(ln) - 1)

                if self.justify_content == "space-between" and gaps > 0 and total_main < main_avail:
                    gap = (main_avail - total_main) / float(gaps)
                    start_off = 0.0
                elif self.justify_content == "space-around" and len(ln) > 0 and total_main < main_avail:
                    gap = (main_avail - total_main) / float(len(ln))
                    start_off = gap * 0.5
                else:
                    gap = self.spacing
                    free = max(0.0, main_avail - total_main - gap * float(gaps))
                    if self.justify_content == "center":
                        start_off = free * 0.5
                    elif self.justify_content == "end":
                        start_off = free
                    else:
                        start_off = 0.0

                line_cross = 0.0
                for (_c, _s, _b, cr) in ln:
                    line_cross = max(line_cross, cr)

                main_pos = (self.padding.left if is_row else self.padding.top) + start_off
                for child, spec, _basis, cross in ln:
                    ms = main_sizes.get(child, 0.0)
                    align = spec.align if spec.align is not None else self.align_items
                    if align == "stretch":
                        cs = line_cross
                        cross_pos = cross_cursor
                    elif align == "center":
                        cs = cross
                        cross_pos = cross_cursor + max(0.0, (line_cross - cs) * 0.5)
                    elif align == "end":
                        cs = cross
                        cross_pos = cross_cursor + max(0.0, line_cross - cs)
                    else:
                        cs = cross
                        cross_pos = cross_cursor

                    if is_row:
                        child.rect.x = main_pos
                        child.rect.y = cross_pos
                        child.rect.w = ms
                        child.rect.h = cs
                    else:
                        child.rect.x = cross_pos
                        child.rect.y = main_pos
                        child.rect.w = cs
                        child.rect.h = ms

                    main_pos += ms + gap
                cross_cursor += line_cross + self.run_spacing
            return

        line_specs = [(c, s, b) for (c, s, b, _cr) in items]
        main_sizes = self._solve_main_sizes(line_specs, main_avail)
        total_main = sum(main_sizes.values())
        gaps = max(0, len(items) - 1)

        if self.justify_content == "space-between" and gaps > 0 and total_main < main_avail:
            gap = (main_avail - total_main) / float(gaps)
            start_off = 0.0
        elif self.justify_content == "space-around" and len(items) > 0 and total_main < main_avail:
            gap = (main_avail - total_main) / float(len(items))
            start_off = gap * 0.5
        else:
            gap = self.spacing
            free = max(0.0, main_avail - total_main - gap * float(gaps))
            if self.justify_content == "center":
                start_off = free * 0.5
            elif self.justify_content == "end":
                start_off = free
            else:
                start_off = 0.0

        main_pos = (self.padding.left if is_row else self.padding.top) + start_off
        for child, spec, _basis, cross in items:
            ms = main_sizes.get(child, 0.0)
            align = spec.align if spec.align is not None else self.align_items
            if align == "stretch":
                cs = cross_avail
                cross_pos = self.padding.top if is_row else self.padding.left
            elif align == "center":
                cs = cross
                cross_pos = (self.padding.top if is_row else self.padding.left) + max(0.0, (cross_avail - cs) * 0.5)
            elif align == "end":
                cs = cross
                cross_pos = (self.padding.top if is_row else self.padding.left) + max(0.0, cross_avail - cs)
            else:
                cs = cross
                cross_pos = self.padding.top if is_row else self.padding.left

            if is_row:
                child.rect.x = main_pos
                child.rect.y = cross_pos
                child.rect.w = ms
                child.rect.h = cs
            else:
                child.rect.x = cross_pos
                child.rect.y = main_pos
                child.rect.w = cs
                child.rect.h = ms

            main_pos += ms + gap

    def layout_tree(self, theme: Any) -> None:
        if self.auto_layout:
            self.layout(theme)
        super().layout_tree(theme)

    def measure(self, theme: Any, constraints: Constraints) -> Size:
        is_row = self.direction != "column"
        pad_main = (self.padding.left + self.padding.right) if is_row else (self.padding.top + self.padding.bottom)
        pad_cross = (self.padding.top + self.padding.bottom) if is_row else (self.padding.left + self.padding.right)

        max_main = constraints.max_w if is_row else constraints.max_h
        if self.wrap == "wrap" and max_main is not None:
            avail_main = max(0.0, float(max_main) - pad_main)
            x = 0.0
            line_cross = 0.0
            total_cross = 0.0
            max_line_main = 0.0
            for child in self.children:
                spec = self._flex.get(child, FlexItem())
                if spec.basis is not None:
                    basis = float(spec.basis)
                else:
                    sz = child.measure(theme, Constraints())
                    basis = sz.w if is_row else sz.h
                sz2 = child.measure(theme, Constraints())
                cr = sz2.h if is_row else sz2.w

                add = basis if x == 0.0 else basis + self.spacing
                if x > 0.0 and x + add > avail_main + 0.01:
                    max_line_main = max(max_line_main, x)
                    total_cross += line_cross + self.run_spacing
                    x = 0.0
                    line_cross = 0.0
                    add = basis
                x = x + add if x > 0.0 else basis
                line_cross = max(line_cross, cr)
            max_line_main = max(max_line_main, x)
            total_cross += line_cross
            w = (max_line_main + pad_main) if is_row else (total_cross + pad_cross)
            h = (total_cross + pad_cross) if is_row else (max_line_main + pad_main)
            return constraints.constrain(Size(w, h))

        main = 0.0
        cross = 0.0
        for i, child in enumerate(self.children):
            spec = self._flex.get(child, FlexItem())
            if spec.basis is not None:
                basis = float(spec.basis)
            else:
                sz = child.measure(theme, Constraints())
                basis = sz.w if is_row else sz.h
            main += max(0.0, basis)
            if i != len(self.children) - 1:
                main += self.spacing

            sz2 = child.measure(theme, Constraints())
            cross = max(cross, sz2.h if is_row else sz2.w)

        w = (main + pad_main) if is_row else (cross + pad_cross)
        h = (cross + pad_cross) if is_row else (main + pad_main)
        return constraints.constrain(Size(w, h))


class SplitView(Container):
    def __init__(
        self,
        rect: Rect,
        *,
        direction: str = "row",
        ratio: float = 0.5,
        divider_size: float = 8.0,
        min_a: float = 80.0,
        min_b: float = 80.0,
        auto_layout: bool = True,
    ) -> None:
        super().__init__(rect)
        self.direction = direction
        self.ratio = float(ratio)
        self.divider_size = float(divider_size)
        self.min_a = float(min_a)
        self.min_b = float(min_b)
        self.auto_layout = bool(auto_layout)

        self._dragging = False
        self._drag_offset = 0.0

    def add(self, child: Widget) -> Widget:
        if len(self.children) >= 2:
            raise ValueError("SplitView supports at most two children")
        return super().add(child)

    def _solve_sizes(self, total_main: float) -> tuple[float, float]:
        total_main = max(0.0, float(total_main))
        avail = max(0.0, total_main - self.divider_size)
        if avail <= 0.0:
            return 0.0, 0.0

        lo = max(0.0, self.min_a)
        hi = max(0.0, avail - max(0.0, self.min_b))
        if hi < lo:
            lo = 0.0
            hi = avail

        a = _clamp(avail * float(self.ratio), lo, hi)
        b = max(0.0, avail - a)
        return a, b

    def _divider_abs_rect(self) -> Rect:
        r = self.abs_rect()
        is_row = self.direction != "column"
        a, _b = self._solve_sizes(r.w if is_row else r.h)
        if is_row:
            return Rect(r.x + a, r.y, self.divider_size, r.h)
        return Rect(r.x, r.y + a, r.w, self.divider_size)

    def layout(self) -> None:
        is_row = self.direction != "column"
        if len(self.children) == 0:
            return
        if len(self.children) == 1:
            self.children[0].rect = Rect(0.0, 0.0, float(self.rect.w), float(self.rect.h))
            return

        a, b = self._solve_sizes(self.rect.w if is_row else self.rect.h)
        if is_row:
            self.children[0].rect = Rect(0.0, 0.0, a, float(self.rect.h))
            self.children[1].rect = Rect(a + self.divider_size, 0.0, b, float(self.rect.h))
        else:
            self.children[0].rect = Rect(0.0, 0.0, float(self.rect.w), a)
            self.children[1].rect = Rect(0.0, a + self.divider_size, float(self.rect.w), b)

    def layout_tree(self, theme: Any) -> None:
        if self.auto_layout:
            self.layout()
        super().layout_tree(theme)

    def draw(self, love: Any, theme: Any) -> None:
        super().draw(love, theme)
        if len(self.children) < 2 or self.divider_size <= 0.0:
            return

        d = self._divider_abs_rect()
        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        if self._dragging or self.is_pressed_visual():
            theme.button_pressed.draw(love, d.x, d.y, d.w, d.h)
        elif self._hovered:
            theme.button_hover.draw(love, d.x, d.y, d.w, d.h)
        else:
            theme.track.draw(love, d.x, d.y, d.w, d.h)

    def on_mousepressed(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        if not self._divider_abs_rect().contains(float(x), float(y)):
            return False
        self.set_pressed(True)
        self._dragging = True
        d = self._divider_abs_rect()
        is_row = self.direction != "column"
        self._drag_offset = float(x - d.x) if is_row else float(y - d.y)
        return True

    def on_mousemoved(self, x: float, y: float, dx: float, dy: float) -> bool:
        if not self._dragging:
            return False

        r = self.abs_rect()
        is_row = self.direction != "column"
        total_main = r.w if is_row else r.h
        avail = max(0.0, float(total_main) - self.divider_size)
        if avail <= 0.0:
            return True

        origin = r.x if is_row else r.y
        mouse_main = float(x) if is_row else float(y)
        new_a = mouse_main - origin - self._drag_offset

        lo = max(0.0, self.min_a)
        hi = max(0.0, avail - max(0.0, self.min_b))
        if hi < lo:
            lo = 0.0
            hi = avail

        a = _clamp(float(new_a), lo, hi)
        self.ratio = 0.0 if avail <= 0.0 else float(a / avail)
        return True

    def on_mousereleased(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
        if self._dragging or self._pressed:
            self._dragging = False
            self.set_pressed(False)
            return True
        return False
