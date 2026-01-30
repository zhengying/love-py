"""
Simple LOVE2D Python Game

This is the proper way - C++ runs the main loop, Python provides callbacks.
Usage: ./love examples/simple_game.py
"""

import love_py  # The graphics/window API provided by C++

# Game state
player_x = 400
player_y = 300
player_speed = 200
circles = []
circle_timer = 0

def love_load():
    """Called once when the game starts."""
    print("Game loading...")
    # Window is already created by C++, but we can configure it
    love_py.window.set_title("LOVE2D Python - Simple Game")
    love_py.graphics.set_background_color(0.1, 0.1, 0.15)
    print("Game loaded!")

def love_update(dt):
    """Called every frame."""
    global player_x, player_y, circle_timer
    
    # Get keyboard state
    if love_py.keyboard.is_down('left', 'a'):
        player_x -= player_speed * dt
    if love_py.keyboard.is_down('right', 'd'):
        player_x += player_speed * dt
    if love_py.keyboard.is_down('up', 'w'):
        player_y -= player_speed * dt
    if love_py.keyboard.is_down('down', 's'):
        player_y += player_speed * dt
    
    # Keep on screen
    width, height = love_py.window.get_dimensions()
    player_x = max(25, min(width - 25, player_x))
    player_y = max(25, min(height - 25, player_y))
    
    # Spawn circles
    circle_timer += dt
    if circle_timer >= 1.0:
        circle_timer = 0
        import random
        circles.append({
            'x': random.randint(50, width - 50),
            'y': random.randint(50, height - 50),
            'r': random.randint(10, 30),
            'color': (random.random(), random.random(), random.random())
        })
        if len(circles) > 20:
            circles.pop(0)

def love_draw():
    """Called every frame to draw."""
    # Clear is done by C++, but we can set background color
    love_py.graphics.clear(0.1, 0.1, 0.15)
    
    # Draw circles
    for circle in circles:
        love_py.graphics.set_color(*circle['color'])
        love_py.graphics.circle('fill', circle['x'], circle['y'], circle['r'])
    
    # Draw player
    love_py.graphics.set_color(1.0, 0.2, 0.2)
    love_py.graphics.rectangle('fill', player_x - 25, player_y - 25, 50, 50)
    
    # Draw FPS
    love_py.graphics.set_color(1, 1, 1)
    # Text drawing would go here when implemented

def love_keypressed(key, scancode, isrepeat):
    """Called when a key is pressed."""
    if key == 'escape':
        print("ESC pressed - game will quit")
    print(f"Key pressed: {key}")

def love_mousepressed(x, y, button, istouch, presses):
    """Called when mouse is clicked."""
    print(f"Mouse clicked at ({x}, {y}) with button {button}")
    import random
    circles.append({
        'x': x,
        'y': y,
        'r': random.randint(10, 30),
        'color': (random.random(), random.random(), random.random())
    })

def love_quit():
    """Called when the game is quitting."""
    print("Game quitting...")
