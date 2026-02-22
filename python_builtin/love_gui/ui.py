from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .theme import Theme, create_default_theme
from .widgets import Container, TextInput, Widget


@dataclass
class _PointerState:
    x: float = 0.0
    y: float = 0.0
    down: bool = False
    button: int = 0


class UI:
    def __init__(self, root: Optional[Container] = None, theme: Optional[Theme] = None) -> None:
        self.root = root if root is not None else Container(rect=_default_root_rect())
        self.theme = theme

        self.pointer = _PointerState()
        self.hovered: Optional[Widget] = None
        self.captured: Optional[Widget] = None
        self.focused: Optional[Widget] = None

    def ensure_theme(self, love: Any) -> Theme:
        if self.theme is None:
            self.theme = create_default_theme(love)
        return self.theme

    def set_focus(self, widget: Optional[Widget]) -> None:
        if self.focused is widget:
            return
        prev = self.focused
        self.focused = widget
        if isinstance(prev, TextInput):
            prev.set_focused(False)
        if isinstance(widget, TextInput):
            widget.set_focused(True)

    def update(self, dt: float) -> None:
        self.root.update(dt)

    def draw(self, love: Any) -> None:
        theme = self.ensure_theme(love)
        if theme.font is not None:
            love.graphics.setFont(theme.font)
        self.root.draw(love, theme)

    def _set_hovered(self, widget: Optional[Widget]) -> None:
        if self.hovered is widget:
            return
        if self.hovered is not None:
            self.hovered.set_hovered(False)
        self.hovered = widget
        if self.hovered is not None:
            self.hovered.set_hovered(True)

    def _hit_test(self, x: float, y: float) -> Optional[Widget]:
        return self.root.hit_test(x, y)

    def on_mousepressed(self, x: float, y: float, button: int, istouch: bool, presses: int) -> None:
        self.pointer.x = float(x)
        self.pointer.y = float(y)
        self.pointer.down = True
        self.pointer.button = int(button)

        target = self._hit_test(self.pointer.x, self.pointer.y)
        self._set_hovered(target)

        if target is None:
            self.set_focus(None)
            return

        if target.focusable:
            self.set_focus(target)
        else:
            self.set_focus(None)

        consumed = target.on_mousepressed(self.pointer.x, self.pointer.y, button, presses)
        if consumed:
            self.captured = target

    def on_mousereleased(self, x: float, y: float, button: int, istouch: bool, presses: int) -> None:
        self.pointer.x = float(x)
        self.pointer.y = float(y)
        self.pointer.down = False
        self.pointer.button = 0

        target = self.captured if self.captured is not None else self._hit_test(self.pointer.x, self.pointer.y)
        if target is None:
            self.captured = None
            return

        target.on_mousereleased(self.pointer.x, self.pointer.y, button, presses)
        self.captured = None
        self._set_hovered(self._hit_test(self.pointer.x, self.pointer.y))

    def on_mousemoved(self, x: float, y: float, dx: float, dy: float, istouch: bool) -> None:
        self.pointer.x = float(x)
        self.pointer.y = float(y)

        target = self.captured if self.captured is not None else self._hit_test(self.pointer.x, self.pointer.y)
        self._set_hovered(None if self.captured is not None else target)
        if target is not None:
            target.on_mousemoved(self.pointer.x, self.pointer.y, float(dx), float(dy))

    def on_wheelmoved(self, x: float, y: float) -> None:
        target = self._hit_test(self.pointer.x, self.pointer.y)
        if target is None:
            return
        target.on_wheelmoved(float(x), float(y))

    def on_keypressed(self, key: str, scancode: Any, isrepeat: bool) -> None:
        if self.focused is None:
            return
        consumed = self.focused.on_keypressed(key, scancode, isrepeat)
        if consumed:
            return

    def on_textinput(self, text: str) -> None:
        if self.focused is None:
            return
        self.focused.on_textinput(text)


def _default_root_rect() -> Any:
    from .types import Rect

    return Rect(0.0, 0.0, 0.0, 0.0)
