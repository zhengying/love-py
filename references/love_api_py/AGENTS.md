# Agent Guidelines for love-api-py

This is a Python package that provides a complete machine-readable representation of the LÖVE 2D game framework API (version 11.5) using Python dataclasses.

## Project Structure

```
love_api_py/
├── love_api_py/
│   ├── __init__.py       # Package exports
│   ├── models.py         # Dataclass definitions (LoveAPI, Module, Function, etc.)
│   ├── api_data.py       # The actual API data (large file)
│   └── modules/          # (empty - future use)
├── tests/
│   ├── __init__.py
│   └── test_api.py       # Comprehensive test suite
├── examples/
│   └── basic_usage.py    # Usage examples
├── convert_lua.py        # Lua-to-Python converter script
├── pyproject.toml        # Build configuration
├── requirements.txt      # Test dependencies
└── setup.py             # Package setup
```

## Build/Test Commands

```bash
# Install package in editable mode
cd love_api_py
pip install -e .

# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run a single test class
pytest tests/test_api.py::TestAPIIntegrity -v

# Run a single test method
pytest tests/test_api.py::TestAPIIntegrity::test_api_version -v

# Run with coverage
pytest tests/ -v --cov=love_api_py --cov-report=html

# Run specific test pattern
pytest tests/ -v -k "test_api"

# Build package (uses setuptools)
python -m build

# Run example
python examples/basic_usage.py
```

## Code Style Guidelines

### Imports
- Group imports: stdlib → third-party → local (alphabetically within groups)
- Use explicit imports (no wildcard imports)
- Example:
  ```python
  from dataclasses import dataclass, field
  from typing import List, Optional, Dict, Any, Union
  
  from love_api_py.models import LoveAPI, Module, Function
  ```

### Formatting
- 4-space indentation (no tabs)
- 100 character line limit
- Use double quotes for strings (unless single quotes needed inside)
- Trailing commas in multi-line lists/dicts
- Two blank lines between top-level classes/functions
- One blank line between methods

### Type Annotations
- Always use type hints for function parameters and return types
- Use `Optional[T]` for nullable values, not `T | None`
- Use `List[T]` not `list[T]` (Python 3.7+ compatible)
- Use `Dict[str, Any]` for flexible dictionaries

### Naming Conventions
- `PascalCase` for classes (LoveAPI, Module, Function)
- `snake_case` for functions, methods, variables
- `UPPER_CASE` for module-level constants
- Descriptive names: `get_module()` not `get_mod()`

### Docstrings
- Google-style docstrings for all public classes and functions
- One-line docstrings for simple methods
- Example:
  ```python
  def get_module(self, name: str) -> Optional[Module]:
      """Get a module by name.
      
      Args:
          name: The module name (e.g., "graphics")
          
      Returns:
          The Module if found, None otherwise
      """
  ```

### Dataclasses
- Always use `@dataclass` decorator
- Use `field(default_factory=list)` for mutable defaults
- Include type annotations on all fields
- Example:
  ```python
  @dataclass
  class Function:
      name: str
      description: str
      variants: List[Variant] = field(default_factory=list)
  ```

### Error Handling
- Use explicit assertions in tests with helpful messages
- Return `Optional[T]` instead of raising exceptions for missing lookups
- Validate data integrity in tests, not in models

### Testing
- Use pytest (not unittest)
- Class-based test organization (TestAPIIntegrity, TestStringValues, etc.)
- Descriptive test method names: `test_*`
- Use pytest fixtures if shared setup needed
- All tests must pass before committing

### API Data Guidelines
- All string fields must contain actual strings (validated in tests)
- All lists must be actual lists (not single items)
- Module names match LÖVE module names: "graphics", "audio", "keyboard", etc.
- Function names are the bare names (not full paths like "love.graphics.draw")
- Descriptions should be complete but concise

### Git Workflow
- No specific branch naming convention
- Run full test suite before any commit
- Tests must pass on Python 3.7+

## Key Files

- `love_api_py/models.py` - Core dataclass definitions (154 lines)
- `love_api_py/api_data.py` - Large auto-generated file with all API data
- `tests/test_api.py` - Comprehensive test suite (330 lines)
- `examples/basic_usage.py` - Working examples of API usage

## Common Patterns

### Querying the API
```python
from love_api_py import API

# Get module
graphics = API.get_module("graphics")

# Get function by full path
draw = API.get_function("love.graphics.draw")

# Get type
image_type = API.get_type("Image")

# Iterate modules
for module in API.modules:
    print(f"{module.name}: {len(module.functions)} functions")
```

### Adding a New Test
```python
class TestNewFeature:
    """Tests for the new feature."""
    
    def test_something_specific(self):
        """Test that something works correctly."""
        result = API.get_module("graphics")
        assert result is not None
        assert result.name == "graphics"
```

## LÖVE API Version
- Current API version: **11.5**
- Version stored in `API.version` and `__version__`
