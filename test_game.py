"""
LOVE2D Python - Test Game (Auto-quit after 5 seconds)
"""

import love
import sys

# Game state
player_x = 400
player_y = 300
player_speed = 200
circles = []
test_timer = 0

def game_load():
    print("Game starting...")
    print(f"LOVE Version: {love.getVersion()}")
    love.window.set_mode(800, 600, fullscreen=False, resizable=True)
    love.window.set_title("LOVE2D Python Test - Auto-quit in 5s")
    love.graphics.set_background_color(0.1, 0.1, 0.15)
    print("Window created successfully!")

def game_update(dt):
    global player_x, player_y, test_timer
    
    # Auto-quit after 5 seconds
    test_timer += dt
    if test_timer >= 5.0:
        print("Test complete - quitting automatically")
        love.event.quit()
    
    # Player movement
    if love.keyboard.is_down('left', 'a'):
        player_x -= player_speed * dt
    if love.keyboard.is_down('right', 'd'):
        player_x += player_speed * dt
    if love.keyboard.is_down('up', 'w'):
        player_y -= player_speed * dt
    if love.keyboard.is_down('down', 's'):
        player_y += player_speed * dt
    
    # Keep player on screen
    width, height = love.window.get_dimensions()
    player_x = max(25, min(width - 25, player_x))
    player_y = max(25, min(height - 25, player_y))

def game_draw():
    # Draw player (red square)
    love.graphics.set_color(1.0, 0.2, 0.2)
    love.graphics.rectangle('fill', player_x - 25, player_y - 25, 50, 50)
    
    # Draw circles
    for circle in circles:
        love.graphics.set_color(*circle['color'])
        love.graphics.circle('fill', circle['x'], circle['y'], circle['r'])

def game_mousepressed(x, y, button, istouch, presses):
    print(f"Mouse clicked at ({x}, {y})")
    import random
    circles.append({
        'x': x, 'y': y, 'r': random.randint(10, 30),
        'color': (random.random(), random.random(), random.random())
    })

def game_quit():
    print("Game quitting...")
    return False

# Set callbacks
love.load = game_load
love.update = game_update
love.draw = game_draw
love.mousepressed = game_mousepressed
love.quit = game_quit

# Run
if __name__ == "__main__":
    try:
        love.run()
        print("Game completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
