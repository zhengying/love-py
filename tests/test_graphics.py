"""
Test graphics module functionality.

Tests L1.3: Graphics - Basic Drawing
"""

import pytest


class TestGraphicsBasic:
    """Test basic graphics operations."""
    
    def test_clear_function_exists(self, love):
        """Test that clear function exists."""
        assert hasattr(love.graphics, 'clear')
    
    def test_present_function_exists(self, love):
        """Test that present function exists."""
        assert hasattr(love.graphics, 'present')


class TestColorFunctions:
    """Test color getting and setting."""
    
    def test_set_color_basic(self, temp_window):
        """Test setting color with RGBA."""
        temp_window.graphics.set_color(1.0, 0.0, 0.0, 1.0)
        # Should not raise
    
    def test_set_color_without_alpha(self, temp_window):
        """Test setting color without alpha (should default to 1.0)."""
        temp_window.graphics.set_color(0.0, 1.0, 0.0)
        # Should not raise
    
    def test_get_color(self, temp_window):
        """Test getting current color."""
        temp_window.graphics.set_color(1.0, 0.5, 0.25, 0.8)
        color = temp_window.graphics.get_color()
        
        assert isinstance(color, tuple)
        assert len(color) == 4
        
        r, g, b, a = color
        assert isinstance(r, float)
        assert isinstance(g, float)
        assert isinstance(b, float)
        assert isinstance(a, float)
    
    def test_color_values_preserved(self, temp_window):
        """Test that color values are preserved."""
        temp_window.graphics.set_color(0.1, 0.2, 0.3, 0.4)
        r, g, b, a = temp_window.graphics.get_color()
        
        assert abs(r - 0.1) < 0.01
        assert abs(g - 0.2) < 0.01
        assert abs(b - 0.3) < 0.01
        assert abs(a - 0.4) < 0.01
    
    def test_set_background_color(self, temp_window):
        """Test setting background color."""
        temp_window.graphics.set_background_color(0.1, 0.1, 0.1, 1.0)
        # Should not raise
    
    def test_get_background_color(self, temp_window):
        """Test getting background color."""
        temp_window.graphics.set_background_color(0.5, 0.5, 0.5, 1.0)
        color = temp_window.graphics.get_background_color()
        
        assert isinstance(color, tuple)
        assert len(color) == 4
    
    def test_color_clamping(self, temp_window):
        """Test that color values are handled correctly at boundaries."""
        # Test values above 1.0
        temp_window.graphics.set_color(2.0, 1.5, 1.2, 1.0)
        
        # Test negative values
        temp_window.graphics.set_color(-0.5, -0.1, 0.0, 1.0)
        # Should handle gracefully (either clamp or accept)


class TestShapeDrawing:
    """Test shape drawing functions."""
    
    def test_rectangle_fill(self, temp_window):
        """Test drawing filled rectangle."""
        temp_window.graphics.rectangle('fill', 10, 10, 50, 50)
        # Should not raise
    
    def test_rectangle_line(self, temp_window):
        """Test drawing outlined rectangle."""
        temp_window.graphics.rectangle('line', 10, 10, 50, 50)
        # Should not raise
    
    def test_rectangle_invalid_mode(self, temp_window):
        """Test rectangle with invalid mode."""
        with pytest.raises((ValueError, RuntimeError)):
            temp_window.graphics.rectangle('invalid', 10, 10, 50, 50)
    
    def test_circle_fill(self, temp_window):
        """Test drawing filled circle."""
        temp_window.graphics.circle('fill', 100, 100, 25)
        # Should not raise
    
    def test_circle_line(self, temp_window):
        """Test drawing outlined circle."""
        temp_window.graphics.circle('line', 100, 100, 25)
        # Should not raise
    
    def test_line_basic(self, temp_window):
        """Test drawing a line."""
        temp_window.graphics.line(0, 0, 100, 100)
        # Should not raise


class TestTransformations:
    """Test graphics transformations."""
    
    def test_push_pop(self, temp_window):
        """Test push and pop operations."""
        temp_window.graphics.push()
        temp_window.graphics.pop()
        # Should not raise
    
    def test_origin(self, temp_window):
        """Test origin reset."""
        temp_window.graphics.origin()
        # Should not raise
    
    def test_translate(self, temp_window):
        """Test translation."""
        temp_window.graphics.translate(10, 20)
        # Should not raise
    
    def test_rotate(self, temp_window):
        """Test rotation."""
        temp_window.graphics.rotate(3.14159 / 4)  # 45 degrees
        # Should not raise
    
    def test_scale(self, temp_window):
        """Test scaling."""
        temp_window.graphics.scale(2.0, 2.0)
        # Should not raise
    
    def test_transform_stack(self, temp_window):
        """Test transform stack with multiple operations."""
        temp_window.graphics.push()
        temp_window.graphics.translate(10, 10)
        temp_window.graphics.rotate(0.5)
        temp_window.graphics.scale(1.5, 1.5)
        temp_window.graphics.pop()
        # Should not raise


class TestDimensions:
    """Test getting graphics dimensions."""
    
    def test_get_width(self, temp_window):
        """Test getting graphics width."""
        width = temp_window.graphics.get_width()
        assert isinstance(width, int)
        assert width > 0
    
    def test_get_height(self, temp_window):
        """Test getting graphics height."""
        height = temp_window.graphics.get_height()
        assert isinstance(height, int)
        assert height > 0
    
    def test_get_dimensions(self, temp_window):
        """Test getting both dimensions."""
        dims = temp_window.graphics.get_dimensions()
        assert isinstance(dims, tuple)
        assert len(dims) == 2
        
        width, height = dims
        assert isinstance(width, int)
        assert isinstance(height, int)
        assert width > 0
        assert height > 0
    
    def test_dimensions_match_window(self, temp_window):
        """Test that graphics dimensions match window dimensions."""
        g_width, g_height = temp_window.graphics.get_dimensions()
        w_width, w_height = temp_window.window.get_dimensions()
        
        assert g_width == w_width
        assert g_height == w_height


class TestClear:
    """Test screen clearing."""
    
    def test_clear_default(self, temp_window):
        """Test clear with default values."""
        temp_window.graphics.clear()
        # Should not raise
    
    def test_clear_with_color(self, temp_window):
        """Test clear with specific color."""
        temp_window.graphics.clear(0.2, 0.3, 0.4, 1.0)
        # Should not raise


class TestAliases:
    """Test that Pythonic aliases work."""
    
    def test_set_color_alias(self, temp_window):
        """Test set_color alias exists."""
        assert hasattr(temp_window.graphics, 'set_color')
        assert hasattr(temp_window.graphics, 'setColor')
    
    def test_get_color_alias(self, temp_window):
        """Test get_color alias exists."""
        assert hasattr(temp_window.graphics, 'get_color')
        assert hasattr(temp_window.graphics, 'getColor')
    
    def test_set_background_color_alias(self, temp_window):
        """Test set_background_color alias exists."""
        assert hasattr(temp_window.graphics, 'set_background_color')
        assert hasattr(temp_window.graphics, 'setBackgroundColor')
    
    def test_get_dimensions_alias(self, temp_window):
        """Test get_dimensions alias exists."""
        assert hasattr(temp_window.graphics, 'get_dimensions')
        assert hasattr(temp_window.graphics, 'getDimensions')


class TestVisualRendering:
    """Tests that require visual verification (manual or automated)."""
    
    @pytest.mark.visual
    def test_rectangle_rendered(self, temp_window):
        """Visual test: Verify rectangle appears on screen.
        
        Note: This test requires manual verification or screenshot comparison.
        """
        temp_window.graphics.clear(0, 0, 0)
        temp_window.graphics.set_color(1, 0, 0)
        temp_window.graphics.rectangle('fill', 10, 10, 50, 50)
        temp_window.graphics.present()
        
        # Manual verification: Red rectangle at (10, 10)
        assert True  # Requires visual check
    
    @pytest.mark.visual
    def test_circle_rendered(self, temp_window):
        """Visual test: Verify circle appears on screen."""
        temp_window.graphics.clear(0, 0, 0)
        temp_window.graphics.set_color(0, 1, 0)
        temp_window.graphics.circle('fill', 100, 100, 30)
        temp_window.graphics.present()
        
        # Manual verification: Green circle at (100, 100)
        assert True  # Requires visual check
    
    @pytest.mark.visual
    def test_transform_rendered(self, temp_window):
        """Visual test: Verify transformations work."""
        temp_window.graphics.clear(0, 0, 0)
        temp_window.graphics.set_color(0, 0, 1)
        temp_window.graphics.push()
        temp_window.graphics.translate(50, 50)
        temp_window.graphics.rotate(0.785)  # 45 degrees
        temp_window.graphics.rectangle('fill', 0, 0, 40, 40)
        temp_window.graphics.pop()
        temp_window.graphics.present()
        
        # Manual verification: Rotated blue rectangle
        assert True  # Requires visual check
