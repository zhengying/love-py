from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .theme import Theme, create_default_theme
from .types import Rect
from .widgets import Container, MessageBox, PopupMenu, PopupMenuItem, TextInput, Widget


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
        self.popup: Optional[PopupMenu] = None
        self.modal: Optional[MessageBox] = None

    def ensure_theme(self, love: Any) -> Theme:
        if self.theme is None:
            self.theme = create_default_theme(love)
        return self.theme

    def _clamp(self, v: float, lo: float, hi: float) -> float:
        if v < lo:
            return lo
        if v > hi:
            return hi
        return v

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
        if self.root.parent is None and self.root.rect.w <= 0.0 and self.root.rect.h <= 0.0:
            self.root.rect = Rect(0.0, 0.0, float(love.graphics.getWidth()), float(love.graphics.getHeight()))
        self.root.layout_tree(theme)
        self.root.draw(love, theme)
        if self.modal is not None and self.modal.visible:
            love.graphics.setColor(0.0, 0.0, 0.0, 0.50)
            love.graphics.rectangle("fill", 0, 0, love.graphics.getWidth(), love.graphics.getHeight())
            self.modal._layout(love, theme)
            self.modal.draw(love, theme)
        elif self.popup is not None and self.popup.visible:
            self.popup.draw(love, theme)

    def show_popup(self, love: Any, x: float, y: float, items: list[PopupMenuItem], min_width: float = 140.0) -> None:
        if self.modal is not None:
            return
        theme = self.ensure_theme(love)
        menu = PopupMenu(x, y, items, min_width=min_width)
        menu._layout(theme)
        r = menu.abs_rect()
        sw = float(love.graphics.getWidth())
        sh = float(love.graphics.getHeight())
        nx = float(self._clamp(r.x, 0.0, max(0.0, sw - r.w)))
        ny = float(self._clamp(r.y, 0.0, max(0.0, sh - r.h)))
        menu.rect = Rect(nx, ny, menu.rect.w, menu.rect.h)
        self.popup = menu
        self._set_hovered(None)
        self.set_focus(None)

    def close_popup(self) -> None:
        self.popup = None

    def show_message_box(
        self,
        love: Any,
        title: str,
        message: str,
        *,
        show_cancel: bool = False,
        on_confirm: Any | None = None,
        on_cancel: Any | None = None,
        ok_text: str = "OK",
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
    ) -> None:
        self.close_popup()
        theme = self.ensure_theme(love)
        self.modal = MessageBox(
            title,
            message,
            ok_text=ok_text,
            confirm_text=confirm_text,
            cancel_text=cancel_text,
            show_cancel=show_cancel,
            on_confirm=on_confirm,
            on_cancel=on_cancel,
        )
        self.modal._layout(love, theme)
        self.captured = None
        self._set_hovered(None)
        self.set_focus(None)

    def close_message_box(self) -> None:
        self.modal = None

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

        if self.modal is not None:
            if not self.modal.abs_rect().contains(self.pointer.x, self.pointer.y):
                self.modal._outside_close()
                if self.modal.close_requested:
                    self.close_message_box()
                return
            self.modal.on_mousepressed(self.pointer.x, self.pointer.y, button, presses)
            self.captured = self.modal
            return

        if self.popup is not None:
            if self.popup.hit_test(self.pointer.x, self.pointer.y) is None:
                self.close_popup()
                self.captured = None
                self._set_hovered(None)
                self.set_focus(None)
                return
            self._set_hovered(self.popup)
            consumed = self.popup.on_mousepressed(self.pointer.x, self.pointer.y, button, presses)
            if consumed:
                self.captured = self.popup
            return

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

        if self.modal is not None:
            target = self.captured if self.captured is not None else self.modal
            target.on_mousereleased(self.pointer.x, self.pointer.y, button, presses)
            self.captured = None
            if self.modal is not None and self.modal.close_requested:
                self.close_message_box()
            return

        if self.popup is not None:
            target = self.captured if self.captured is not None else self.popup
            target.on_mousereleased(self.pointer.x, self.pointer.y, button, presses)
            self.captured = None
            if self.popup is not None and self.popup.close_requested:
                self.close_popup()
                self._set_hovered(None)
                self.set_focus(None)
                return
            if self.popup is not None and self.popup.hit_test(self.pointer.x, self.pointer.y) is None:
                self._set_hovered(None)
            else:
                self._set_hovered(self.popup)
            return

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

        if self.modal is not None:
            self.modal.on_mousemoved(self.pointer.x, self.pointer.y, float(dx), float(dy))
            return

        if self.popup is not None:
            self._set_hovered(self.popup if self.popup.hit_test(self.pointer.x, self.pointer.y) is not None else None)
            self.popup.on_mousemoved(self.pointer.x, self.pointer.y, float(dx), float(dy))
            return

        target = self.captured if self.captured is not None else self._hit_test(self.pointer.x, self.pointer.y)
        self._set_hovered(None if self.captured is not None else target)
        if target is not None:
            target.on_mousemoved(self.pointer.x, self.pointer.y, float(dx), float(dy))

    def on_wheelmoved(self, x: float, y: float) -> None:
        if self.modal is not None:
            return
        if self.popup is not None:
            return
        target = self._hit_test(self.pointer.x, self.pointer.y)
        dx = float(x)
        dy = float(y)
        while target is not None:
            if target.on_wheelmoved(dx, dy):
                return
            target = target.parent

    def on_keypressed(self, key: str, scancode: Any, isrepeat: bool) -> None:
        if self.modal is not None:
            consumed = self.modal.on_keypressed(key, scancode, isrepeat)
            if self.modal is not None and self.modal.close_requested:
                self.close_message_box()
            if consumed:
                return
        if self.popup is not None:
            consumed = self.popup.on_keypressed(key, scancode, isrepeat)
            if self.popup is not None and self.popup.close_requested:
                self.close_popup()
            if consumed:
                return
        if self.focused is None:
            return
        consumed = self.focused.on_keypressed(key, scancode, isrepeat)
        if consumed:
            return

    def on_textinput(self, text: str) -> None:
        if self.modal is not None:
            return
        if self.popup is not None:
            return
        if self.focused is None:
            return
        self.focused.on_textinput(text)


def _default_root_rect() -> Any:
    from .types import Rect

    return Rect(0.0, 0.0, 0.0, 0.0)
