#!/usr/bin/env python3
"""
SimpleLisp - A Simply Scheme Interpreter
Run examples from the Harvey/Wright book without friction.

Usage:
    python main.py              # Start REPL
    python main.py script.scm   # Run a file
"""
import sys
import os
from parser import parse, ParseError
from lexer import LexerError
from eval import lisp_eval, EvalError
from primitives import create_global_env, set_load_function
from lisp_types import LispVoid, LispList, LispString, is_void


def load_file(filepath: str, env) -> None:
    """Load and execute a Scheme file."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return
    
    with open(filepath, 'r') as f:
        source = f.read()
    
    try:
        exprs = parse(source)
        for expr in exprs:
            lisp_eval(expr, env)
    except (LexerError, ParseError, EvalError) as e:
        print(f"Error in {filepath}: {e}")
        raise


def run_file(filepath: str, args: list = None) -> None:
    """Run a Scheme file as a script with optional command-line args."""
    env = create_global_env()
    
    # Set up the load function to use this environment
    def do_load(path):
        # Resolve relative paths from the script's directory
        if not os.path.isabs(path):
            script_dir = os.path.dirname(os.path.abspath(filepath))
            path = os.path.join(script_dir, path)
        load_file(path, env)
    
    set_load_function(do_load)
    
    # Set command-line arguments
    arg_list = [LispString(a) for a in (args or [])]
    env.define("*command-line-args*", LispList(arg_list))
    
    load_startup(env)
    load_file(filepath, env)


def load_startup(env) -> None:
    """Load the startup.scm standard library."""
    startup_path = os.path.join(os.path.dirname(__file__), 'startup.scm')
    if os.path.exists(startup_path):
        try:
            load_file(startup_path, env)
        except Exception as e:
            print(f"Warning: Could not load startup.scm: {e}")


def repl() -> None:
    """Run the interactive Read-Eval-Print Loop."""
    print("SimpleLisp - Simply Scheme Interpreter")
    print("Type (exit) to quit, (help) for help\n")
    
    env = create_global_env()
    
    # Set up the load function to use this environment
    def do_load(path):
        # Resolve relative paths from current directory
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        load_file(path, env)
    
    set_load_function(do_load)
    
    # Empty command-line args for REPL
    env.define("*command-line-args*", LispList([]))
    
    load_startup(env)
    
    # Track multi-line input
    buffer = ""
    
    while True:
        # Prompt
        prompt = "> " if not buffer else "  "
        
        try:
            line = input(prompt)
        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nInterrupted. Type (exit) to quit.")
            buffer = ""
            continue
        
        # Handle special commands
        stripped = line.strip().lower()
        if stripped in ("(exit)", "exit", "quit", "(quit)"):
            print("Goodbye!")
            break
        
        if stripped in ("(help)", "help"):
            print_help()
            continue
        
        # Accumulate input
        buffer += line + "\n"
        
        # Check if we have balanced parens
        if not is_balanced(buffer):
            continue
        
        # Try to evaluate
        try:
            exprs = parse(buffer)
            for expr in exprs:
                result = lisp_eval(expr, env)
                if not is_void(result):
                    print(result)
        except (LexerError, ParseError) as e:
            print(f"Syntax error: {e}")
        except EvalError as e:
            print(f"Evaluation error: {e}")
        except NameError as e:
            print(f"Name error: {e}")
        except TypeError as e:
            print(f"Type error: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        
        buffer = ""


def is_balanced(source: str) -> bool:
    """Check if parentheses are balanced (simple check)."""
    depth = 0
    in_string = False
    escape = False
    
    for c in source:
        if escape:
            escape = False
            continue
        if c == '\\' and in_string:
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
    
    return depth <= 0


def print_help():
    """Print help information."""
    print("""
SimpleLisp Help
===============

Basic Expressions:
  (+ 1 2 3)          ; => 6
  (* 2 (+ 3 4))      ; => 14
  (define x 10)      ; Define a variable
  (define (f n) ...) ; Define a function

Word Operations (Simply Scheme):
  (word 'a 'b)       ; => ab
  (first 'hello)     ; => h
  (butfirst 'hello)  ; => ello
  (sentence 'a 'b)   ; => (a b)

Higher-Order Functions:
  (every square '(1 2 3))    ; => (1 4 9)
  (keep even? '(1 2 3 4))    ; => (2 4)
  (accumulate + '(1 2 3 4))  ; => 10

Special Forms:
  (if test then else)
  (cond ((test1) expr1) ...)
  (lambda (args) body)
  (let ((a 1)) body)

Commands:
  (exit)    ; Quit the interpreter
  (help)    ; Show this help
""")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Run file mode with optional args
        run_file(sys.argv[1], sys.argv[2:])
    else:
        # Interactive REPL
        repl()


if __name__ == "__main__":
    main()
