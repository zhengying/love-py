"""
SimpleLisp Primitives
Built-in functions for the Simply Scheme interpreter.
"""
from typing import List, Any
from lisp_types import (
    LispValue, LispNumber, LispSymbol, LispString, LispBool,
    LispList, LispVector, LispPrimitive, LispProcedure, LispVoid,
    TRUE, FALSE, VOID, NIL,
    is_truthy, is_list, is_number, is_symbol, is_string, is_word,
    is_procedure, is_boolean, is_vector, to_python_string
)
from env import Environment


# ============================================================================
# Simply Scheme Word & Sentence Primitives (Ch 5)
# ============================================================================

def prim_word(*args: LispValue) -> LispSymbol:
    """Concatenate arguments into a single word (symbol)."""
    parts = []
    for arg in args:
        parts.append(to_python_string(arg))
    return LispSymbol(''.join(parts))


def prim_sentence(*args: LispValue) -> LispList:
    """
    Variadic flattening constructor.
    If arg is list -> unwrap/splice it
    If arg is atom -> add to result list
    """
    result = []
    for arg in args:
        if isinstance(arg, LispList):
            result.extend(arg.elements)
        else:
            result.append(arg)
    return LispList(result)


def prim_first(arg: LispValue) -> LispValue:
    """
    If arg is list -> return 1st element
    If arg is word -> return 1st character (as symbol)
    """
    if isinstance(arg, LispList):
        if arg.is_empty():
            raise ValueError("first: empty list")
        return arg[0]
    elif is_word(arg):
        s = to_python_string(arg)
        if len(s) == 0:
            raise ValueError("first: empty word")
        return LispSymbol(s[0])
    else:
        raise TypeError(f"first: expected list or word, got {type(arg).__name__}")


def prim_butfirst(arg: LispValue) -> LispValue:
    """
    If arg is list -> return rest (cdr)
    If arg is word -> return string slice [1:] as symbol
    """
    if isinstance(arg, LispList):
        if arg.is_empty():
            raise ValueError("butfirst: empty list")
        return LispList(arg.elements[1:])
    elif is_word(arg):
        s = to_python_string(arg)
        if len(s) == 0:
            raise ValueError("butfirst: empty word")
        result = s[1:]
        if result == "":
            return LispString("")
        return LispSymbol(result)
    else:
        raise TypeError(f"butfirst: expected list or word, got {type(arg).__name__}")


def prim_last(arg: LispValue) -> LispValue:
    """
    If arg is list -> return last element
    If arg is word -> return last character (as symbol)
    """
    if isinstance(arg, LispList):
        if arg.is_empty():
            raise ValueError("last: empty list")
        return arg[-1]
    elif is_word(arg):
        s = to_python_string(arg)
        if len(s) == 0:
            raise ValueError("last: empty word")
        return LispSymbol(s[-1])
    else:
        raise TypeError(f"last: expected list or word, got {type(arg).__name__}")


def prim_butlast(arg: LispValue) -> LispValue:
    """
    If arg is list -> return all but last
    If arg is word -> return string slice [:-1] as symbol
    """
    if isinstance(arg, LispList):
        if arg.is_empty():
            raise ValueError("butlast: empty list")
        return LispList(arg.elements[:-1])
    elif is_word(arg):
        s = to_python_string(arg)
        if len(s) == 0:
            raise ValueError("butlast: empty word")
        result = s[:-1]
        if result == "":
            return LispString("")
        return LispSymbol(result)
    else:
        raise TypeError(f"butlast: expected list or word, got {type(arg).__name__}")


def prim_item(n: LispValue, obj: LispValue) -> LispValue:
    """Return n-th element (1-based index!)."""
    if not isinstance(n, LispNumber):
        raise TypeError("item: first argument must be a number")
    
    index = int(n.value) - 1  # Convert to 0-based
    
    if isinstance(obj, LispList):
        if index < 0 or index >= len(obj):
            raise ValueError(f"item: index {int(n.value)} out of range")
        return obj[index]
    elif is_word(obj):
        s = to_python_string(obj)
        if index < 0 or index >= len(s):
            raise ValueError(f"item: index {int(n.value)} out of range")
        return LispSymbol(s[index])
    else:
        raise TypeError(f"item: expected list or word, got {type(obj).__name__}")


def prim_empty(arg: LispValue) -> LispBool:
    """Returns true for () (empty list) AND "" (empty string)."""
    if isinstance(arg, LispList):
        return TRUE if arg.is_empty() else FALSE
    elif isinstance(arg, LispString):
        return TRUE if arg.value == "" else FALSE
    elif isinstance(arg, LispSymbol):
        return TRUE if arg.name == "" else FALSE
    return FALSE


def prim_count(arg: LispValue) -> LispNumber:
    """Return length of list or word."""
    if isinstance(arg, LispList):
        return LispNumber(len(arg))
    elif is_word(arg):
        return LispNumber(len(to_python_string(arg)))
    else:
        raise TypeError(f"count: expected list or word, got {type(arg).__name__}")


# ============================================================================
# Math Primitives
# ============================================================================

def prim_add(*args: LispValue) -> LispNumber:
    result = 0
    for arg in args:
        if not isinstance(arg, LispNumber):
            raise TypeError(f"+: expected number, got {type(arg).__name__}")
        result += arg.value
    return LispNumber(result)


def prim_sub(*args: LispValue) -> LispNumber:
    if len(args) == 0:
        raise ValueError("-: requires at least 1 argument")
    if not isinstance(args[0], LispNumber):
        raise TypeError(f"-: expected number, got {type(args[0]).__name__}")
    if len(args) == 1:
        return LispNumber(-args[0].value)
    result = args[0].value
    for arg in args[1:]:
        if not isinstance(arg, LispNumber):
            raise TypeError(f"-: expected number, got {type(arg).__name__}")
        result -= arg.value
    return LispNumber(result)


def prim_mul(*args: LispValue) -> LispNumber:
    result = 1
    for arg in args:
        if not isinstance(arg, LispNumber):
            raise TypeError(f"*: expected number, got {type(arg).__name__}")
        result *= arg.value
    return LispNumber(result)


def prim_div(*args: LispValue) -> LispNumber:
    if len(args) == 0:
        raise ValueError("/: requires at least 1 argument")
    if not isinstance(args[0], LispNumber):
        raise TypeError(f"/: expected number, got {type(args[0]).__name__}")
    if len(args) == 1:
        return LispNumber(1 / args[0].value)
    result = args[0].value
    for arg in args[1:]:
        if not isinstance(arg, LispNumber):
            raise TypeError(f"/: expected number, got {type(arg).__name__}")
        result /= arg.value
    return LispNumber(result)


def prim_quotient(a: LispValue, b: LispValue) -> LispNumber:
    if not isinstance(a, LispNumber) or not isinstance(b, LispNumber):
        raise TypeError("quotient: expected numbers")
    return LispNumber(int(a.value) // int(b.value))


def prim_remainder(a: LispValue, b: LispValue) -> LispNumber:
    if not isinstance(a, LispNumber) or not isinstance(b, LispNumber):
        raise TypeError("remainder: expected numbers")
    return LispNumber(int(a.value) % int(b.value))


def prim_eq(a: LispValue, b: LispValue) -> LispBool:
    if not isinstance(a, LispNumber) or not isinstance(b, LispNumber):
        raise TypeError("=: expected numbers")
    return TRUE if a.value == b.value else FALSE


def prim_lt(a: LispValue, b: LispValue) -> LispBool:
    if not isinstance(a, LispNumber) or not isinstance(b, LispNumber):
        raise TypeError("<: expected numbers")
    return TRUE if a.value < b.value else FALSE


def prim_gt(a: LispValue, b: LispValue) -> LispBool:
    if not isinstance(a, LispNumber) or not isinstance(b, LispNumber):
        raise TypeError(">: expected numbers")
    return TRUE if a.value > b.value else FALSE


def prim_le(a: LispValue, b: LispValue) -> LispBool:
    if not isinstance(a, LispNumber) or not isinstance(b, LispNumber):
        raise TypeError("<=: expected numbers")
    return TRUE if a.value <= b.value else FALSE


def prim_ge(a: LispValue, b: LispValue) -> LispBool:
    if not isinstance(a, LispNumber) or not isinstance(b, LispNumber):
        raise TypeError(">=: expected numbers")
    return TRUE if a.value >= b.value else FALSE


def prim_abs(a: LispValue) -> LispNumber:
    if not isinstance(a, LispNumber):
        raise TypeError("abs: expected number")
    return LispNumber(abs(a.value))


def prim_sqrt(a: LispValue) -> LispNumber:
    if not isinstance(a, LispNumber):
        raise TypeError("sqrt: expected number")
    import math
    return LispNumber(math.sqrt(a.value))


def prim_max(*args: LispValue) -> LispNumber:
    if len(args) == 0:
        raise ValueError("max: requires at least 1 argument")
    values = []
    for arg in args:
        if not isinstance(arg, LispNumber):
            raise TypeError("max: expected numbers")
        values.append(arg.value)
    return LispNumber(max(values))


def prim_min(*args: LispValue) -> LispNumber:
    if len(args) == 0:
        raise ValueError("min: requires at least 1 argument")
    values = []
    for arg in args:
        if not isinstance(arg, LispNumber):
            raise TypeError("min: expected numbers")
        values.append(arg.value)
    return LispNumber(min(values))


def prim_random(n: LispValue) -> LispNumber:
    if not isinstance(n, LispNumber):
        raise TypeError("random: expected number")
    import random
    return LispNumber(random.randint(0, int(n.value) - 1))


# ============================================================================
# Logic Primitives
# ============================================================================

def prim_not(arg: LispValue) -> LispBool:
    return FALSE if is_truthy(arg) else TRUE


def prim_equal(a: LispValue, b: LispValue) -> LispBool:
    """Deep comparison."""
    return TRUE if lisp_equal(a, b) else FALSE


def lisp_equal(a: LispValue, b: LispValue) -> bool:
    """Deep equality check."""
    if type(a) != type(b):
        return False
    if isinstance(a, LispNumber):
        return a.value == b.value
    if isinstance(a, LispSymbol):
        return a.name == b.name
    if isinstance(a, LispString):
        return a.value == b.value
    if isinstance(a, LispBool):
        return a.value == b.value
    if isinstance(a, LispList):
        if len(a) != len(b):
            return False
        return all(lisp_equal(x, y) for x, y in zip(a.elements, b.elements))
    if isinstance(a, LispVector):
        if len(a.elements) != len(b.elements):
            return False
        return all(lisp_equal(x, y) for x, y in zip(a.elements, b.elements))
    return a is b


def prim_member(item: LispValue, lst: LispValue) -> LispValue:
    """Check if item is in list."""
    if not isinstance(lst, LispList):
        raise TypeError("member: second argument must be a list")
    for i, elem in enumerate(lst.elements):
        if lisp_equal(item, elem):
            return LispList(lst.elements[i:])
    return FALSE


# ============================================================================
# List Primitives
# ============================================================================

def prim_cons(a: LispValue, b: LispValue) -> LispList:
    if not isinstance(b, LispList):
        raise TypeError("cons: second argument must be a list")
    return LispList([a] + b.elements)


def prim_car(lst: LispValue) -> LispValue:
    if not isinstance(lst, LispList):
        raise TypeError("car: expected list")
    if lst.is_empty():
        raise ValueError("car: empty list")
    return lst[0]


def prim_cdr(lst: LispValue) -> LispList:
    if not isinstance(lst, LispList):
        raise TypeError("cdr: expected list")
    if lst.is_empty():
        raise ValueError("cdr: empty list")
    return LispList(lst.elements[1:])


def prim_list(*args: LispValue) -> LispList:
    return LispList(list(args))


def prim_length(lst: LispValue) -> LispNumber:
    if not isinstance(lst, LispList):
        raise TypeError("length: expected list")
    return LispNumber(len(lst))


def prim_append(*args: LispValue) -> LispList:
    result = []
    for arg in args:
        if not isinstance(arg, LispList):
            raise TypeError("append: expected lists")
        result.extend(arg.elements)
    return LispList(result)


def prim_null(arg: LispValue) -> LispBool:
    if isinstance(arg, LispList):
        return TRUE if arg.is_empty() else FALSE
    return FALSE


def prim_list_q(arg: LispValue) -> LispBool:
    return TRUE if isinstance(arg, LispList) else FALSE


def prim_reverse(lst: LispValue) -> LispList:
    if not isinstance(lst, LispList):
        raise TypeError("reverse: expected list")
    return LispList(lst.elements[::-1])


# ============================================================================
# Type Check Primitives
# ============================================================================

def prim_number_q(arg: LispValue) -> LispBool:
    return TRUE if is_number(arg) else FALSE


def prim_word_q(arg: LispValue) -> LispBool:
    """True for string/symbol/number."""
    return TRUE if is_word(arg) else FALSE


def prim_boolean_q(arg: LispValue) -> LispBool:
    return TRUE if is_boolean(arg) else FALSE


def prim_procedure_q(arg: LispValue) -> LispBool:
    return TRUE if is_procedure(arg) else FALSE


def prim_symbol_q(arg: LispValue) -> LispBool:
    return TRUE if is_symbol(arg) else FALSE


def prim_string_q(arg: LispValue) -> LispBool:
    return TRUE if is_string(arg) else FALSE


def prim_integer_q(arg: LispValue) -> LispBool:
    if isinstance(arg, LispNumber):
        return TRUE if isinstance(arg.value, int) or arg.value.is_integer() else FALSE
    return FALSE


def prim_even_q(arg: LispValue) -> LispBool:
    if not isinstance(arg, LispNumber):
        raise TypeError("even?: expected number")
    return TRUE if int(arg.value) % 2 == 0 else FALSE


def prim_odd_q(arg: LispValue) -> LispBool:
    if not isinstance(arg, LispNumber):
        raise TypeError("odd?: expected number")
    return TRUE if int(arg.value) % 2 != 0 else FALSE


# ============================================================================
# I/O Primitives
# ============================================================================

def prim_display(arg: LispValue) -> LispVoid:
    """Print representation to stdout (no quotes for strings)."""
    if isinstance(arg, LispString):
        print(arg.value, end='')
    elif isinstance(arg, LispVoid):
        pass
    else:
        print(repr(arg), end='')
    return VOID


def prim_show(arg: LispValue) -> LispVoid:
    """Same as display but follows with a newline."""
    prim_display(arg)
    print()
    return VOID


def prim_newline() -> LispVoid:
    """Print a newline."""
    print()
    return VOID


def prim_read() -> LispValue:
    """Read one S-expression from stdin."""
    from parser import parse_one
    try:
        line = input()
        result = parse_one(line)
        return result if result is not None else NIL
    except EOFError:
        return NIL


def prim_read_line() -> LispString:
    """Read a line from stdin."""
    try:
        return LispString(input())
    except EOFError:
        return LispString("")


# Global reference to load function (set by create_global_env)
_load_file_func = None


def prim_load(filename: LispValue) -> LispVoid:
    """Load and execute a Scheme file."""
    if not isinstance(filename, LispString):
        raise TypeError("load: expected string filename")
    if _load_file_func is None:
        raise RuntimeError("load: interpreter not initialized")
    _load_file_func(filename.value)
    return VOID


# ============================================================================
# Vector Primitives
# ============================================================================

def prim_make_vector(size: LispValue, fill: LispValue = None) -> LispVector:
    if not isinstance(size, LispNumber):
        raise TypeError("make-vector: size must be a number")
    n = int(size.value)
    default = fill if fill is not None else LispNumber(0)
    return LispVector([default] * n)


def prim_vector_ref(vec: LispValue, index: LispValue) -> LispValue:
    if not isinstance(vec, LispVector):
        raise TypeError("vector-ref: first argument must be a vector")
    if not isinstance(index, LispNumber):
        raise TypeError("vector-ref: index must be a number")
    i = int(index.value)
    if i < 0 or i >= len(vec.elements):
        raise ValueError(f"vector-ref: index {i} out of range")
    return vec.elements[i]


def prim_vector_set(vec: LispValue, index: LispValue, val: LispValue) -> LispVoid:
    if not isinstance(vec, LispVector):
        raise TypeError("vector-set!: first argument must be a vector")
    if not isinstance(index, LispNumber):
        raise TypeError("vector-set!: index must be a number")
    i = int(index.value)
    if i < 0 or i >= len(vec.elements):
        raise ValueError(f"vector-set!: index {i} out of range")
    vec.elements[i] = val
    return VOID


def prim_vector_length(vec: LispValue) -> LispNumber:
    if not isinstance(vec, LispVector):
        raise TypeError("vector-length: expected vector")
    return LispNumber(len(vec.elements))


# ============================================================================
# Register All Primitives
# ============================================================================

def create_global_env() -> Environment:
    """Create the global environment with all primitives."""
    env = Environment()
    
    # Simply Scheme word/sentence
    env.define("word", LispPrimitive("word", prim_word))
    env.define("sentence", LispPrimitive("sentence", prim_sentence))
    env.define("se", LispPrimitive("se", prim_sentence))
    env.define("first", LispPrimitive("first", prim_first))
    env.define("butfirst", LispPrimitive("butfirst", prim_butfirst))
    env.define("bf", LispPrimitive("bf", prim_butfirst))
    env.define("last", LispPrimitive("last", prim_last))
    env.define("butlast", LispPrimitive("butlast", prim_butlast))
    env.define("bl", LispPrimitive("bl", prim_butlast))
    env.define("item", LispPrimitive("item", prim_item))
    env.define("empty?", LispPrimitive("empty?", prim_empty))
    env.define("count", LispPrimitive("count", prim_count))
    
    # Math
    env.define("+", LispPrimitive("+", prim_add))
    env.define("-", LispPrimitive("-", prim_sub))
    env.define("*", LispPrimitive("*", prim_mul))
    env.define("/", LispPrimitive("/", prim_div))
    env.define("quotient", LispPrimitive("quotient", prim_quotient))
    env.define("remainder", LispPrimitive("remainder", prim_remainder))
    env.define("=", LispPrimitive("=", prim_eq))
    env.define("<", LispPrimitive("<", prim_lt))
    env.define(">", LispPrimitive(">", prim_gt))
    env.define("<=", LispPrimitive("<=", prim_le))
    env.define(">=", LispPrimitive(">=", prim_ge))
    env.define("abs", LispPrimitive("abs", prim_abs))
    env.define("sqrt", LispPrimitive("sqrt", prim_sqrt))
    env.define("max", LispPrimitive("max", prim_max))
    env.define("min", LispPrimitive("min", prim_min))
    env.define("random", LispPrimitive("random", prim_random))
    
    # Logic
    env.define("not", LispPrimitive("not", prim_not))
    env.define("equal?", LispPrimitive("equal?", prim_equal))
    env.define("member", LispPrimitive("member", prim_member))
    
    # Lists
    env.define("cons", LispPrimitive("cons", prim_cons))
    env.define("car", LispPrimitive("car", prim_car))
    env.define("cdr", LispPrimitive("cdr", prim_cdr))
    env.define("list", LispPrimitive("list", prim_list))
    env.define("length", LispPrimitive("length", prim_length))
    env.define("append", LispPrimitive("append", prim_append))
    env.define("null?", LispPrimitive("null?", prim_null))
    env.define("list?", LispPrimitive("list?", prim_list_q))
    env.define("reverse", LispPrimitive("reverse", prim_reverse))
    
    # Type checks
    env.define("number?", LispPrimitive("number?", prim_number_q))
    env.define("word?", LispPrimitive("word?", prim_word_q))
    env.define("boolean?", LispPrimitive("boolean?", prim_boolean_q))
    env.define("procedure?", LispPrimitive("procedure?", prim_procedure_q))
    env.define("symbol?", LispPrimitive("symbol?", prim_symbol_q))
    env.define("string?", LispPrimitive("string?", prim_string_q))
    env.define("integer?", LispPrimitive("integer?", prim_integer_q))
    env.define("even?", LispPrimitive("even?", prim_even_q))
    env.define("odd?", LispPrimitive("odd?", prim_odd_q))
    
    # I/O
    env.define("display", LispPrimitive("display", prim_display))
    env.define("show", LispPrimitive("show", prim_show))
    env.define("newline", LispPrimitive("newline", prim_newline))
    env.define("read", LispPrimitive("read", prim_read))
    env.define("read-line", LispPrimitive("read-line", prim_read_line))
    
    # Vectors
    env.define("make-vector", LispPrimitive("make-vector", prim_make_vector))
    env.define("vector-ref", LispPrimitive("vector-ref", prim_vector_ref))
    env.define("vector-set!", LispPrimitive("vector-set!", prim_vector_set))
    env.define("vector-length", LispPrimitive("vector-length", prim_vector_length))
    
    # Load (file importing)
    env.define("load", LispPrimitive("load", prim_load))
    
    return env


def set_load_function(func):
    """Set the load function for the interpreter."""
    global _load_file_func
    _load_file_func = func
