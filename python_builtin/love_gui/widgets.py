from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

from .types import Insets, Rect


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

    def hit_test(self, x: float, y: float) -> Optional["Widget"]:
        if not self.visible or not self.enabled:
            return None
        if self.abs_rect().contains(x, y):
            return self
        return None

    def update(self, dt: float) -> None:
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
        for child in self.children:
            child.update(dt)

    def draw(self, love: Any, theme: Any) -> None:
        for child in self.children:
            if child.visible:
                child.draw(love, theme)


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


class Button(Widget):
    def __init__(self, rect: Rect, text: str, on_click: Optional[Callable[[], None]] = None) -> None:
        super().__init__(rect)
        self.text = text
        self.on_click = on_click
        self._pressed_inside = False

    def draw(self, love: Any, theme: Any) -> None:
        r = self.abs_rect()
        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        if self._pressed and self._hovered:
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


class TextInput(Widget):
    def __init__(self, rect: Rect, text: str = "", placeholder: str = "") -> None:
        super().__init__(rect)
        self.focusable = True
        self.text = text
        self.placeholder = placeholder
        self.cursor = len(text)
        self._focused = False
        self._scroll_x = 0.0

    def set_focused(self, focused: bool) -> None:
        self._focused = focused

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
        pad_y = max(0.0, (inner.h - float(theme.font.getHeight())) * 0.5)
        prev_scissor = _push_scissor(love, inner.x, inner.y, inner.w, inner.h)

        if self.text:
            text_w = float(theme.font.getWidth(self.text))
            avail = max(0.0, r.w - pad_x * 2.0)
            cursor_px = float(theme.font.getWidth(self.text[: self.cursor]))

            if self._focused:
                if cursor_px - self._scroll_x > avail:
                    self._scroll_x = cursor_px - avail + 2.0
                if cursor_px - self._scroll_x < 0.0:
                    self._scroll_x = max(0.0, cursor_px - 2.0)
                self._scroll_x = _clamp(self._scroll_x, 0.0, max(0.0, text_w - avail))
            else:
                self._scroll_x = max(0.0, text_w - avail)

            love.graphics.setColor(*theme.text_color)
            love.graphics.print(
                self.text,
                _round_half_up(r.x + pad_x - self._scroll_x),
                _round_half_up(inner.y + pad_y),
            )

            if self._focused:
                t = float(love.timer.getTime())
                on = int(t * 2) % 2 == 0
                if on:
                    cx = r.x + pad_x - self._scroll_x + cursor_px
                    love.graphics.setColor(*theme.text_color)
                    love.graphics.rectangle(
                        "fill",
                        _round_half_up(cx),
                        _round_half_up(inner.y + pad_y),
                        2,
                        float(theme.font.getHeight()),
                    )
        else:
            self._scroll_x = 0.0
            love.graphics.setColor(*theme.text_muted)
            love.graphics.print(
                self.placeholder,
                _round_half_up(r.x + pad_x),
                _round_half_up(inner.y + pad_y),
            )

        _pop_scissor(love, prev_scissor)

    def on_mousepressed(self, x: float, y: float, button: int, presses: int) -> bool:
        if button != 1:
            return False
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


class ScrollView(Container):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)
        self.scroll_x = 0.0
        self.scroll_y = 0.0
        self.scroll_speed = 38.0

    def content_bounds(self) -> Rect:
        if not self.children:
            return Rect(0.0, 0.0, 0.0, 0.0)
        min_x = min(c.rect.x for c in self.children)
        min_y = min(c.rect.y for c in self.children)
        max_r = max(c.rect.x + c.rect.w for c in self.children)
        max_b = max(c.rect.y + c.rect.h for c in self.children)
        return Rect(min_x, min_y, max(0.0, max_r - min_x), max(0.0, max_b - min_y))

    def _apply_scroll_limits(self) -> None:
        bounds = self.content_bounds()
        max_x = max(0.0, bounds.w - self.rect.w)
        max_y = max(0.0, bounds.h - self.rect.h)
        self.scroll_x = _clamp(self.scroll_x, 0.0, max_x)
        self.scroll_y = _clamp(self.scroll_y, 0.0, max_y)

    def on_wheelmoved(self, x: float, y: float) -> bool:
        self.scroll_y -= float(y) * self.scroll_speed
        self._apply_scroll_limits()
        return True

    def hit_test(self, x: float, y: float) -> Optional[Widget]:
        if not self.visible or not self.enabled:
            return None
        if not self.abs_rect().contains(x, y):
            return None
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


class VBox(Container):
    def __init__(self, rect: Rect, spacing: float = 8.0, padding: Insets | None = None) -> None:
        super().__init__(rect)
        self.spacing = spacing
        self.padding = padding if padding is not None else Insets.all(0.0)

    def layout(self) -> None:
        y = self.padding.top
        for child in self.children:
            child.rect.x = self.padding.left
            child.rect.y = y
            child.rect.w = max(0.0, self.rect.w - self.padding.left - self.padding.right)
            y += child.rect.h + self.spacing


class HBox(Container):
    def __init__(self, rect: Rect, spacing: float = 8.0, padding: Insets | None = None) -> None:
        super().__init__(rect)
        self.spacing = spacing
        self.padding = padding if padding is not None else Insets.all(0.0)

    def layout(self) -> None:
        x = self.padding.left
        for child in self.children:
            child.rect.x = x
            child.rect.y = self.padding.top
            child.rect.h = max(0.0, self.rect.h - self.padding.top - self.padding.bottom)
            x += child.rect.w + self.spacing
