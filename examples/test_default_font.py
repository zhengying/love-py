"""
Simple Font Rendering Test with Default Font

This test uses the built-in default font from resources/font.ttf
so it doesn't depend on system fonts.

For pixel art fonts, use font:setFilter("nearest", "nearest")
For smooth fonts, use font:setFilter("linear", "linear") or leave as default
"""

import love

def love_load():
    print("=== Font Rendering Test with Default Font ===\n")
    
    # Get the default font (should be automatically created)
    font = love.graphics.getFont()
    if font:
        print("✓ Default font loaded successfully")
        print(f"  Font height: {font.getHeight()}")
        print(f"  Text width for 'Hello': {font.getWidth('Hello')}")
        
        # For pixel art fonts, use nearest neighbor filtering
        # This keeps the sharp edges and prevents distortion
        font.setFilter("nearest", "nearest")
        print("  ✓ Font filter set to 'nearest' for pixel-perfect rendering")
    else:
        print("✗ Failed to load default font")
    
    print("\nYou should see text rendered in the window.")
    print("Press ESC to quit.")

def love_draw():
    # Clear background
    love.graphics.clear(0.1, 0.1, 0.15)
    
    # Draw a green rectangle for reference
    love.graphics.setColor(0, 1, 0)
    love.graphics.rectangle('fill', 350, 250, 100, 100)
    
    # Draw text using the default font
    love.graphics.setColor(1, 1, 1)
    love.graphics.print("Hello LOVE2D!", 50, 50)
    love.graphics.print("Default Font Test", 50, 100)
    love.graphics.print("Font rendering should work now!", 50, 150)
    love.graphics.print("Press ESC to quit", 50, 550)

def love_keypressed(key, scancode, isrepeat):
    if key == 'escape':
        love.event.quit()
