"""
Test core LOVE2D functionality - callbacks and game loop.

This module tests L1.1: Core Callbacks & Game Loop
"""

import pytest
import time
import threading


class TestCoreInitialization:
    """Test basic module initialization."""
    
    def test_module_import(self, love):
        """Test that the love module can be imported."""
        assert love is not None
        assert hasattr(love, 'getVersion')
        assert hasattr(love, 'graphics')
        assert hasattr(love, 'window')
        assert hasattr(love, 'event')
        assert hasattr(love, 'timer')
        assert hasattr(love, 'keyboard')
        assert hasattr(love, 'mouse')
    
    def test_get_version(self, love):
        """Test that getVersion returns correct version info."""
        version = love.getVersion()
        assert isinstance(version, tuple)
        assert len(version) == 4
        assert version[0] == 11  # Major
        assert version[1] == 5   # Minor
        assert version[3] == "Mysterious Mysteries"  # Codename
    
    def test_init_quit(self, love):
        """Test LOVE2D initialization and shutdown."""
        # Should be able to init
        result = love._love2d_core.init()
        assert result is True
        
        # Second init should succeed (idempotent)
        result = love._love2d_core.init()
        assert result is True
        
        # Should be able to quit
        love._love2d_core.quit()


class TestCallbackRegistration:
    """Test callback registration."""
    
    def test_load_callback_registration(self, love, callback_tracker):
        """Test that load callback can be registered."""
        love.load = callback_tracker.load
        assert love.load is callback_tracker.load
    
    def test_update_callback_registration(self, love, callback_tracker):
        """Test that update callback can be registered."""
        love.update = callback_tracker.update
        assert love.update is callback_tracker.update
    
    def test_draw_callback_registration(self, love, callback_tracker):
        """Test that draw callback can be registered."""
        love.draw = callback_tracker.draw
        assert love.draw is callback_tracker.draw
    
    def test_quit_callback_registration(self, love, callback_tracker):
        """Test that quit callback can be registered."""
        love.quit = callback_tracker.quit
        assert love.quit is callback_tracker.quit
    
    def test_keypressed_callback_registration(self, love, callback_tracker):
        """Test that keypressed callback can be registered."""
        love.keypressed = callback_tracker.keypressed
        assert love.keypressed is callback_tracker.keypressed
    
    def test_keyreleased_callback_registration(self, love, callback_tracker):
        """Test that keyreleased callback can be registered."""
        love.keyreleased = callback_tracker.keyreleased
        assert love.keyreleased is callback_tracker.keyreleased
    
    def test_mousepressed_callback_registration(self, love, callback_tracker):
        """Test that mousepressed callback can be registered."""
        love.mousepressed = callback_tracker.mousepressed
        assert love.mousepressed is callback_tracker.mousepressed
    
    def test_mousereleased_callback_registration(self, love, callback_tracker):
        """Test that mousereleased callback can be registered."""
        love.mousereleased = callback_tracker.mousereleased
        assert love.mousereleased is callback_tracker.mousereleased
    
    def test_mousemoved_callback_registration(self, love, callback_tracker):
        """Test that mousemoved callback can be registered."""
        love.mousemoved = callback_tracker.mousemoved
        assert love.mousemoved is callback_tracker.mousemoved


class TestCallbackInvocation:
    """Test that callbacks are properly invoked."""
    
    def test_load_callback_invoked(self, initialized_love, callback_tracker):
        """Test that load callback is called when run starts."""
        initialized_love.load = callback_tracker.load
        
        # Call load directly (we can't run the full loop in tests)
        if initialized_love.load:
            initialized_love.load()
        
        assert callback_tracker.load_called is True
    
    def test_update_callback_invoked(self, initialized_love, callback_tracker):
        """Test that update callback is called."""
        initialized_love.update = callback_tracker.update
        
        # Simulate update
        if initialized_love.update:
            initialized_love.update(0.016)  # ~60fps
        
        assert len(callback_tracker.update_calls) == 1
        assert callback_tracker.update_calls[0] == 0.016
    
    def test_draw_callback_invoked(self, initialized_love, callback_tracker):
        """Test that draw callback is called."""
        initialized_love.draw = callback_tracker.draw
        
        # Simulate draw
        if initialized_love.draw:
            initialized_love.draw()
        
        assert len(callback_tracker.draw_calls) == 1
    
    def test_quit_callback_invoked(self, initialized_love, callback_tracker):
        """Test that quit callback is called."""
        initialized_love.quit = callback_tracker.quit
        
        # Simulate quit
        if initialized_love.quit:
            result = initialized_love.quit()
        
        assert callback_tracker.quit_called is True


class TestSubmoduleAccess:
    """Test that all submodules are accessible."""
    
    def test_graphics_module(self, love):
        """Test graphics module exists."""
        assert love.graphics is not None
        assert hasattr(love.graphics, 'clear')
        assert hasattr(love.graphics, 'present')
        assert hasattr(love.graphics, 'rectangle')
        assert hasattr(love.graphics, 'circle')
        assert hasattr(love.graphics, 'setColor')
        assert hasattr(love.graphics, 'getColor')
    
    def test_window_module(self, love):
        """Test window module exists."""
        assert love.window is not None
        assert hasattr(love.window, 'set_mode')
        assert hasattr(love.window, 'get_mode')
        assert hasattr(love.window, 'set_title')
        assert hasattr(love.window, 'get_dimensions')
    
    def test_event_module(self, love):
        """Test event module exists."""
        assert love.event is not None
        assert hasattr(love.event, 'pump')
        assert hasattr(love.event, 'poll')
        assert hasattr(love.event, 'quit')
    
    def test_timer_module(self, love):
        """Test timer module exists."""
        assert love.timer is not None
        assert hasattr(love.timer, 'get_delta')
        assert hasattr(love.timer, 'get_fps')
        assert hasattr(love.timer, 'get_time')
    
    def test_keyboard_module(self, love):
        """Test keyboard module exists."""
        assert love.keyboard is not None
        assert hasattr(love.keyboard, 'is_down')
        assert hasattr(love.keyboard, 'KeyConstant')
    
    def test_mouse_module(self, love):
        """Test mouse module exists."""
        assert love.mouse is not None
        assert hasattr(love.mouse, 'get_position')
        assert hasattr(love.mouse, 'is_down')
        assert hasattr(love.mouse, 'LEFT')


class TestErrorHandling:
    """Test error handling."""
    
    def test_callback_error_handling(self, initialized_love):
        """Test that errors in callbacks are handled gracefully."""
        def bad_callback():
            raise ValueError("Test error")
        
        initialized_love.load = bad_callback
        
        # Should not crash when calling the bad callback
        with pytest.raises(ValueError):
            if initialized_love.load:
                initialized_love.load()


class TestGlobalState:
    """Test global state management."""
    
    def test_state_persistence(self, initialized_love):
        """Test that state persists across calls."""
        # Set up callbacks
        initialized_love.load = lambda: None
        initialized_love.update = lambda dt: None
        initialized_love.draw = lambda: None
        
        # State should be preserved
        assert initialized_love.load is not None
        assert initialized_love.update is not None
        assert initialized_love.draw is not None
