"""
Font Rendering Test with Ubuntu Mono

This test uses a proper TTF font (Ubuntu Mono) to check if rendering issues
are specific to the pixel art font or a general problem.
"""

import love

font = None

def love_load():
    global font
    print("=== Font Rendering Test with Ubuntu Mono ===\n")
    
    try:
        # Load Ubuntu Mono font
        font = love.font.newFont("examples/font/ubuntu-mono.ttf", 24)
        print("✓ Ubuntu Mono font loaded successfully")
        print(f"  Font height: {font.getHeight()}")
        print(f"  Text width for 'Hello': {font.getWidth('Hello')}")
        
        # Set the font for rendering
        love.graphics.setFont(font)
        print("  ✓ Font set for rendering")
    except Exception as e:
        print(f"✗ Error loading font: {e}")
        font = None
    
    print("\nYou should see text rendered in the window.")
    print("Press ESC to quit.")

def love_draw():
    # Clear background
    love.graphics.clear(0.1, 0.1, 0.15)
    
    # Draw a green rectangle for reference
    love.graphics.setColor(0, 1, 0)
    love.graphics.rectangle('fill', 350, 250, 100, 100)
    
    # Draw text using Ubuntu Mono font
    love.graphics.setColor(1, 1, 1)
    if font:
        love.graphics.print("Hello LOVE2D!", 50, 50)
        love.graphics.print("Ubuntu Mono Font Test", 50, 100)
        love.graphics.print("Testing with different font", 50, 150)
        love.graphics.print("Press ESC to quit", 50, 550)

def love_keypressed(key, scancode, isrepeat):
    if key == 'escape':
        love.event.quit()
