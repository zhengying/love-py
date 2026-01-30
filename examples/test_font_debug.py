"""
Font Debug Test - Shows individual glyphs to isolate rendering issues
"""

import love

font = None

def love_load():
    global font
    print("=== Font Debug Test ===\n")
    
    # Load font at larger size for easier debugging
    font = love.font.newFont("examples/font/ubuntu-mono.ttf", 48)
    love.graphics.setFont(font)
    
    print(f"Font height: {font.getHeight()}")
    print(f"'A' width: {font.getWidth('A')}")
    print(f"'a' width: {font.getWidth('a')}")
    print("\nRendering individual characters...")

def love_draw():
    love.graphics.clear(0.1, 0.1, 0.15)
    
    # Draw reference rectangles
    love.graphics.setColor(0.2, 0.2, 0.2)
    love.graphics.rectangle('line', 10, 10, 100, 100)
    love.graphics.rectangle('line', 120, 10, 100, 100)
    
    # Test drawing single characters at large size
    love.graphics.setColor(1, 1, 1)
    
    # Draw 'A' - should be clear and crisp
    love.graphics.print("A", 50, 50)
    
    # Draw 'a' 
    love.graphics.print("a", 160, 50)
    
    # Draw 'B'
    love.graphics.print("B", 50, 120)
    
    # Draw space between letters
    love.graphics.print("AB", 50, 190)
    
    # Test the full alphabet
    love.graphics.print("ABCDEF", 50, 260)
    love.graphics.print("abcdef", 50, 330)
    
    # Test numbers
    love.graphics.print("123456", 50, 400)
    
    # Instructions
    love.graphics.setColor(0.5, 0.5, 0.5)
    love.graphics.print("Press ESC to quit", 50, 550)

def love_keypressed(key, scancode, isrepeat):
    if key == 'escape':
        love.event.quit()
