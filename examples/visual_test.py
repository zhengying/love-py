"""
Visual Test - Shows window for 3 seconds

Run with: ./bin/love examples/visual_test.py
Press ESC to quit early
"""

import love

time = 0

def love_load():
    print("Visual Test Loaded!")
    print("Press ESC to quit")
    love.window.setTitle("Visual Test - 3 second demo")
    love.graphics.setBackgroundColor(0.1, 0.1, 0.2)

def love_update(dt):
    global time
    time += dt
    
    # Quit after 3 seconds
    if time > 3.0:
        print(f"Test complete! Ran for {time:.1f} seconds")
        love.event.quit()

def love_draw():
    # Clear with background color
    love.graphics.clear()
    
    # Draw a red rectangle in the center
    love.graphics.setColor(1.0, 0.2, 0.2)
    love.graphics.rectangle('fill', 350, 250, 100, 100)
    
    # Draw a green circle on the left
    love.graphics.setColor(0.2, 1.0, 0.2)
    love.graphics.circle('fill', 200, 300, 50)
    
    # Draw a blue circle on the right  
    love.graphics.setColor(0.2, 0.2, 1.0)
    love.graphics.circle('fill', 600, 300, 50)
    
    # Draw a white line connecting them
    love.graphics.setColor(1.0, 1.0, 1.0)
    love.graphics.line(200, 300, 600, 300)

def love_quit():
    print("Visual Test Ended")
