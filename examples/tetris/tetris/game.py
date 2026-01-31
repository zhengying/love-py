from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import love

from .board import Board
from .pieces import FallingPiece, ORDERED_PIECES, PIECE_COLORS


@dataclass
class _RepeatState:
    direction: int = 0
    held_time: float = 0.0
    arr_accum: float = 0.0


class TetrisGame:
    def __init__(self) -> None:
        self.board = Board()
        self.current: Optional[FallingPiece] = None
        self.next_queue: List[str] = []
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self._gravity_accum = 0.0
        self._keys_down: Dict[str, bool] = {}
        self._repeat = _RepeatState()
        self._rng = random.Random()

    def reset(self) -> None:
        love.graphics.setBackgroundColor(0.08, 0.08, 0.10)
        self.board.reset()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self._gravity_accum = 0.0
        self._keys_down = {}
        self._repeat = _RepeatState()
        self.next_queue = []
        for _ in range(5):
            self._ensure_next()
        self.current = self._spawn_piece(self._take_next())
        if not self.board.can_place(self.current):
            self.game_over = True

    def keypressed(self, key: str, scancode: int, isrepeat: int) -> None:
        kid = self._normalize_key(key)
        self._keys_down[kid] = True

        if kid == "escape":
            love.event.quit()
            return

        if kid == "p":
            if not self.game_over:
                self.paused = not self.paused
            return

        if kid == "r":
            self.reset()
            return

        if self.game_over or self.paused or not self.current:
            return

        if kid == "left":
            self._move_horizontal(-1)
            self._repeat = _RepeatState(direction=-1, held_time=0.0, arr_accum=0.0)
            return

        if kid == "right":
            self._move_horizontal(1)
            self._repeat = _RepeatState(direction=1, held_time=0.0, arr_accum=0.0)
            return

        if kid == "down":
            self._soft_drop_one()
            return

        if kid in ("up", "x"):
            self._rotate(1)
            return

        if kid == "z":
            self._rotate(-1)
            return

        if kid == "space":
            self._hard_drop()
            return

    def keyreleased(self, key: str, scancode: int) -> None:
        kid = self._normalize_key(key)
        self._keys_down[kid] = False
        if kid == "left" and self._repeat.direction == -1:
            self._repeat = _RepeatState()
        if kid == "right" and self._repeat.direction == 1:
            self._repeat = _RepeatState()

    def update(self, dt: float) -> None:
        if self.game_over or self.paused or not self.current:
            return

        self._update_horizontal_repeat(dt)

        interval = self._drop_interval()
        if self._is_down("down"):
            interval = min(interval, 0.05)

        self._gravity_accum += dt
        while self._gravity_accum >= interval:
            self._gravity_accum -= interval
            if not self._step_down_or_lock():
                break

    def draw(self) -> None:
        love.graphics.clear(0.08, 0.08, 0.10, 1.0)

        cell = 28
        margin_x = 40
        margin_y = 40
        board_w_px = self.board.width * cell
        board_h_px = self.board.visible_height * cell

        self._draw_panel(margin_x - 10, margin_y - 10, board_w_px + 20, board_h_px + 20)
        self._draw_grid(margin_x, margin_y, cell)
        self._draw_locked_blocks(margin_x, margin_y, cell)

        if self.current:
            self._draw_ghost(margin_x, margin_y, cell)
            self._draw_piece(self.current, margin_x, margin_y, cell, alpha=1.0)

        right_x = margin_x + board_w_px + 40
        self._draw_sidebar(right_x, margin_y)

        if self.paused:
            love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
            love.graphics.print("PAUSED", margin_x + 90, margin_y + 260)

        if self.game_over:
            love.graphics.setColor(1.0, 0.3, 0.3, 1.0)
            love.graphics.print("GAME OVER", margin_x + 70, margin_y + 250)
            love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
            love.graphics.print("Press R to restart", margin_x + 55, margin_y + 290)

    def _normalize_key(self, key: str) -> str:
        k = (key or "").strip().lower()
        k = k.replace("_", " ")
        if k in (" ", ""):
            return ""
        if k == "escape":
            return "escape"
        if k == "space":
            return "space"
        if "left" in k:
            return "left"
        if "right" in k:
            return "right"
        if "down" in k:
            return "down"
        if "up" in k:
            return "up"
        if k in ("x", "z", "p", "r"):
            return k
        if len(k) == 1 and "a" <= k <= "z":
            return k
        return k

    def _is_down(self, key_id: str) -> bool:
        return self._keys_down.get(key_id, False)

    def _drop_interval(self) -> float:
        base = 0.8 - (self.level - 1) * 0.07
        return max(0.05, base)

    def _ensure_next(self) -> None:
        if len(self.next_queue) >= 5:
            return
        bag = list(ORDERED_PIECES)
        self._rng.shuffle(bag)
        self.next_queue.extend(bag)

    def _take_next(self) -> str:
        self._ensure_next()
        kind = self.next_queue.pop(0)
        self._ensure_next()
        return kind

    def _spawn_piece(self, kind: str) -> FallingPiece:
        x = 3
        y = 0
        return FallingPiece(kind=kind, x=x, y=y, rotation=0)

    def _try_set_piece(self, piece: FallingPiece) -> bool:
        if self.board.can_place(piece):
            self.current = piece
            return True
        return False

    def _move_horizontal(self, dx: int) -> None:
        if not self.current:
            return
        self._try_set_piece(self.current.moved(dx, 0))

    def _soft_drop_one(self) -> None:
        if not self.current:
            return
        nxt = self.current.moved(0, 1)
        if self.board.can_place(nxt):
            self.current = nxt
            self.score += 1
            self._gravity_accum = 0.0
        else:
            self._lock_and_spawn()

    def _hard_drop(self) -> None:
        if not self.current:
            return
        d = self.board.drop_distance(self.current)
        if d > 0:
            self.current = self.current.moved(0, d)
            self.score += 2 * d
        self._lock_and_spawn()

    def _rotate(self, direction: int) -> None:
        if not self.current:
            return
        rotated = self.current.rotated(direction)
        kicks = [(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)]
        for dx, dy in kicks:
            if self._try_set_piece(rotated.moved(dx, dy)):
                return

    def _step_down_or_lock(self) -> bool:
        if not self.current:
            return False
        nxt = self.current.moved(0, 1)
        if self.board.can_place(nxt):
            self.current = nxt
            return True
        self._lock_and_spawn()
        return False

    def _lock_and_spawn(self) -> None:
        if not self.current:
            return
        self.board.lock(self.current)
        cleared = self.board.clear_lines().cleared
        if cleared:
            self._apply_scoring(cleared)
        self.current = self._spawn_piece(self._take_next())
        self._gravity_accum = 0.0
        if not self.board.can_place(self.current) or self.board.is_stack_in_hidden_rows():
            self.game_over = True

    def _apply_scoring(self, cleared: int) -> None:
        table = {1: 40, 2: 100, 3: 300, 4: 1200}
        self.score += table.get(cleared, 0) * self.level
        self.lines += cleared
        self.level = 1 + self.lines // 10

    def _update_horizontal_repeat(self, dt: float) -> None:
        left = self._is_down("left")
        right = self._is_down("right")
        direction = (-1 if left and not right else 1 if right and not left else 0)

        if direction == 0:
            self._repeat = _RepeatState()
            return

        if direction != self._repeat.direction:
            self._move_horizontal(direction)
            self._repeat = _RepeatState(direction=direction, held_time=0.0, arr_accum=0.0)
            return

        das = 0.18
        arr = 0.05
        self._repeat.held_time += dt
        if self._repeat.held_time < das:
            return
        self._repeat.arr_accum += dt
        while self._repeat.arr_accum >= arr:
            self._repeat.arr_accum -= arr
            self._move_horizontal(direction)

    def _draw_panel(self, x: int, y: int, w: int, h: int) -> None:
        love.graphics.setColor(0.14, 0.14, 0.17, 1.0)
        love.graphics.rectangle("fill", x, y, w, h)
        love.graphics.setColor(0.30, 0.30, 0.34, 1.0)
        love.graphics.rectangle("line", x, y, w, h)

    def _draw_grid(self, x0: int, y0: int, cell: int) -> None:
        love.graphics.setColor(0.11, 0.11, 0.13, 1.0)
        love.graphics.rectangle("fill", x0, y0, self.board.width * cell, self.board.visible_height * cell)
        love.graphics.setColor(0.18, 0.18, 0.20, 1.0)
        for x in range(self.board.width + 1):
            xpx = x0 + x * cell
            love.graphics.line(xpx, y0, xpx, y0 + self.board.visible_height * cell)
        for y in range(self.board.visible_height + 1):
            ypx = y0 + y * cell
            love.graphics.line(x0, ypx, x0 + self.board.width * cell, ypx)

    def _draw_locked_blocks(self, x0: int, y0: int, cell: int) -> None:
        for x, y, kind in self.board.iter_visible_cells():
            if kind is None:
                continue
            self._draw_block(kind, x0 + x * cell, y0 + y * cell, cell, alpha=1.0)

    def _draw_piece(self, piece: FallingPiece, x0: int, y0: int, cell: int, alpha: float) -> None:
        for x, y in piece.cells():
            if y < self.board.hidden_rows:
                continue
            vy = y - self.board.hidden_rows
            self._draw_block(piece.kind, x0 + x * cell, y0 + vy * cell, cell, alpha=alpha)

    def _draw_ghost(self, x0: int, y0: int, cell: int) -> None:
        if not self.current:
            return
        d = self.board.drop_distance(self.current)
        ghost = self.current.moved(0, d)
        for x, y in ghost.cells():
            if y < self.board.hidden_rows:
                continue
            vy = y - self.board.hidden_rows
            self._draw_ghost_block(ghost.kind, x0 + x * cell, y0 + vy * cell, cell)

    def _draw_block(self, kind: str, x: int, y: int, size: int, alpha: float) -> None:
        r, g, b = PIECE_COLORS.get(kind, (1.0, 1.0, 1.0))
        love.graphics.setColor(r, g, b, alpha)
        love.graphics.rectangle("fill", x + 1, y + 1, size - 2, size - 2)
        love.graphics.setColor(r * 0.55, g * 0.55, b * 0.55, alpha)
        love.graphics.rectangle("line", x + 1, y + 1, size - 2, size - 2)

    def _draw_ghost_block(self, kind: str, x: int, y: int, size: int) -> None:
        r, g, b = PIECE_COLORS.get(kind, (1.0, 1.0, 1.0))
        pad = max(4, size // 5)
        inner = size - pad * 2
        if inner <= 0:
            return
        love.graphics.setColor(r, g, b, 0.06)
        love.graphics.rectangle("fill", x + pad, y + pad, inner, inner)
        love.graphics.setColor(1.0, 1.0, 1.0, 0.38)
        love.graphics.rectangle("line", x + pad, y + pad, inner, inner)
        love.graphics.setColor(r * 0.8, g * 0.8, b * 0.8, 0.20)
        love.graphics.rectangle("line", x + pad + 1, y + pad + 1, inner - 2, inner - 2)

    def _draw_sidebar(self, x: int, y: int) -> None:
        love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
        love.graphics.print(f"Score: {self.score}", x, y)
        love.graphics.print(f"Lines: {self.lines}", x, y + 24)
        love.graphics.print(f"Level: {self.level}", x, y + 48)

        love.graphics.print("Next:", x, y + 100)
        self._draw_next_preview(x, y + 130)

        love.graphics.print("Controls:", x, y + 260)
        love.graphics.print("Arrows: move", x, y + 284)
        love.graphics.print("Up/X: rotate", x, y + 308)
        love.graphics.print("Z: rotate CCW", x, y + 332)
        love.graphics.print("Space: hard drop", x, y + 356)
        love.graphics.print("P: pause", x, y + 380)
        love.graphics.print("R: restart", x, y + 404)
        love.graphics.print("Esc: quit", x, y + 428)

    def _draw_next_preview(self, x: int, y: int) -> None:
        if not self.next_queue:
            return
        kind = self.next_queue[0]
        cell = 20
        preview_origin_x = x
        preview_origin_y = y
        piece = FallingPiece(kind=kind, x=0, y=0, rotation=0)
        cells = list(piece.cells())
        min_x = min(cx for cx, cy in cells)
        min_y = min(cy for cx, cy in cells)
        max_x = max(cx for cx, cy in cells)
        max_y = max(cy for cx, cy in cells)
        w = (max_x - min_x + 1) * cell
        h = (max_y - min_y + 1) * cell
        ox = preview_origin_x + (120 - w) // 2
        oy = preview_origin_y + (80 - h) // 2
        for cx, cy in cells:
            px = ox + (cx - min_x) * cell
            py = oy + (cy - min_y) * cell
            self._draw_block(kind, px, py, cell, alpha=1.0)
