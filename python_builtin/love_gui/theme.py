from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .nineslice import NineSlice
from .types import Insets


@dataclass(frozen=True)
class Theme:
    font: Any
    panel: NineSlice
    button: NineSlice
    button_hover: NineSlice
    button_pressed: NineSlice
    input: NineSlice
    track: NineSlice
    fill: NineSlice

    text_color: tuple[float, float, float, float] = (0.92, 0.92, 0.95, 1.0)
    text_muted: tuple[float, float, float, float] = (0.70, 0.70, 0.75, 1.0)
    accent: tuple[float, float, float, float] = (0.30, 0.65, 1.0, 1.0)


def _draw_skin_variant(love: Any, canvas: Any, base: tuple[float, float, float], edge: tuple[float, float, float]) -> None:
    def draw() -> None:
        love.graphics.clear(0.0, 0.0, 0.0, 0.0)
        love.graphics.setColor(base[0], base[1], base[2], 1.0)
        love.graphics.rectangle("fill", 0, 0, 48, 48)
        love.graphics.setColor(edge[0], edge[1], edge[2], 1.0)
        love.graphics.rectangle("fill", 0, 0, 48, 10)
        love.graphics.rectangle("fill", 0, 38, 48, 10)
        love.graphics.rectangle("fill", 0, 0, 10, 48)
        love.graphics.rectangle("fill", 38, 0, 10, 48)
        love.graphics.setColor(edge[0] * 1.12, edge[1] * 1.12, edge[2] * 1.12, 1.0)
        love.graphics.rectangle("fill", 0, 0, 10, 10)
        love.graphics.rectangle("fill", 38, 0, 10, 10)
        love.graphics.rectangle("fill", 0, 38, 10, 10)
        love.graphics.rectangle("fill", 38, 38, 10, 10)

    canvas.renderTo(draw)


def create_default_theme(love: Any) -> Theme:
    font = love.graphics.getFont()

    panel_canvas = love.graphics.newCanvas(48, 48)
    button_canvas = love.graphics.newCanvas(48, 48)
    button_hover_canvas = love.graphics.newCanvas(48, 48)
    button_pressed_canvas = love.graphics.newCanvas(48, 48)
    input_canvas = love.graphics.newCanvas(48, 48)
    track_canvas = love.graphics.newCanvas(48, 48)
    fill_canvas = love.graphics.newCanvas(48, 48)

    _draw_skin_variant(love, panel_canvas, base=(0.13, 0.13, 0.16), edge=(0.22, 0.22, 0.26))
    _draw_skin_variant(love, button_canvas, base=(0.18, 0.18, 0.22), edge=(0.30, 0.30, 0.36))
    _draw_skin_variant(love, button_hover_canvas, base=(0.21, 0.21, 0.25), edge=(0.38, 0.38, 0.45))
    _draw_skin_variant(love, button_pressed_canvas, base=(0.14, 0.18, 0.26), edge=(0.22, 0.40, 0.65))
    _draw_skin_variant(love, input_canvas, base=(0.10, 0.10, 0.12), edge=(0.26, 0.26, 0.30))
    _draw_skin_variant(love, track_canvas, base=(0.12, 0.12, 0.14), edge=(0.22, 0.22, 0.26))
    _draw_skin_variant(love, fill_canvas, base=(0.15, 0.35, 0.60), edge=(0.30, 0.65, 1.0))

    insets = Insets(10, 10, 10, 10)
    return Theme(
        font=font,
        panel=NineSlice(panel_canvas, insets),
        button=NineSlice(button_canvas, insets),
        button_hover=NineSlice(button_hover_canvas, insets),
        button_pressed=NineSlice(button_pressed_canvas, insets),
        input=NineSlice(input_canvas, insets),
        track=NineSlice(track_canvas, insets),
        fill=NineSlice(fill_canvas, insets),
    )
