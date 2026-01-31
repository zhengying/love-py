"""
Import Test

Verifies that a game script can import sibling Python modules.
Run with: ./bin/love examples/test_imports.py
"""

import love

import import_helper

elapsed = 0.0


def love_load():
    print("=== Import Test ===")
    print(import_helper.get_message())
    love.window.setTitle("Import Test (Auto-quit)")


def love_update(dt):
    global elapsed
    elapsed += dt
    if elapsed >= 0.2:
        love.event.quit()


def love_draw():
    love.graphics.clear(0.1, 0.1, 0.15)
    love.graphics.setColor(0, 1, 0)
    love.graphics.rectangle("fill", 350, 250, 100, 100)


def love_quit():
    print("Import test ended!")
