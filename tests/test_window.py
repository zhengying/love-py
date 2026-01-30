"""
Test window module functionality.

Tests L1.2: Window Management
"""

import pytest


class TestWindowCreation:
    """Test window creation and management."""
    
    def test_set_mode_returns_bool(self, initialized_love):
        """Test that set_mode returns a boolean."""
        result = initialized_love.window.set_mode(800, 600)
        assert isinstance(result, bool)
    
    def test_set_mode_creates_window(self, initialized_love):
        """Test that set_mode creates a window."""
        result = initialized_love.window.set_mode(800, 600)
        assert result is True
        
        # Clean up
        initialized_love.window.close()
    
    def test_set_mode_with_flags(self, initialized_love):
        """Test window creation with various flags."""
        result = initialized_love.window.set_mode(
            800, 600,
            fullscreen=False,
            resizable=True,
            borderless=False
        )
        assert result is True
        
        # Clean up
        initialized_love.window.close()
    
    def test_set_mode_multiple_times(self, initialized_love):
        """Test that set_mode can be called multiple times."""
        # First window
        result1 = initialized_love.window.set_mode(800, 600)
        assert result1 is True
        
        # Second window (should resize/replace)
        result2 = initialized_love.window.set_mode(1024, 768)
        assert result2 is True
        
        # Clean up
        initialized_love.window.close()
    
    def test_close_window(self, initialized_love):
        """Test that close properly closes the window."""
        initialized_love.window.set_mode(800, 600)
        initialized_love.window.close()
        
        # Should be able to create another window after closing
        result = initialized_love.window.set_mode(800, 600)
        assert result is True
        
        initialized_love.window.close()


class TestWindowProperties:
    """Test window property getters and setters."""
    
    def test_set_and_get_title(self, temp_window):
        """Test setting and getting window title."""
        temp_window.window.set_title("Test Title")
        title = temp_window.window.get_title()
        assert title == "Test Title"
    
    def test_set_title_unicode(self, temp_window):
        """Test setting title with unicode characters."""
        temp_window.window.set_title("测试 🎮")
        title = temp_window.window.get_title()
        assert "测试" in title
    
    def test_set_title_empty(self, temp_window):
        """Test setting empty title."""
        temp_window.window.set_title("")
        title = temp_window.window.get_title()
        assert title == ""
    
    def test_get_dimensions(self, temp_window):
        """Test getting window dimensions."""
        width, height = temp_window.window.get_dimensions()
        assert isinstance(width, int)
        assert isinstance(height, int)
        assert width > 0
        assert height > 0
    
    def test_get_width(self, temp_window):
        """Test getting window width."""
        width = temp_window.window.get_width()
        assert isinstance(width, int)
        assert width > 0
    
    def test_get_height(self, temp_window):
        """Test getting window height."""
        height = temp_window.window.get_height()
        assert isinstance(height, int)
        assert height > 0
    
    def test_get_mode(self, temp_window):
        """Test getting window mode."""
        mode = temp_window.window.get_mode()
        assert isinstance(mode, tuple)
        assert len(mode) == 3
        
        width, height, flags = mode
        assert isinstance(width, int)
        assert isinstance(height, int)
        assert isinstance(flags, dict)
    
    def test_mode_flags_structure(self, temp_window):
        """Test that mode flags is a proper dictionary."""
        width, height, flags = temp_window.window.get_mode()
        
        # Should have expected keys
        assert isinstance(flags.get('fullscreen'), bool)
        assert isinstance(flags.get('resizable'), bool)
        assert isinstance(flags.get('borderless'), bool)
        assert isinstance(flags.get('vsync'), int)


class TestFullscreen:
    """Test fullscreen functionality."""
    
    def test_set_fullscreen(self, temp_window):
        """Test setting fullscreen mode."""
        # Note: This might not actually work in headless/test environments
        temp_window.window.set_fullscreen(True)
        is_fullscreen = temp_window.window.get_fullscreen()
        
        # Should return a boolean
        assert isinstance(is_fullscreen, bool)
    
    def test_unset_fullscreen(self, temp_window):
        """Test unsetting fullscreen mode."""
        temp_window.window.set_fullscreen(False)
        is_fullscreen = temp_window.window.get_fullscreen()
        
        assert isinstance(is_fullscreen, bool)


class TestVSync:
    """Test vsync functionality."""
    
    def test_set_vsync(self, temp_window):
        """Test setting vsync."""
        temp_window.window.set_vsync(1)
        vsync = temp_window.window.get_vsync()
        assert isinstance(vsync, int)
    
    def test_disable_vsync(self, temp_window):
        """Test disabling vsync."""
        temp_window.window.set_vsync(0)
        vsync = temp_window.window.get_vsync()
        assert isinstance(vsync, int)


class TestFocus:
    """Test window focus detection."""
    
    def test_has_focus(self, temp_window):
        """Test has_focus returns boolean."""
        focus = temp_window.window.has_focus()
        assert isinstance(focus, bool)
    
    def test_has_mouse_focus(self, temp_window):
        """Test has_mouse_focus returns boolean."""
        mouse_focus = temp_window.window.has_mouse_focus()
        assert isinstance(mouse_focus, bool)


class TestWindowEdgeCases:
    """Test window edge cases and error handling."""
    
    def test_zero_size_window(self, initialized_love):
        """Test that zero-size window is handled gracefully."""
        # This should either fail gracefully or be handled
        try:
            result = initialized_love.window.set_mode(0, 0)
            # If it succeeds, that's fine
            initialized_love.window.close()
        except Exception:
            # If it raises, that's also acceptable
            pass
    
    def test_negative_size_window(self, initialized_love):
        """Test that negative-size window is handled gracefully."""
        try:
            result = initialized_love.window.set_mode(-100, -100)
            initialized_love.window.close()
        except Exception:
            pass
    
    def test_very_large_window(self, initialized_love):
        """Test very large window dimensions."""
        try:
            result = initialized_love.window.set_mode(10000, 10000)
            # Might fail due to hardware limitations
            if result:
                initialized_love.window.close()
        except Exception:
            # Expected to potentially fail
            pass
    
    def test_get_dimensions_without_window(self, initialized_love):
        """Test getting dimensions before window creation."""
        # Should return default values or reasonable defaults
        width, height = initialized_love.window.get_dimensions()
        assert isinstance(width, int)
        assert isinstance(height, int)


class TestWindowModuleAliases:
    """Test that Pythonic aliases work."""
    
    def test_set_mode_alias(self, temp_window):
        """Test set_mode function exists."""
        assert hasattr(temp_window.window, 'set_mode')
        assert hasattr(temp_window.window, 'setMode')  # Original name
    
    def test_get_dimensions_alias(self, temp_window):
        """Test get_dimensions function exists."""
        assert hasattr(temp_window.window, 'get_dimensions')
        assert hasattr(temp_window.window, 'getDimensions')
    
    def test_set_title_alias(self, temp_window):
        """Test set_title function exists."""
        assert hasattr(temp_window.window, 'set_title')
        assert hasattr(temp_window.window, 'setTitle')
