"""
Simple Test Game - Basic Rendering

This is a minimal test to verify the love module works correctly.
Run with: ./bin/love examples/test_simple.py
"""

import love

def love_load():
    print("Game loaded!")
    love.window.setTitle("Simple Test")
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
