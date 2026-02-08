"""
SimpleLisp Environment
Lexical scoping environment for the Simply Scheme interpreter.
"""
from typing import Any, Dict, Optional


class Environment:
    """
    Lexical environment with parent chain for scoping.
    """
    
    def __init__(self, parent: Optional['Environment'] = None):
        self.bindings: Dict[str, Any] = {}
        self.parent = parent
    
    def define(self, name: str, value: Any) -> None:
        """Define a new binding in the current environment."""
        self.bindings[name] = value
    
    def lookup(self, name: str) -> Any:
        """Look up a variable, searching parent environments."""
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        raise NameError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: Any) -> None:
        """Set an existing variable (for set!)."""
        if name in self.bindings:
            self.bindings[name] = value
        elif self.parent is not None:
            self.parent.set(name, value)
        else:
            raise NameError(f"Cannot set undefined variable: {name}")
    
    def extend(self, params: list, args: list) -> 'Environment':
        """Create a new environment extending this one with param/arg bindings."""
        new_env = Environment(self)
        for param, arg in zip(params, args):
            new_env.define(param, arg)
        return new_env
    
    def __repr__(self):
        bindings_str = ", ".join(f"{k}: {v}" for k, v in self.bindings.items())
        parent_str = " -> parent" if self.parent else ""
        return f"Env({{{bindings_str}}}{parent_str})"
