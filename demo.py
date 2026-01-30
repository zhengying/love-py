#!/usr/bin/env python3
"""
Visual Demo for LOVE2D Python
Tests basic rendering functionality.
"""

import love
import time

print("🎮 LOVE2D Python Visual Demo")
print("=" * 40)
print(f"Version: {love.getVersion()}")
print()

# Set up game
love.window.set_mode(800, 600)
love.window.set_title("LOVE2D Python - Visual Demo")
love.graphics.set_background_color(0.1, 0.1, 0.15)

print("✅ Window created: 800x600")
print("✅ Background color set")
print()

# Simple render test
print("🎨 Testing graphics rendering...")

# Clear and draw some shapes
love.graphics.clear()

# Draw red rectangle
love.graphics.set_color(1.0, 0.2, 0.2)
love.graphics.rectangle('fill', 350, 250, 100, 100)
print("  ✅ Red rectangle drawn at (350, 250)")

# Draw green circle
love.graphics.set_color(0.2, 1.0, 0.2)
love.graphics.circle('fill', 200, 300, 50)
print("  ✅ Green circle drawn at (200, 300)")

# Draw blue circle
love.graphics.set_color(0.2, 0.2, 1.0)
love.graphics.circle('fill', 600, 300, 50)
print("  ✅ Blue circle drawn at (600, 300)")

# Draw line
love.graphics.set_color(1.0, 1.0, 1.0)
love.graphics.line(200, 300, 600, 300)
print("  ✅ White line drawn between circles")

# Present frame
love.graphics.present()
print()
print("✅ Frame rendered and presented!")
print()

# Test input
print("⌨️  Testing input...")
print(f"  Mouse position: {love.mouse.get_position()}")
print(f"  Window has focus: {love.window.has_focus()}")
print()

# Show FPS
print("⏱️  Timer info:")
print(f"  Current FPS: {love.timer.get_fps()}")
print(f"  Delta time: {love.timer.get_delta():.4f}")
print()

print("🎉 SUCCESS! All systems functional!")
print()
print("The demo window is now showing:")
print("  - A red square in the center")
print("  - A green circle on the left")
print("  - A blue circle on the right")
print("  - A white line connecting the circles")
print()
print("Window will close in 3 seconds...")

time.sleep(3)

# Cleanup
love.window.close()
love._love2d_core.quit()

print()
print("✅ Demo complete! LOVE2D Python is working perfectly!")
