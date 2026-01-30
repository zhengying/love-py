"""
Input Callbacks Test

Tests all input callbacks:
- love.keypressed(key, scancode, isrepeat)
- love.keyreleased(key, scancode)
- love.mousepressed(x, y, button, istouch, presses)
- love.mousereleased(x, y, button, istouch, presses)
- love.mousemoved(x, y, dx, dy, istouch)

Run with: ./bin/love examples/test_input_callbacks.py
Press ESC to quit
"""

import love

def love_load():
    print("=== Input Callbacks Test ===")
    print("Press any key or click mouse to test callbacks")
    print("Press ESC to quit")
    love.window.setTitle("Input Callbacks Test")

def love_update(dt):
    pass

def love_draw():
    love.graphics.clear(0.1, 0.1, 0.15)
    love.graphics.setColor(0, 1, 0)
    love.graphics.rectangle('fill', 350, 250, 100, 100)

# Input callbacks
def love_keypressed(key, scancode, isrepeat):
    print(f"Key pressed: key='{key}', scancode={scancode}, repeat={isrepeat}")
    if key == 'escape':
        love.event.quit()

def love_keyreleased(key, scancode):
    print(f"Key released: key='{key}', scancode={scancode}")

def love_mousepressed(x, y, button, istouch, presses):
    button_names = {1: 'left', 2: 'middle', 3: 'right'}
    button_name = button_names.get(button, f'button{button}')
    print(f"Mouse pressed: x={x}, y={y}, button={button_name} ({button}), presses={presses}")

def love_mousereleased(x, y, button, istouch, presses):
    button_names = {1: 'left', 2: 'middle', 3: 'right'}
    button_name = button_names.get(button, f'button{button}')
    print(f"Mouse released: x={x}, y={y}, button={button_name} ({button}), presses={presses}")

def love_mousemoved(x, y, dx, dy, istouch):
    # Only print every 10th move event to avoid spam
    if hasattr(love_mousemoved, 'counter'):
        love_mousemoved.counter += 1
    else:
        love_mousemoved.counter = 0
    
    if love_mousemoved.counter % 10 == 0:
        print(f"Mouse moved: x={x}, y={y}, dx={dx}, dy={dy}")

def love_quit():
    print("\nInput test ended!")
