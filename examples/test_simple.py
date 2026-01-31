"""
Simple Test Game - Basic Rendering

This is a minimal test to verify the love module works correctly.
Run with: ./bin/love examples/test_simple.py
"""

import love

def love_load():
    print("Game loaded!")
    print("LOVE version:", love.getVersion())
    print("Version compatible (11.5.0):", love.isVersionCompatible("11.5.0"))
    print("Deprecation output (before):", love.hasDeprecationOutput())
    love.setDeprecationOutput(True)
    print("Deprecation output (after):", love.hasDeprecationOutput())
    love.window.setTitle("Simple Test")
    print("Window mode:", love.window.getMode())
    love.graphics.setBackgroundColor(0.1, 0.1, 0.15)

def love_update(dt):
    pass

def love_draw():
    # Clear and draw a simple rectangle
    love.graphics.clear()
    love.graphics.setColor(1.0, 0.0, 0.0)
    love.graphics.rectangle('fill', 350, 250, 100, 100)

def love_quit():
    print("Game quit!")
