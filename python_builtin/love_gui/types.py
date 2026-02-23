from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Insets:
    left: float
    top: float
    right: float
    bottom: float

    @staticmethod
    def all(v: float) -> "Insets":
        return Insets(v, v, v, v)


@dataclass
class Rect:
    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h

    def contains(self, px: float, py: float) -> bool:
        return self.x <= px < self.right and self.y <= py < self.bottom

    def inset(self, insets: Insets) -> "Rect":
        nx = self.x + insets.left
        ny = self.y + insets.top
        nw = max(0.0, self.w - insets.left - insets.right)
        nh = max(0.0, self.h - insets.top - insets.bottom)
        return Rect(nx, ny, nw, nh)


@dataclass(frozen=True)
class Size:
    w: float
    h: float


@dataclass(frozen=True)
class Constraints:
    min_w: float = 0.0
    min_h: float = 0.0
    max_w: float | None = None
    max_h: float | None = None

    def constrain(self, size: Size) -> Size:
        w = max(self.min_w, float(size.w))
        h = max(self.min_h, float(size.h))
        if self.max_w is not None:
            w = min(w, float(self.max_w))
        if self.max_h is not None:
            h = min(h, float(self.max_h))
        return Size(w, h)
