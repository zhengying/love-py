"""
Test configuration and fixtures for LOVE2D Python tests.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import love
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture
def love():
    """Fixture to provide the love module."""
    import love as love_module
    return love_module


@pytest.fixture
def initialized_love(love):
    """Fixture that provides an initialized LOVE2D instance."""
    if not love._love2d_core.init():
        pytest.skip("LOVE2D initialization failed")
    
    yield love
    
    # Cleanup
    love._love2d_core.quit()


@pytest.fixture
def temp_window(initialized_love):
    """Fixture that creates a temporary window for testing."""
    # Create a small test window (hidden if possible, but macOS doesn't support that easily)
    success = initialized_love.window.set_mode(100, 100)
    if not success:
        pytest.skip("Failed to create test window")
    
    yield initialized_love
    
    # Cleanup
    initialized_love.window.close()


@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup after each test to ensure clean state."""
    yield
    # Any global cleanup can go here
    pass


class CallbackTracker:
    """Helper class to track callback invocations."""
    
    def __init__(self):
        self.calls = []
        self.load_called = False
        self.update_calls = []
        self.draw_calls = []
        self.quit_called = False
        self.keypressed_calls = []
        self.keyreleased_calls = []
        self.mousepressed_calls = []
        self.mousereleased_calls = []
        self.mousemoved_calls = []
    
    def load(self):
        self.load_called = True
        self.calls.append(('load',))
    
    def update(self, dt):
        self.update_calls.append(dt)
        self.calls.append(('update', dt))
    
    def draw(self):
        self.draw_calls.append(True)
        self.calls.append(('draw',))
    
    def quit(self):
        self.quit_called = True
        self.calls.append(('quit',))
        return False
    
    def keypressed(self, key, scancode, isrepeat):
        self.keypressed_calls.append((key, scancode, isrepeat))
        self.calls.append(('keypressed', key, scancode, isrepeat))
    
    def keyreleased(self, key, scancode):
        self.keyreleased_calls.append((key, scancode))
        self.calls.append(('keyreleased', key, scancode))
    
    def mousepressed(self, x, y, button, istouch, presses):
        self.mousepressed_calls.append((x, y, button, istouch, presses))
        self.calls.append(('mousepressed', x, y, button, istouch, presses))
    
    def mousereleased(self, x, y, button, istouch, presses):
        self.mousereleased_calls.append((x, y, button, istouch, presses))
        self.calls.append(('mousereleased', x, y, button, istouch, presses))
    
    def mousemoved(self, x, y, dx, dy, istouch):
        self.mousemoved_calls.append((x, y, dx, dy, istouch))
        self.calls.append(('mousemoved', x, y, dx, dy, istouch))


@pytest.fixture
def callback_tracker():
    """Fixture to provide a callback tracker."""
    return CallbackTracker()
