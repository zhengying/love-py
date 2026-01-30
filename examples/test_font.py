"""
Font and Text Rendering Test

Tests:
- love.font.newFont(filename, size)
- font:getWidth(text)
- font:getHeight()
- love.graphics.setFont(font)
- love.graphics.getFont()
- love.graphics.print(text, x, y)
- love.graphics.newFont(filename, size) [convenience]

Run with: ./bin/love examples/test_font.py
Press ESC to quit
"""

import love
import os

font = None
test_results = []

def love_load():
    global font
    print("=== Font & Text Rendering Test ===\n")
    
    # Test 1: Load system font
    print("Test 1: Loading system font")
    try:
        # Try to load a system font
        font_path = "/System/Library/Fonts/Geneva.ttf"
        if love.filesystem.exists(font_path):
            font = love.font.newFont(font_path, 24)
            test_results.append(("Load font", True))
            print(f"  ✓ Font loaded: {font_path}")
        else:
            # Try alternative
            font_path = "/System/Library/Fonts/SFNSMono.ttf"
            if love.filesystem.exists(font_path):
                font = love.font.newFont(font_path, 24)
                test_results.append(("Load font", True))
                print(f"  ✓ Font loaded: {font_path}")
            else:
                test_results.append(("Load font", False))
                print(f"  ✗ No font file found")
                return
    except Exception as e:
        test_results.append(("Load font", False))
        print(f"  ✗ Error loading font: {e}")
        return
    
    # Test 2: Get font metrics
    print("\nTest 2: Font metrics")
    try:
        height = font.getHeight()
        test_results.append(("getHeight()", height > 0))
        print(f"  ✓ Font height: {height}")
        
        test_text = "Hello LOVE"
        width = font.getWidth(test_text)
        test_results.append(("getWidth()", width > 0))
        print(f"  ✓ Text width for '{test_text}': {width}")
    except Exception as e:
        test_results.append(("Font metrics", False))
        print(f"  ✗ Error: {e}")
    
    # Test 3: Set and get font
    print("\nTest 3: Set/get font")
    try:
        love.graphics.setFont(font)
        current_font = love.graphics.getFont()
        test_results.append(("setFont/getFont", current_font is not None))
        print(f"  ✓ Font set and retrieved successfully")
    except Exception as e:
        test_results.append(("setFont/getFont", False))
        print(f"  ✗ Error: {e}")
    
    # Test 4: graphics.newFont convenience function
    print("\nTest 4: graphics.newFont convenience")
    try:
        font2 = love.graphics.newFont(font_path, 16)
        test_results.append(("graphics.newFont", font2 is not None))
        print(f"  ✓ Created font via graphics.newFont()")
    except Exception as e:
        test_results.append(("graphics.newFont", False))
        print(f"  ✗ Error: {e}")
    
    print("\n=== Summary ===")
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    print(f"Passed: {passed}/{total}")
    
    for name, result in test_results:
        status = "✓" if result else "✗"
        print(f"  {status} {name}")
    
    print("\nWindow should show rendered text...")

def love_update(dt):
    pass

def love_draw():
    # Clear background
    love.graphics.clear(0.1, 0.1, 0.15)
    
    # Draw a green rectangle
    love.graphics.setColor(0, 1, 0)
    love.graphics.rectangle('fill', 350, 250, 100, 100)
    
    # Draw text if font is loaded
    if font:
        love.graphics.setColor(1, 1, 1)
        love.graphics.print("Hello LOVE2D!", x=50, y=50)
        love.graphics.print("Font Test", x=50, y=100)
        love.graphics.print("Press ESC to quit", x=50, y=550)

def love_keypressed(key, scancode, isrepeat):
    if key == 'escape':
        love.event.quit()

def love_quit():
    print("\nFont test ended!")
