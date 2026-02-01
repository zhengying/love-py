import love


_font = None


def _try_load_font():
    candidates = [
        "/System/Library/Fonts/Geneva.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
    ]
    for path in candidates:
        try:
            return love.font.newFont(path, 18)
        except Exception:
            pass
    return None


def love_load():
    global _font
    love.window.setTitle("LOVE2D Python")
    love.graphics.setBackgroundColor(0.08, 0.08, 0.10, 1.0)
    _font = _try_load_font()
    if _font is not None:
        love.graphics.setFont(_font)


def love_update(dt):
    pass


def love_draw():
    love.graphics.clear(0.08, 0.08, 0.10, 1.0)

    love.graphics.setColor(0.2, 0.8, 0.4, 1.0)
    love.graphics.rectangle("fill", 60, 70, 680, 120)

    love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
    try:
        love.graphics.print("Welcome to LOVE2D Python", 90, 95)
        love.graphics.print("Run a game script from Terminal:", 90, 130)
        love.graphics.print("  love your_game.py", 90, 155)
    except Exception:
        love.graphics.rectangle("line", 90, 95, 620, 80)

    love.graphics.setColor(0.3, 0.3, 0.35, 1.0)
    love.graphics.rectangle("fill", 60, 220, 680, 300)

    love.graphics.setColor(1.0, 1.0, 1.0, 1.0)
    try:
        love.graphics.print("Examples:", 90, 245)
        love.graphics.print("  love examples/visual_test.py", 90, 275)
        love.graphics.print("  love examples/test_input_callbacks.py", 90, 305)
        love.graphics.print("Press ESC to quit", 90, 470)
    except Exception:
        love.graphics.rectangle("line", 90, 245, 620, 250)


def love_keypressed(key, scancode, isrepeat):
    if key == "escape":
        love.event.quit()


def love_quit():
    pass

