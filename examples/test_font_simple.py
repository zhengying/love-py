"""
Simple Font Test - Using positional arguments
"""
import love

font = None

def love_load():
    global font
    print("Loading font...")
    font = love.font.newFont("/System/Library/Fonts/Geneva.ttf", 24)
    love.graphics.setFont(font)
    print(f"Font loaded, height: {font.getHeight()}")

def love_draw():
    love.graphics.clear(0.1, 0.1, 0.2)
    love.graphics.setColor(1, 1, 1)
    # Use positional arguments
    love.graphics.print("Hello LOVE2D!", 50, 50)
    love.graphics.print("Font Test", 50, 100)
    love.graphics.print("Press ESC", 50, 550)

def love_keypressed(key, scancode, isrepeat):
    if key == 'escape':
        love.event.quit()

def love_quit():
    print("Test ended!")
