"""
Data models for the LOVE2D API.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union


@dataclass
class TableField:
    """Represents a field in a table type argument/return."""
    type: str
    name: str
    description: str
    default: Optional[str] = None


@dataclass
class Argument:
    """Represents a function argument."""
    type: str
    name: str
    description: str
    default: Optional[str] = None
    table: List[TableField] = field(default_factory=list)


@dataclass
class Return:
    """Represents a function return value."""
    type: str
    name: str
    description: str
    table: List[TableField] = field(default_factory=list)


@dataclass
class Variant:
    """Represents a function variant (overloaded function signature)."""
    description: Optional[str] = None
    arguments: List[Argument] = field(default_factory=list)
    returns: List[Return] = field(default_factory=list)


@dataclass
class Function:
    """Represents a function in the API."""
    name: str
    description: str
    variants: List[Variant] = field(default_factory=list)


@dataclass
class Type:
    """Represents a type/class in the API."""
    name: str
    description: str
    constructors: List[str] = field(default_factory=list)
    functions: List[Function] = field(default_factory=list)
    supertypes: List[str] = field(default_factory=list)


@dataclass
class EnumConstant:
    """Represents a constant in an enum."""
    name: str
    description: str


@dataclass
class Enum:
    """Represents an enumeration in the API."""
    name: str
    description: str
    constants: List[EnumConstant] = field(default_factory=list)


@dataclass
class Module:
    """Represents a LÖVE module (e.g., graphics, audio)."""
    name: str
    description: str
    types: List[Type] = field(default_factory=list)
    functions: List[Function] = field(default_factory=list)
    enums: List[Enum] = field(default_factory=list)


@dataclass
class Callback(Function):
    """Represents a callback function (special type of function)."""
    pass


@dataclass
class LoveAPI:
    """Root class containing the entire LÖVE API."""
    version: str
    functions: List[Function] = field(default_factory=list)
    modules: List[Module] = field(default_factory=list)
    types: List[Type] = field(default_factory=list)
    callbacks: List[Callback] = field(default_factory=list)
    
    def get_module(self, name: str) -> Optional[Module]:
        """Get a module by name."""
        for module in self.modules:
            if module.name == name:
                return module
        return None
    
    def get_callback(self, name: str) -> Optional[Callback]:
        """Get a callback by name."""
        for callback in self.callbacks:
            if callback.name == name:
                return callback
        return None
    
    def get_type(self, name: str) -> Optional[Type]:
        """Get a type by name (searches all modules and global types)."""
        # Search global types first
        for type_ in self.types:
            if type_.name == name:
                return type_
        # Search in modules
        for module in self.modules:
            for type_ in module.types:
                if type_.name == name:
                    return type_
        return None
    
    def get_function(self, full_name: str) -> Optional[Function]:
        """Get a function by full name (e.g., 'love.graphics.draw')."""
        parts = full_name.split('.')
        if len(parts) == 2 and parts[0] == 'love':
            # Global function like love.getVersion
            for func in self.functions:
                if func.name == parts[1]:
                    return func
        elif len(parts) >= 3 and parts[0] == 'love':
            # Module function like love.graphics.draw
            module = self.get_module(parts[1])
            if module:
                func_name = parts[2]
                for func in module.functions:
                    if func.name == func_name:
                        return func
                # Check type methods
                for type_ in module.types:
                    if type_.name == func_name:
                        # This is a constructor
                        return None
                    for method in type_.functions:
                        if method.name == func_name:
                            return method
        return None
