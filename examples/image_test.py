"""
Image Loading Test for LOVE2D Python

This example tests loading and displaying an image.
Since we don't have an image file, we'll create a simple one programmatically first.

Usage: love/love examples/image_test.py
"""

import love_py
import os

# Create a simple test image (1x1 red pixel PNG) if it doesn't exist
def create_test_image():
    # Use the pre-created test image in examples directory
    filename = "examples/test_image.png"
    if os.path.exists(filename):
        print(f"Using test image: {filename}")
        return filename
    
    # Fallback: try to create one in current directory
    filename = "test_image.png"
    if not os.path.exists(filename):
        # Try to create a simple PNG using Python's PIL if available
        try:
            from PIL import Image
            img = Image.new('RGBA', (100, 100), (255, 0, 0, 255))  # Red
            img.save(filename)
            print(f"Created test image: {filename}")
            return filename
        except ImportError:
            print("PIL not available, please provide a PNG image named 'test_image.png'")
            return None
    return filename

# Game state
test_image = None
image_loaded = False

def love_load():
    """Called once when the game starts."""
    global test_image, image_loaded
    
    print("🎮 Image Loading Test")
    print("=" * 40)
    
    love_py.window.setTitle("LOVE2D Python - Image Test")
    love_py.graphics.setBackgroundColor(0.1, 0.1, 0.15)
    
    # Create or find test image
    filename = create_test_image()
    
    if filename and os.path.exists(filename):
        try:
            print(f"Loading image: {filename}")
            test_image = love_py.newImage(filename)
            image_loaded = True
            print(f"✅ Image loaded successfully!")
            print(f"   Size: {test_image.getWidth()}x{test_image.getHeight()}")
        except Exception as e:
            print(f"❌ Failed to load image: {e}")
            image_loaded = False
    else:
        print("⚠️  No test image available")
        print("   Place a PNG file named 'test_image.png' in the game directory")

def love_update(dt):
    """Called every frame."""
    pass

def love_draw():
    """Called every frame to draw."""
    # Clear screen
    love_py.graphics.clear(0.1, 0.1, 0.15)
    
    if image_loaded and test_image:
        # Draw the loaded image at position (350, 250) - center of 800x600
        love_py.graphics.setColor(1, 1, 1)  # White (no tint)
        love_py.image.draw(test_image, 350, 250)
        
        # Draw some text instructions (using shapes for now)
        love_py.graphics.setColor(1, 1, 1)
        love_py.graphics.rectangle('fill', 300, 50, 200, 30)  # Placeholder for text box
    else:
        # Draw error message placeholder
        love_py.graphics.setColor(1, 0.2, 0.2)
        love_py.graphics.rectangle('fill', 250, 275, 300, 50)  # Red box for error
        
        # Draw white text box
        love_py.graphics.setColor(1, 1, 1)
        love_py.graphics.rectangle('line', 250, 275, 300, 50)

def love_quit():
    """Called when the game is quitting."""
    print("\n✅ Image test complete!")
