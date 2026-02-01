"""
Pytest tests for the LOVE2D API Python implementation.
These tests validate the structure and integrity of the API data.
"""
import pytest
from dataclasses import fields, is_dataclass
from typing import get_type_hints

from love_api_py.models import (
    LoveAPI, Module, Function, Type, Enum, EnumConstant,
    Variant, Argument, Return, Callback, TableField
)
from love_api_py.api_data import API


class TestAPIIntegrity:
    """Tests to ensure the API table is valid and properly structured."""
    
    def test_api_exists(self):
        """Ensure the API object exists and is valid."""
        assert API is not None
        assert isinstance(API, LoveAPI)
        
    def test_api_version(self):
        """Ensure the API has a valid version."""
        assert API.version is not None
        assert isinstance(API.version, str)
        assert API.version == "11.5"
    
    def test_api_lists_exist(self):
        """Ensure all required lists exist."""
        assert isinstance(API.functions, list)
        assert isinstance(API.modules, list)
        assert isinstance(API.types, list)
        assert isinstance(API.callbacks, list)


class TestStringValues:
    """Tests that all string fields contain actual strings."""
    
    def test_all_string_fields_are_strings(self):
        """Recursively check that all values expected to be strings are strings."""
        
        def check_string_field(obj, field_name, value):
            """Check if a value is a string when it should be."""
            string_fields = [
                'name', 'description', 'type', 'default', 'version'
            ]
            
            if field_name in string_fields and value is not None:
                assert isinstance(value, str), (
                    f"Field '{field_name}' should be a string, "
                    f"got {type(value).__name__}: {value!r}"
                )
        
        def recursive_check(obj, field_name=None):
            """Recursively check all fields."""
            if is_dataclass(obj):
                for field in fields(obj):
                    value = getattr(obj, field.name)
                    check_string_field(obj, field.name, value)
                    recursive_check(value, field.name)
            elif isinstance(obj, list):
                for item in obj:
                    recursive_check(item, field_name)
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    check_string_field(obj, key, value)
                    recursive_check(value, key)
        
        recursive_check(API)


class TestValidKeys:
    """Tests that only valid keys are used in the data structures."""
    
    VALID_MODEL_FIELDS = {
        # LoveAPI fields
        'version', 'functions', 'modules', 'types', 'callbacks',
        # Module fields
        'name', 'description', 'types', 'functions', 'enums',
        # Function/Callback fields
        'variants',
        # Type fields
        'constructors', 'supertypes', 'functions',
        # Enum fields
        'constants',
        # EnumConstant fields
        # Variant fields
        'arguments', 'returns',
        # Argument/Return fields
        'type', 'name', 'default', 'description', 'table',
        # TableField fields
        # Other valid fields
        'parenttype', 'subtypes', 'minidescription', 'notes',
        'arraytype', 'tabletype', 'tablearray', 'signature',
        'config', 'api'
    }
    
    def test_all_model_fields_valid(self):
        """Check that all dataclass fields are in the valid fields list."""
        models = [
            LoveAPI, Module, Function, Type, Enum, EnumConstant,
            Variant, Argument, Return, Callback, TableField
        ]
        
        for model in models:
            for field in fields(model):
                assert field.name in self.VALID_MODEL_FIELDS, (
                    f"Field '{field.name}' in {model.__name__} is not in valid fields list"
                )


class TestArgumentStructure:
    """Tests that arguments are properly wrapped in tables/lists."""
    
    def test_arguments_are_wrapped_in_lists(self):
        """Check that all arguments are wrapped in lists."""
        
        def check_arguments_in_function(func):
            """Check arguments in a function."""
            for variant in func.variants:
                assert isinstance(variant.arguments, list), (
                    f"Arguments in {func.name} should be a list"
                )
                for arg in variant.arguments:
                    assert isinstance(arg, Argument), (
                        f"Each argument in {func.name} should be an Argument object"
                    )
        
        # Check global functions
        for func in API.functions:
            check_arguments_in_function(func)
        
        # Check module functions
        for module in API.modules:
            for func in module.functions:
                check_arguments_in_function(func)
            
            # Check type methods
            for type_ in module.types:
                for func in type_.functions:
                    check_arguments_in_function(func)
        
        # Check callbacks
        for callback in API.callbacks:
            check_arguments_in_function(callback)


class TestReturnStructure:
    """Tests that return values are properly wrapped in tables/lists."""
    
    def test_returns_are_wrapped_in_lists(self):
        """Check that all returns are wrapped in lists."""
        
        def check_returns_in_function(func):
            """Check returns in a function."""
            for variant in func.variants:
                assert isinstance(variant.returns, list), (
                    f"Returns in {func.name} should be a list"
                )
                for ret in variant.returns:
                    assert isinstance(ret, Return), (
                        f"Each return in {func.name} should be a Return object"
                    )
        
        # Check global functions
        for func in API.functions:
            check_returns_in_function(func)
        
        # Check module functions
        for module in API.modules:
            for func in module.functions:
                check_returns_in_function(func)
            
            # Check type methods
            for type_ in module.types:
                for func in type_.functions:
                    check_returns_in_function(func)
        
        # Check callbacks
        for callback in API.callbacks:
            check_returns_in_function(callback)


class TestModuleIntegrity:
    """Tests for module-specific integrity checks."""
    
    def test_modules_have_required_fields(self):
        """Ensure all modules have required fields."""
        for module in API.modules:
            assert module.name is not None and module.name != "", (
                f"Module name cannot be empty"
            )
            assert module.description is not None, (
                f"Module {module.name} must have a description"
            )
            assert isinstance(module.types, list)
            assert isinstance(module.functions, list)
            assert isinstance(module.enums, list)
    
    def test_modules_have_unique_names(self):
        """Ensure all module names are unique."""
        names = [m.name for m in API.modules]
        assert len(names) == len(set(names)), (
            f"Duplicate module names found: {names}"
        )


class TestFunctionIntegrity:
    """Tests for function-specific integrity checks."""
    
    def test_functions_have_required_fields(self):
        """Ensure all functions have required fields."""
        def check_function(func, context=""):
            assert func.name is not None and func.name != "", (
                f"Function name cannot be empty in {context}"
            )
            assert func.description is not None, (
                f"Function {func.name} must have a description"
            )
            assert isinstance(func.variants, list), (
                f"Function {func.name} must have a variants list"
            )
        
        # Check global functions
        for func in API.functions:
            check_function(func, "global functions")
        
        # Check module functions
        for module in API.modules:
            for func in module.functions:
                check_function(func, f"module {module.name}")
            
            # Check type methods
            for type_ in module.types:
                for func in type_.functions:
                    check_function(func, f"type {type_.name}")
        
        # Check callbacks
        for callback in API.callbacks:
            check_function(callback, "callbacks")


class TestTypeIntegrity:
    """Tests for type-specific integrity checks."""
    
    def test_types_have_required_fields(self):
        """Ensure all types have required fields."""
        for module in API.modules:
            for type_ in module.types:
                assert type_.name is not None and type_.name != "", (
                    f"Type name cannot be empty in module {module.name}"
                )
                assert type_.description is not None, (
                    f"Type {type_.name} must have a description"
                )
                assert isinstance(type_.functions, list)
                assert isinstance(type_.supertypes, list)
                assert isinstance(type_.constructors, list)


class TestEnumIntegrity:
    """Tests for enum-specific integrity checks."""
    
    def test_enums_have_required_fields(self):
        """Ensure all enums have required fields."""
        for module in API.modules:
            for enum in module.enums:
                assert enum.name is not None and enum.name != "", (
                    f"Enum name cannot be empty in module {module.name}"
                )
                assert enum.description is not None, (
                    f"Enum {enum.name} must have a description"
                )
                assert isinstance(enum.constants, list)
                
                for constant in enum.constants:
                    assert constant.name is not None and constant.name != "", (
                        f"Enum constant name cannot be empty in enum {enum.name}"
                    )
                    assert constant.description is not None, (
                        f"Enum constant {constant.name} must have a description"
                    )


class TestAPIQueries:
    """Tests for API query methods."""
    
    def test_get_module(self):
        """Test the get_module method."""
        graphics = API.get_module("graphics")
        assert graphics is not None
        assert graphics.name == "graphics"
        
        nonexistent = API.get_module("nonexistent")
        assert nonexistent is None
    
    def test_get_callback(self):
        """Test the get_callback method."""
        update = API.get_callback("update")
        assert update is not None
        assert update.name == "update"
        
        nonexistent = API.get_callback("nonexistent")
        assert nonexistent is None
    
    def test_get_type(self):
        """Test the get_type method."""
        image = API.get_type("Image")
        assert image is not None
        assert image.name == "Image"
        
        nonexistent = API.get_type("Nonexistent")
        assert nonexistent is None
    
    def test_get_function(self):
        """Test the get_function method."""
        draw = API.get_function("love.graphics.draw")
        assert draw is not None
        assert draw.name == "draw"
        
        get_version = API.get_function("love.getVersion")
        assert get_version is not None
        assert get_version.name == "getVersion"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
