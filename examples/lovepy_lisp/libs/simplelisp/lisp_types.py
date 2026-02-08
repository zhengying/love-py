"""
SimpleLisp Type System
Data types for the Simply Scheme interpreter.
"""
from dataclasses import dataclass
from typing import Any, Callable, List as PyList, Optional, Union


# ============================================================================
# Base Types
# ============================================================================

class LispValue:
    """Base class for all Lisp values."""
    pass


@dataclass
class LispNumber(LispValue):
    """Integer or Float number."""
    value: Union[int, float]
    
    def __repr__(self):
        if isinstance(self.value, float) and self.value.is_integer():
            return str(int(self.value))
        return str(self.value)


@dataclass
class LispSymbol(LispValue):
    """Interned symbol (e.g., 'hello)."""
    name: str
    
    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, LispSymbol):
            return self.name == other.name
        return False


@dataclass
class LispString(LispValue):
    """Quoted string."""
    value: str
    
    def __repr__(self):
        return f'"{self.value}"'


@dataclass  
class LispBool(LispValue):
    """Boolean: #t or #f."""
    value: bool
    
    def __repr__(self):
        return "#t" if self.value else "#f"


# Singleton booleans
TRUE = LispBool(True)
FALSE = LispBool(False)


class LispList(LispValue):
    """List implemented as Python list for simplicity."""
    def __init__(self, elements: PyList[LispValue] = None):
        self.elements = elements if elements is not None else []
    
    def __repr__(self):
        if not self.elements:
            return "()"
        inner = " ".join(repr(e) for e in self.elements)
        return f"({inner})"
    
    def __len__(self):
        return len(self.elements)
    
    def __iter__(self):
        return iter(self.elements)
    
    def __getitem__(self, index):
        return self.elements[index]
    
    def is_empty(self):
        return len(self.elements) == 0


# Empty list singleton
NIL = LispList([])


@dataclass
class LispVector(LispValue):
    """Mutable fixed-length array."""
    elements: PyList[LispValue]
    
    def __repr__(self):
        inner = " ".join(repr(e) for e in self.elements)
        return f"#({inner})"


class LispVoid(LispValue):
    """Returned by side-effect functions like define, display."""
    def __repr__(self):
        return ""


# Singleton void
VOID = LispVoid()


# ============================================================================
# Procedures
# ============================================================================

class LispProcedure(LispValue):
    """Base class for callable procedures."""
    pass


@dataclass
class LispPrimitive(LispProcedure):
    """Built-in function implemented in Python."""
    name: str
    func: Callable
    
    def __repr__(self):
        return f"#<primitive:{self.name}>"


@dataclass
class LispClosure(LispProcedure):
    """User-defined function (lambda)."""
    params: PyList[str]        # Parameter names
    body: PyList[LispValue]    # Body expressions
    env: Any                   # Captured environment (will be Environment)
    name: Optional[str] = None # Optional name for debugging
    
    def __repr__(self):
        if self.name:
            return f"#<procedure:{self.name}>"
        return "#<procedure>"


# ============================================================================
# Type Checking Utilities
# ============================================================================

def is_truthy(value: LispValue) -> bool:
    """Everything except #f is truthy in Scheme."""
    if isinstance(value, LispBool):
        return value.value
    return True


def is_list(value: LispValue) -> bool:
    return isinstance(value, LispList)


def is_number(value: LispValue) -> bool:
    return isinstance(value, LispNumber)


def is_symbol(value: LispValue) -> bool:
    return isinstance(value, LispSymbol)


def is_string(value: LispValue) -> bool:
    return isinstance(value, LispString)


def is_word(value: LispValue) -> bool:
    """A 'word' in Simply Scheme: number, symbol, or string."""
    return isinstance(value, (LispNumber, LispSymbol, LispString))


def is_procedure(value: LispValue) -> bool:
    return isinstance(value, LispProcedure)


def is_boolean(value: LispValue) -> bool:
    return isinstance(value, LispBool)


def is_vector(value: LispValue) -> bool:
    return isinstance(value, LispVector)


def is_void(value: LispValue) -> bool:
    return isinstance(value, LispVoid)


def to_python_string(value: LispValue) -> str:
    """Convert a word to its string representation."""
    if isinstance(value, LispNumber):
        if isinstance(value.value, float) and value.value.is_integer():
            return str(int(value.value))
        return str(value.value)
    elif isinstance(value, LispSymbol):
        return value.name
    elif isinstance(value, LispString):
        return value.value
    else:
        raise TypeError(f"Cannot convert {type(value).__name__} to string")
