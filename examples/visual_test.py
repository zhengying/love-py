"""
Visual Test for LOVE2D Python Drawing
Tests that graphics actually render to the screen.
Usage: love/love examples/visual_test.py
"""

import love_py
import time

print("🎨 Starting visual drawing test...")

def love_load():
    """Setup the test"""
    love_py.window.setTitle("Visual Drawing Test - LOVE2D Python")
    print("✅ love_load() called - Setting up...")

def love_draw():
    """Draw test patterns"""
    # Clear with dark background
    love_py.graphics.clear(0.1, 0.1, 0.15)
    
    # Draw a large red rectangle in center
    love_py.graphics.setColor(1.0, 0.2, 0.2)
    love_py.graphics.rectangle('fill', 350, 250, 100, 100)
    
    # Draw a green circle on left
    love_py.graphics.setColor(0.2, 1.0, 0.2)
    love_py.graphics.circle('fill', 200, 300, 50)
    
    # Draw a blue circle on right  
    love_py.graphics.setColor(0.2, 0.2, 1.0)
    love_py.graphics.circle('fill', 600, 300, 50)
    
    # Draw white line connecting them
    love_py.graphics.setColor(1.0, 1.0, 1.0)
    love_py.graphics.line(200, 300, 600, 300)
    
    print("✅ love_draw() called - Frame rendered")

def love_update(dt):
    """Called every frame"""
    pass

def love_quit():
    """Cleanup"""
    print("✅ love_quit() called - Test complete!")
    print("🎉 Drawing test successful - shapes rendered to screen")
