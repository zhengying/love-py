"""
LOVE2D Python - Example Game

This is a simple example demonstrating the LOVE2D Python API.
Run with: python examples/basic_game.py
"""

import love

# Game state
player_x = 400
player_y = 300
player_speed = 200
player_color = (1.0, 0.2, 0.2)  # Red

circles = []
circle_timer = 0

def game_load():
    """Called once when the game starts."""
    print("Game starting...")
    print(f"LOVE Version: {love.getVersion()}")
    
    # Set up window
    love.window.set_mode(800, 600, fullscreen=False, resizable=True)
    love.window.set_title("LOVE2D Python Example")
    
    # Set background color
    love.graphics.set_background_color(0.1, 0.1, 0.15)


def game_update(dt):
    """Called every frame to update game logic."""
    global player_x, player_y, circle_timer
    
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
    
    # Spawn circles
    circle_timer += dt
    if circle_timer >= 1.0:
        circle_timer = 0
        import random
        circles.append({
            'x': random.randint(50, width - 50),
            'y': random.randint(50, height - 50),
            'r': random.randint(10, 30),
            'color': (
                random.random(),
                random.random(),
                random.random()
            )
        })
        # Limit number of circles
        if len(circles) > 20:
            circles.pop(0)


def game_draw():
    """Called every frame to draw the game."""
    # Draw circles
    for circle in circles:
        love.graphics.set_color(*circle['color'])
        love.graphics.circle('fill', circle['x'], circle['y'], circle['r'])
    
    # Draw player
    love.graphics.set_color(*player_color)
    love.graphics.rectangle('fill', player_x - 25, player_y - 25, 50, 50)
    
    # Draw FPS
    love.graphics.set_color(1, 1, 1)
    fps = love.timer.get_fps()
    # Note: Text drawing not yet implemented in foundation
    # love.graphics.print(f"FPS: {fps}", 10, 10)


def game_keypressed(key, scancode, isrepeat):
    """Called when a key is pressed."""
    if key == 'escape':
        love.event.quit()
    print(f"Key pressed: {key}")


def game_mousepressed(x, y, button, istouch, presses):
    """Called when mouse is clicked."""
    print(f"Mouse clicked at ({x}, {y}) with button {button}")
    # Add circle at click position
    import random
    circles.append({
        'x': x,
        'y': y,
        'r': random.randint(10, 30),
        'color': (
            random.random(),
            random.random(),
            random.random()
        )
    })


def game_quit():
    """Called when the game is quitting."""
    print("Game quitting...")
    return False  # Return True to cancel quit


# Set up callbacks
love.load = game_load
love.update = game_update
love.draw = game_draw
love.keypressed = game_keypressed
love.mousepressed = game_mousepressed
love.quit = game_quit

# Run the game
if __name__ == "__main__":
    try:
        love.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
