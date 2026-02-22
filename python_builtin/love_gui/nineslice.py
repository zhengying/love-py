from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .types import Insets


class _Drawable(Protocol):
    def getWidth(self) -> int: ...
    def getHeight(self) -> int: ...


@dataclass(frozen=True)
class NineSlice:
    drawable: Any
    insets: Insets
    src_x: float = 0.0
    src_y: float = 0.0
    src_w: float | None = None
    src_h: float | None = None

    def draw(self, love: Any, x: float, y: float, w: float, h: float) -> None:
        dw = float(getattr(self.drawable, "getWidth")())
        dh = float(getattr(self.drawable, "getHeight")())
        src_w = float(self.src_w) if self.src_w is not None else dw
        src_h = float(self.src_h) if self.src_h is not None else dh

        l = max(0.0, self.insets.left)
        t = max(0.0, self.insets.top)
        r = max(0.0, self.insets.right)
        b = max(0.0, self.insets.bottom)

        l = min(l, w)
        r = min(r, max(0.0, w - l))
        t = min(t, h)
        b = min(b, max(0.0, h - t))

        sx0 = self.src_x
        sy0 = self.src_y
        sx1 = sx0 + l
        sy1 = sy0 + t
        sx2 = sx0 + src_w - r
        sy2 = sy0 + src_h - b
        sx3 = sx0 + src_w
        sy3 = sy0 + src_h

        dx0 = x
        dy0 = y
        dx1 = x + l
        dy1 = y + t
        dx2 = x + w - r
        dy2 = y + h - b
        dx3 = x + w
        dy3 = y + h

        draw_region = love.graphics.drawImageRegion
        img = self.drawable

        if l > 0 and t > 0:
            draw_region(img, sx0, sy0, l, t, x=dx0, y=dy0)
        if dx2 > dx1 and t > 0:
            draw_region(img, sx1, sy0, max(0.0, sx2 - sx1), t, x=dx1, y=dy0, scale_x=(dx2 - dx1) / max(1.0, sx2 - sx1))
        if r > 0 and t > 0:
            draw_region(img, sx2, sy0, r, t, x=dx2, y=dy0)

        if l > 0 and dy2 > dy1:
            draw_region(img, sx0, sy1, l, max(0.0, sy2 - sy1), x=dx0, y=dy1, scale_y=(dy2 - dy1) / max(1.0, sy2 - sy1))
        if dx2 > dx1 and dy2 > dy1:
            draw_region(
                img,
                sx1,
                sy1,
                max(0.0, sx2 - sx1),
                max(0.0, sy2 - sy1),
                x=dx1,
                y=dy1,
                scale_x=(dx2 - dx1) / max(1.0, sx2 - sx1),
                scale_y=(dy2 - dy1) / max(1.0, sy2 - sy1),
            )
        if r > 0 and dy2 > dy1:
            draw_region(img, sx2, sy1, r, max(0.0, sy2 - sy1), x=dx2, y=dy1, scale_y=(dy2 - dy1) / max(1.0, sy2 - sy1))

        if l > 0 and b > 0:
            draw_region(img, sx0, sy2, l, b, x=dx0, y=dy2)
        if dx2 > dx1 and b > 0:
            draw_region(img, sx1, sy2, max(0.0, sx2 - sx1), b, x=dx1, y=dy2, scale_x=(dx2 - dx1) / max(1.0, sx2 - sx1))
        if r > 0 and b > 0:
            draw_region(img, sx2, sy2, r, b, x=dx2, y=dy2)
