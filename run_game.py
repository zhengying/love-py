#!/usr/bin/env python3
"""
Simple runner script for LOVE2D Python games.

Usage:
    python run_game.py examples/basic_game.py
    python run_game.py my_game.py
"""

import sys
import os

# Add love2d_py to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_game.py <game_file.py>")
        print("Example: python run_game.py examples/basic_game.py")
        sys.exit(1)
    
    game_file = sys.argv[1]
    
    if not os.path.exists(game_file):
        print(f"Error: Game file '{game_file}' not found")
        sys.exit(1)
    
    print(f"🎮 Starting LOVE2D Python...")
    print(f"📁 Loading: {game_file}")
    print(f"⌨️  Controls: WASD/Arrows to move, Click to spawn circles, ESC to quit")
    print(f"-" * 50)
    
    # Execute the game file
    with open(game_file, 'r') as f:
        code = compile(f.read(), game_file, 'exec')
        exec(code, {'__name__': '__main__', '__file__': game_file})

if __name__ == "__main__":
    main()
