# SimpleLisp

A teaching Lisp interpreter based on the *Simply Scheme* book by Harvey and Wright.

## Features

- **Simply Scheme primitives**: `word`, `sentence`, `first`, `butfirst`, `every`, `keep`, `accumulate`
- **Standard Lisp**: `define`, `lambda`, `if`, `cond`, `let`, `quote`
- **60+ built-in functions**: math, lists, I/O, vectors
- **Interactive REPL** with multi-line support

## Quick Start

```bash
# Start REPL
python main.py

# Run a file
python main.py script.scm
```

## Example

```scheme
> (define (square x) (* x x))
> (every square '(1 2 3 4 5))
(1 4 9 16 25)
> (keep even? '(1 2 3 4 5 6))
(2 4 6)
> (accumulate + '(1 2 3 4 5))
15
```

## Files

| File | Description |
|------|-------------|
| `main.py` | REPL entry point |
| `lisp_types.py` | Data types |
| `lexer.py` | Tokenizer |
| `parser.py` | S-expression parser |
| `env.py` | Environment/scoping |
| `eval.py` | Evaluator |
| `primitives.py` | Built-in functions |
| `startup.scm` | Standard library |

## Documentation

- [TUTORIAL.md](TUTORIAL.md) - Learn Lisp programming step by step
- [spec.md](spec.md) - Language specification

## License

MIT
