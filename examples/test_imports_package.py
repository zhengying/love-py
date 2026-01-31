"""
Import Package Test

Verifies that a game script can import a package (a directory module).
Run with: ./bin/love examples/test_imports_package.py
"""

import love

from pkg_demo import add
from pkg_demo.math_utils import add as add2

elapsed = 0.0


def love_load():
    print("=== Import Package Test ===")
    print("pkg_demo.add(2, 3) =", add(2, 3))
    print("pkg_demo.math_utils.add(10, 20) =", add2(10, 20))
    love.window.setTitle("Import Package Test (Auto-quit)")


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
    print("Import package test ended!")
