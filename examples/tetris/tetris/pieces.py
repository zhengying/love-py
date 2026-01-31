from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple


Cell = Tuple[int, int]


PIECE_COLORS: Dict[str, Tuple[float, float, float]] = {
    "I": (0.0, 0.9, 0.9),
    "O": (0.9, 0.9, 0.0),
    "T": (0.7, 0.2, 0.9),
    "S": (0.2, 0.9, 0.2),
    "Z": (0.9, 0.2, 0.2),
    "J": (0.2, 0.4, 0.9),
    "L": (0.9, 0.5, 0.1),
}


PIECE_ROTATIONS: Dict[str, List[List[Cell]]] = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
    "O": [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(1, 1), (2, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}


ORDERED_PIECES: Tuple[str, ...] = ("I", "O", "T", "S", "Z", "J", "L")


@dataclass(frozen=True)
class FallingPiece:
    kind: str
    x: int
    y: int
    rotation: int = 0

    def cells(self) -> Sequence[Cell]:
        return [(self.x + dx, self.y + dy) for dx, dy in PIECE_ROTATIONS[self.kind][self.rotation]]

    def rotated(self, direction: int) -> "FallingPiece":
        r = (self.rotation + direction) % 4
        return FallingPiece(self.kind, self.x, self.y, r)

    def moved(self, dx: int, dy: int) -> "FallingPiece":
        return FallingPiece(self.kind, self.x + dx, self.y + dy, self.rotation)

