"""
Example usage of the LOVE2D Python API.
"""

from love_api_py import API


def example_1_basic_usage():
    """Example 1: Basic API usage."""
    print("=" * 60)
    print("Example 1: Basic API Information")
    print("=" * 60)
    
    # Get API version
    print(f"\nLÖVE Version: {API.version}")
    
    # List all modules
    print(f"\nTotal modules: {len(API.modules)}")
    print("\nModules:")
    for module in API.modules:
        print(f"  - {module.name}")


def example_2_query_functions():
    """Example 2: Querying functions."""
    print("\n" + "=" * 60)
    print("Example 2: Querying Functions")
    print("=" * 60)
    
    # Get graphics module
    graphics = API.get_module("graphics")
    print(f"\nGraphics module has:")
    print(f"  - {len(graphics.functions)} functions")
    print(f"  - {len(graphics.types)} types")
    print(f"  - {len(graphics.enums)} enums")
    
    # Get a specific function
    draw_func = API.get_function("love.graphics.draw")
    if draw_func:
        print(f"\nFunction: love.graphics.draw")
        print(f"Description: {draw_func.description[:100]}...")
        print(f"Number of variants: {len(draw_func.variants)}")
        
        # Show first variant
        if draw_func.variants:
            variant = draw_func.variants[0]
            print(f"\nFirst variant arguments:")
            for arg in variant.arguments[:4]:  # Show first 4 args
                print(f"  - {arg.name}: {arg.type}")


def example_3_list_all_callbacks():
    """Example 3: List all callbacks."""
    print("\n" + "=" * 60)
    print("Example 3: All Callbacks")
    print("=" * 60)
    
    print(f"\nTotal callbacks: {len(API.callbacks)}")
    print("\nCallbacks:")
    for callback in API.callbacks:
        print(f"  - {callback.name}: {callback.description[:50]}...")


def example_4_types_info():
    """Example 4: Information about types."""
    print("\n" + "=" * 60)
    print("Example 4: Types Information")
    print("=" * 60)
    
    # Get Image type
    image_type = API.get_type("Image")
    if image_type:
        print(f"\nType: {image_type.name}")
        print(f"Description: {image_type.description}")
        print(f"Constructors: {image_type.constructors}")
        print(f"Supertypes: {image_type.supertypes}")
        print(f"Methods: {len(image_type.functions)}")
        
        print("\nMethods:")
        for func in image_type.functions[:5]:
            print(f"  - {func.name}")


def example_5_generate_signatures():
    """Example 5: Generate function signatures."""
    print("\n" + "=" * 60)
    print("Example 5: Function Signatures")
    print("=" * 60)
    
    def generate_signature(func):
        """Generate Python-style function signature."""
        sigs = []
        for variant in func.variants:
            args = []
            for arg in variant.arguments:
                arg_str = f"{arg.name}: {arg.type}"
                if arg.default:
                    arg_str += f" = {arg.default}"
                args.append(arg_str)
            
            ret = "None"
            if variant.returns:
                if len(variant.returns) == 1:
                    ret = variant.returns[0].type
                else:
                    ret = f"Tuple[{', '.join(r.type for r in variant.returns)}]"
            
            sigs.append(f"def {func.name}({', '.join(args)}) -> {ret}")
        return sigs
    
    # Generate signatures for keyboard functions
    keyboard = API.get_module("keyboard")
    print("\nKeyboard module signatures:")
    for func in keyboard.functions[:3]:
        sigs = generate_signature(func)
        for sig in sigs:
            print(f"  {sig}")


def example_6_enum_constants():
    """Example 6: Enum constants."""
    print("\n" + "=" * 60)
    print("Example 6: Enum Constants")
    print("=" * 60)
    
    graphics = API.get_module("graphics")
    
    print("\nGraphics enums:")
    for enum in graphics.enums:
        print(f"\n  Enum: {enum.name}")
        print(f"  Description: {enum.description}")
        print(f"  Constants ({len(enum.constants)} total):")
        for const in enum.constants[:5]:  # Show first 5
            print(f"    - {const.name}")


def example_7_statistics():
    """Example 7: API Statistics."""
    print("\n" + "=" * 60)
    print("Example 7: API Statistics")
    print("=" * 60)
    
    total_functions = len(API.functions)
    total_callbacks = len(API.callbacks)
    total_modules = len(API.modules)
    
    module_functions = sum(len(m.functions) for m in API.modules)
    module_types = sum(len(m.types) for m in API.modules)
    module_enums = sum(len(m.enums) for m in API.modules)
    
    type_methods = sum(
        len(t.functions) for m in API.modules for t in m.types
    )
    
    total_all_functions = total_functions + module_functions + type_methods
    
    print(f"\nAPI Overview:")
    print(f"  LÖVE Version: {API.version}")
    print(f"  Modules: {total_modules}")
    print(f"  Global Functions: {total_functions}")
    print(f"  Callbacks: {total_callbacks}")
    print(f"  Module Functions: {module_functions}")
    print(f"  Type Methods: {type_methods}")
    print(f"  Total Functions: {total_all_functions}")
    print(f"  Types: {module_types}")
    print(f"  Enums: {module_enums}")


if __name__ == "__main__":
    # Run all examples
    example_1_basic_usage()
    example_2_query_functions()
    example_3_list_all_callbacks()
    example_4_types_info()
    example_5_generate_signatures()
    example_6_enum_constants()
    example_7_statistics()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
