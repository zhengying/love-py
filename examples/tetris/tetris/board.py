from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

from .pieces import FallingPiece


Cell = Tuple[int, int]


@dataclass
class LineClearResult:
    cleared: int
    cells_removed: int


class Board:
    def __init__(self, width: int = 10, visible_height: int = 20, hidden_rows: int = 2) -> None:
        self.width = width
        self.visible_height = visible_height
        self.hidden_rows = hidden_rows
        self.height = visible_height + hidden_rows
        self.grid: List[List[Optional[str]]] = []
        self.reset()

    def reset(self) -> None:
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def cell(self, x: int, y: int) -> Optional[str]:
        if not self.in_bounds(x, y):
            return None
        return self.grid[y][x]

    def can_place(self, piece: FallingPiece) -> bool:
        for x, y in piece.cells():
            if not self.in_bounds(x, y):
                return False
            if self.grid[y][x] is not None:
                return False
        return True

    def lock(self, piece: FallingPiece) -> None:
        for x, y in piece.cells():
            if self.in_bounds(x, y):
                self.grid[y][x] = piece.kind

    def drop_distance(self, piece: FallingPiece) -> int:
        d = 0
        candidate = piece
        while True:
            nxt = candidate.moved(0, 1)
            if not self.can_place(nxt):
                return d
            candidate = nxt
            d += 1

    def clear_lines(self) -> LineClearResult:
        kept: List[List[Optional[str]]] = []
        cleared = 0
        removed_cells = 0
        for row in self.grid:
            if all(cell is not None for cell in row):
                cleared += 1
                removed_cells += self.width
            else:
                kept.append(row)
        if cleared == 0:
            return LineClearResult(0, 0)
        while len(kept) < self.height:
            kept.insert(0, [None for _ in range(self.width)])
        self.grid = kept
        return LineClearResult(cleared, removed_cells)

    def is_stack_in_hidden_rows(self) -> bool:
        for y in range(self.hidden_rows):
            if any(self.grid[y][x] is not None for x in range(self.width)):
                return True
        return False

    def iter_visible_cells(self) -> Sequence[Tuple[int, int, Optional[str]]]:
        cells: List[Tuple[int, int, Optional[str]]] = []
        for y in range(self.hidden_rows, self.height):
            for x in range(self.width):
                cells.append((x, y - self.hidden_rows, self.grid[y][x]))
        return cells

