# LOVE2D API for Python

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![LÖVE](https://img.shields.io/badge/L%C3%96VE-11.5-EA316E.svg)](http://love2d.org/)
[![Pytest](https://img.shields.io/badge/tested%20with-pytest-brightgreen.svg)](https://docs.pytest.org/)

Complete LÖVE 2D game framework API documentation as Python dataclasses.

This package provides a machine-readable representation of the entire LÖVE API, making it perfect for:
- IDE autocompletion and code hints
- Documentation generators
- Code analysis tools
- Type checking systems
- Game development frameworks

## Installation

```bash
pip install love-api-py
```

Or install from source:

```bash
git clone https://github.com/love2d-community/love-api.git
cd love-api/love_api_py
pip install -e .
```

## Quick Start

```python
from love_api_py import API, LoveAPI, Module, Function

# Access the complete API
print(f"LÖVE Version: {API.version}")  # 11.5

# Get a specific module
graphics = API.get_module("graphics")
print(f"Graphics module has {len(graphics.functions)} functions")

# Find a function
draw_func = API.get_function("love.graphics.draw")
print(f"Function: {draw_func.name}")
print(f"Description: {draw_func.description}")

# List all modules
for module in API.modules:
    print(f"- {module.name}: {len(module.functions)} functions, {len(module.types)} types")

# Access callbacks
update_callback = API.get_callback("update")
print(f"Update callback: {update_callback.description}")
```

## API Structure

The API is organized into Python dataclasses:

```python
LoveAPI
├── version: str                    # "11.5"
├── functions: List[Function]       # Global love.* functions
├── modules: List[Module]           # All modules (graphics, audio, etc.)
│   └── Module
│       ├── name: str
│       ├── description: str
│       ├── types: List[Type]       # Types in this module
│       ├── functions: List[Function]
│       └── enums: List[Enum]
├── types: List[Type]               # Global types
└── callbacks: List[Callback]       # Event callbacks

Function/Callback
├── name: str
├── description: str
└── variants: List[Variant]         # Function overloads
    └── Variant
        ├── description: str
        ├── arguments: List[Argument]
        │   └── Argument
        │       ├── type: str
        │       ├── name: str
        │       ├── description: str
        │       └── default: str (optional)
        └── returns: List[Return]
            └── Return
                ├── type: str
                ├── name: str
                └── description: str

Type
├── name: str
├── description: str
├── constructors: List[str]         # Functions that create this type
├── supertypes: List[str]           # Parent types
└── functions: List[Function]       # Methods

Enum
├── name: str
├── description: str
└── constants: List[EnumConstant]
    └── EnumConstant
        ├── name: str
        └── description: str
```

## Available Modules

- **graphics** - Drawing, images, fonts, shaders, shapes
- **keyboard** - Keyboard input handling
- **mouse** - Mouse input handling
- **timer** - Time and frame rate functions
- **window** - Window management
- **event** - Event queue management
- **filesystem** - File I/O operations
- **audio** - Audio playback
- **math** - Math utilities and random numbers
- **touch** - Touch screen input

## Query Methods

The `LoveAPI` class provides convenient query methods:

```python
# Get module by name
module = API.get_module("graphics")

# Get callback by name  
callback = API.get_callback("update")

# Get type by name (searches all modules)
type_ = API.get_type("Image")

# Get function by full name
func = API.get_function("love.graphics.draw")
func = API.get_function("love.getVersion")
```

## Testing

Run the test suite with pytest:

```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
cd love_api_py
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=love_api_py --cov-report=html
```

### Test Categories

The test suite includes:

- **TestAPIIntegrity** - Validates API structure and version
- **TestStringValues** - Ensures all string fields are strings
- **TestValidKeys** - Validates only allowed field names are used
- **TestArgumentStructure** - Checks arguments are properly wrapped in lists
- **TestReturnStructure** - Checks return values are properly wrapped in lists
- **TestModuleIntegrity** - Validates module structure
- **TestFunctionIntegrity** - Validates function structure
- **TestTypeIntegrity** - Validates type structure
- **TestEnumIntegrity** - Validates enum structure
- **TestAPIQueries** - Tests query methods

## Example: Generating Function Signatures

```python
from love_api_py import API

def generate_signature(func):
    """Generate a function signature string."""
    signatures = []
    
    for variant in func.variants:
        # Build arguments string
        args_str = ", ".join([
            f"{arg.name}: {arg.type}" + 
            (f" = {arg.default}" if arg.default else "")
            for arg in variant.arguments
        ])
        
        # Build returns string
        if variant.returns:
            if len(variant.returns) == 1:
                ret_str = f" -> {variant.returns[0].type}"
            else:
                ret_types = ", ".join([r.type for r in variant.returns])
                ret_str = f" -> Tuple[{ret_types}]"
        else:
            ret_str = ""
        
        sig = f"{func.name}({args_str}){ret_str}"
        signatures.append(sig)
    
    return signatures

# Get all graphics functions
graphics = API.get_module("graphics")
for func in graphics.functions[:5]:  # First 5 functions
    sigs = generate_signature(func)
    print(f"{func.name}:")
    for sig in sigs:
        print(f"  {sig}")
```

## Example: IDE Autocompletion Data

```python
from love_api_py import API

# Generate autocompletion data for an IDE
def generate_completion_data():
    completions = []
    
    # Add module functions
    for module in API.modules:
        prefix = f"love.{module.name}."
        for func in module.functions:
            completions.append({
                "label": prefix + func.name,
                "kind": "function",
                "documentation": func.description,
            })
        
        # Add type methods
        for type_ in module.types:
            for func in type_.functions:
                completions.append({
                    "label": prefix + func.name,
                    "kind": "method",
                    "documentation": func.description,
                })
    
    return completions

completions = generate_completion_data()
print(f"Generated {len(completions)} completion items")
```

## Version

This package documents LÖVE version **11.5**.

## Contributing

Contributions are welcome! If you find any errors or missing content:

1. Fork the repository
2. Make your changes to the appropriate files in `love_api_py/`
3. Add or update tests in `tests/`
4. Run the test suite: `pytest tests/ -v`
5. Submit a pull request

## Projects Using This API

This Python API is perfect for building:
- Python-based LÖVE game editors
- IDE plugins (VSCode, PyCharm, etc.)
- Documentation generators
- Code analysis and linting tools
- Type stub generators

## Credits

This Python API is based on the [LÖVE-API](https://github.com/love2d-community/love-api) Lua project by the LÖVE community.

- Original Lua API: [love2d-community/love-api](https://github.com/love2d-community/love-api)
- LÖVE Game Framework: [love2d.org](https://love2d.org/)

## License

This project follows the same license as the original LÖVE-API project.

## Related Projects

- [LÖVE-API (Lua)](https://github.com/love2d-community/love-api) - Original Lua version
- [ZeroBrane Studio](http://studio.zerobrane.com/) - Lua IDE using the Lua API
- [Lua language server](https://github.com/LuaLS/lua-language-server) - Lua LSP using the API

---

Made with ❤️ for the LÖVE community
