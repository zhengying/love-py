"""
Converter script to transform Lua API files to Python.
This script reads Lua files and generates equivalent Python dataclass definitions.
"""
import re
import os
from pathlib import Path
from typing import List, Dict, Any


class LuaToPythonConverter:
    """Converts Lua table definitions to Python dataclass instances."""
    
    def __init__(self, lua_file_path: str):
        self.lua_file_path = lua_file_path
        self.lua_content = self._read_lua_file()
        
    def _read_lua_file(self) -> str:
        """Read the Lua file content."""
        with open(self.lua_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _extract_string_value(self, text: str, key: str) -> str:
        """Extract a string value from a Lua table definition."""
        pattern = rf'{key}\s*=\s*(?:\'|\"|\[\[)(.*?)(?:\'|\"|\]\])'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_table_array(self, text: str, key: str) -> List[Dict]:
        """Extract an array of tables from Lua."""
        items = []
        # Find the start of the array
        pattern = rf'{key}\s*=\s*\{{'
        match = re.search(pattern, text)
        if not match:
            return items
        
        start_pos = match.end() - 1
        brace_count = 0
        in_string = False
        string_char = None
        i = start_pos
        
        while i < len(text):
            char = text[i]
            
            if not in_string and char in ('"', "'", '['):
                if char == '[' and text[i:i+2] == '[[':
                    in_string = True
                    string_char = '[['
                    i += 2
                    continue
                in_string = True
                string_char = char
            elif in_string:
                if string_char == '[[' and text[i:i+2] == ']]':
                    in_string = False
                    string_char = None
                    i += 2
                    continue
                elif char == string_char:
                    in_string = False
                    string_char = None
            elif char == '{':
                brace_count += 1
                if brace_count == 1:
                    item_start = i
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    item_text = text[item_start:i+1]
                    items.append(self._parse_table_item(item_text))
                    
            i += 1
            
            if brace_count == 0 and char == '}':
                break
        
        return items
    
    def _parse_table_item(self, item_text: str) -> Dict[str, Any]:
        """Parse a single Lua table into a dictionary."""
        result = {}
        
        # Extract name
        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', item_text)
        if name_match:
            result['name'] = name_match.group(1)
        
        # Extract description (handle multiline strings)
        desc_match = re.search(r'description\s*=\s*(?:\[\[|"\'|\'"|\')(.*?)(?:\]\]|"\'|\'"|\')', item_text, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1).replace('\n', '\\n').replace('"', '\\"')
            result['description'] = desc
        else:
            result['description'] = ""
        
        # Extract type
        type_match = re.search(r'type\s*=\s*["\']([^"\']+)["\']', item_text)
        if type_match:
            result['type'] = type_match.group(1)
        
        # Extract default
        default_match = re.search(r'default\s*=\s*["\']([^"\']*)["\']', item_text)
        if default_match:
            result['default'] = default_match.group(1)
        
        return result
    
    def convert_module(self, output_dir: str):
        """Convert a Lua module file to Python."""
        # Extract module info
        name = self._extract_string_value(self.lua_content, 'name')
        description = self._extract_string_value(self.lua_content, 'description')
        
        # Generate Python code
        py_lines = [
            '"""',
            f'{name.capitalize()} module for LÖVE 11.5',
            '"""',
            'from ..models import Module, Function, Type, Enum, EnumConstant, Variant, Argument, Return',
            '',
            f'def get_{name}_module() -> Module:',
            '    """Get the {name} module definition."""'.format(name=name),
            '    return Module(',
            f'        name="{name}",',
            f'        description="{description}",',
            '        types=[],',
            '        functions=[],',
            '        enums=[],',
            '    )',
        ]
        
        output_file = Path(output_dir) / f'{name}.py'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(py_lines))
        
        print(f"Converted {self.lua_file_path} -> {output_file}")


def convert_all_modules(lua_modules_dir: str, output_dir: str):
    """Convert all Lua module files to Python."""
    modules_path = Path(lua_modules_dir)
    
    for module_dir in modules_path.iterdir():
        if module_dir.is_dir():
            lua_file = module_dir / f'{module_dir.name.capitalize()}.lua'
            if lua_file.exists():
                converter = LuaToPythonConverter(str(lua_file))
                converter.convert_module(output_dir)


if __name__ == '__main__':
    # Example usage
    convert_all_modules('../modules', 'love_api_py/modules')
