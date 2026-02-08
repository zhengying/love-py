#!/usr/bin/env python3
"""
SimpleLisp Test Runner
Runs all test cases and reports results.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser import parse
from eval import lisp_eval, EvalError
from primitives import create_global_env, set_load_function
from lisp_types import LispList, LispString, LispNumber, LispBool, LispSymbol, TRUE, FALSE


def load_startup(env):
    """Load the startup.scm standard library."""
    startup_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'startup.scm')
    if os.path.exists(startup_path):
        with open(startup_path, 'r') as f:
            for expr in parse(f.read()):
                lisp_eval(expr, env)


def run_test(name, code, expected, env=None):
    """Run a single test case."""
    if env is None:
        env = create_global_env()
        load_startup(env)
    
    try:
        exprs = parse(code)
        result = None
        for expr in exprs:
            result = lisp_eval(expr, env)
        
        # Compare result
        result_str = str(result) if result is not None else ""
        expected_str = str(expected)
        
        if result_str == expected_str:
            return True, None
        else:
            return False, f"Expected {expected_str}, got {result_str}"
    except Exception as e:
        return False, str(e)


def main():
    """Run all tests."""
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("SimpleLisp Test Suite")
    print("=" * 60)
    
    # =========================================================================
    # BASIC MATH TESTS
    # =========================================================================
    print("\n📐 Basic Math")
    print("-" * 40)
    
    tests = [
        ("addition", "(+ 1 2 3)", "6"),
        ("subtraction", "(- 10 3)", "7"),
        ("negation", "(- 5)", "-5"),
        ("multiplication", "(* 2 3 4)", "24"),
        ("division", "(/ 20 4)", "5"),
        ("quotient", "(quotient 10 3)", "3"),
        ("remainder", "(remainder 10 3)", "1"),
        ("abs positive", "(abs 5)", "5"),
        ("abs negative", "(abs -5)", "5"),
        ("sqrt", "(sqrt 16)", "4"),
        ("max", "(max 3 7 2 9 1)", "9"),
        ("min", "(min 3 7 2 9 1)", "1"),
        ("nested", "(* 2 (+ 3 4))", "14"),
        ("complex", "(+ (* 2 3) (* 4 5))", "26"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # COMPARISON TESTS
    # =========================================================================
    print("\n⚖️  Comparisons")
    print("-" * 40)
    
    tests = [
        ("equal true", "(= 5 5)", "#t"),
        ("equal false", "(= 5 6)", "#f"),
        ("less than true", "(< 3 5)", "#t"),
        ("less than false", "(< 5 3)", "#f"),
        ("greater than true", "(> 5 3)", "#t"),
        ("greater than false", "(> 3 5)", "#f"),
        ("less or equal", "(<= 5 5)", "#t"),
        ("greater or equal", "(>= 5 5)", "#t"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # WORD TESTS
    # =========================================================================
    print("\n📝 Words")
    print("-" * 40)
    
    tests = [
        ("word concat", "(word 'super 'hero)", "superhero"),
        ("word with number", "(word 'item 1)", "item1"),
        ("first symbol", "(first 'hello)", "h"),
        ("first string", '(first "hello")', "h"),
        ("butfirst", "(butfirst 'hello)", "ello"),
        ("bf alias", "(bf 'hello)", "ello"),
        ("last", "(last 'hello)", "o"),
        ("butlast", "(butlast 'hello)", "hell"),
        ("bl alias", "(bl 'hello)", "hell"),
        ("count word", "(count 'hello)", "5"),
        ("item word", "(item 2 'hello)", "e"),
        ("empty string", '(empty? "")', "#t"),
        ("empty symbol false", "(empty? 'hello)", "#f"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # SENTENCE/LIST TESTS
    # =========================================================================
    print("\n📋 Sentences and Lists")
    print("-" * 40)
    
    tests = [
        ("sentence", "(sentence 'hello 'world)", "(hello world)"),
        ("se alias", "(se 'a 'b 'c)", "(a b c)"),
        ("sentence flatten", "(sentence 'hello '(my friend))", "(hello my friend)"),
        ("first list", "(first '(apple banana cherry))", "apple"),
        ("butfirst list", "(butfirst '(apple banana cherry))", "(banana cherry)"),
        ("last list", "(last '(apple banana cherry))", "cherry"),
        ("butlast list", "(butlast '(apple banana cherry))", "(apple banana)"),
        ("cons", "(cons 'a '(b c))", "(a b c)"),
        ("car", "(car '(a b c))", "a"),
        ("cdr", "(cdr '(a b c))", "(b c)"),
        ("list", "(list 1 2 3)", "(1 2 3)"),
        ("append", "(append '(a b) '(c d))", "(a b c d)"),
        ("reverse", "(reverse '(1 2 3))", "(3 2 1)"),
        ("length", "(length '(a b c d))", "4"),
        ("count list", "(count '(a b c d e))", "5"),
        ("null empty", "(null? '())", "#t"),
        ("null non-empty", "(null? '(1))", "#f"),
        ("list? true", "(list? '(1 2))", "#t"),
        ("list? false", "(list? 5)", "#f"),
        ("item list", "(item 2 '(a b c))", "b"),
        ("empty list", "(empty? '())", "#t"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # DEFINE AND LAMBDA TESTS
    # =========================================================================
    print("\n🔧 Define and Lambda")
    print("-" * 40)
    
    env = create_global_env()
    load_startup(env)
    
    tests = [
        ("define var", "(define x 10) x", "10"),
        ("define func", "(define (square n) (* n n)) (square 5)", "25"),
        ("lambda call", "((lambda (x) (* x x)) 7)", "49"),
        ("lambda multi", "((lambda (a b) (+ a b)) 3 4)", "7"),
        ("closure", "(define (make-adder n) (lambda (x) (+ x n))) ((make-adder 5) 10)", "15"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected, env)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # CONDITIONAL TESTS
    # =========================================================================
    print("\n🔀 Conditionals")
    print("-" * 40)
    
    tests = [
        ("if true", "(if (> 5 3) 'yes 'no)", "yes"),
        ("if false", "(if (< 5 3) 'yes 'no)", "no"),
        ("cond first", "(cond ((= 1 1) 'first) ((= 2 2) 'second))", "first"),
        ("cond second", "(cond ((= 1 2) 'first) ((= 2 2) 'second))", "second"),
        ("cond else", "(cond ((= 1 2) 'first) (else 'default))", "default"),
        ("and true", "(and #t #t)", "#t"),
        ("and false", "(and #t #f)", "#f"),
        ("and short-circuit", "(and #f (/ 1 0))", "#f"),
        ("or true", "(or #f #t)", "#t"),
        ("or false", "(or #f #f)", "#f"),
        ("or short-circuit", "(or #t (/ 1 0))", "#t"),
        ("not true", "(not #t)", "#f"),
        ("not false", "(not #f)", "#t"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # LET TESTS
    # =========================================================================
    print("\n📦 Let Bindings")
    print("-" * 40)
    
    tests = [
        ("let simple", "(let ((x 5)) x)", "5"),
        ("let multi", "(let ((x 10) (y 20)) (+ x y))", "30"),
        ("let nested", "(let ((x 5)) (let ((y 10)) (+ x y)))", "15"),
        ("let shadow", "(define x 100) (let ((x 5)) x)", "5"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # TYPE PREDICATE TESTS
    # =========================================================================
    print("\n🏷️  Type Predicates")
    print("-" * 40)
    
    tests = [
        ("number? true", "(number? 42)", "#t"),
        ("number? false", "(number? 'hello)", "#f"),
        ("symbol? true", "(symbol? 'hello)", "#t"),
        ("symbol? false", "(symbol? 42)", "#f"),
        ("string? true", '(string? "hello")', "#t"),
        ("string? false", "(string? 'hello)", "#f"),
        ("list? true", "(list? '(1 2))", "#t"),
        ("list? false", "(list? 42)", "#f"),
        ("boolean? true", "(boolean? #t)", "#t"),
        ("boolean? false", "(boolean? 42)", "#f"),
        ("procedure? true", "(procedure? +)", "#t"),
        ("procedure? false", "(procedure? 42)", "#f"),
        ("word? symbol", "(word? 'hello)", "#t"),
        ("word? number", "(word? 42)", "#t"),
        ("word? string", '(word? "hello")', "#t"),
        ("word? list", "(word? '(1 2))", "#f"),
        ("even? true", "(even? 4)", "#t"),
        ("even? false", "(even? 5)", "#f"),
        ("odd? true", "(odd? 5)", "#t"),
        ("odd? false", "(odd? 4)", "#f"),
        ("integer? true", "(integer? 5)", "#t"),
        ("integer? false", "(integer? 5.5)", "#f"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # RECURSION TESTS
    # =========================================================================
    print("\n🔄 Recursion")
    print("-" * 40)
    
    tests = [
        ("factorial 0", "(define (factorial n) (if (= n 0) 1 (* n (factorial (- n 1))))) (factorial 0)", "1"),
        ("factorial 5", "(define (factorial n) (if (= n 0) 1 (* n (factorial (- n 1))))) (factorial 5)", "120"),
        ("fib 0", "(define (fib n) (cond ((= n 0) 0) ((= n 1) 1) (else (+ (fib (- n 1)) (fib (- n 2)))))) (fib 0)", "0"),
        ("fib 1", "(define (fib n) (cond ((= n 0) 0) ((= n 1) 1) (else (+ (fib (- n 1)) (fib (- n 2)))))) (fib 1)", "1"),
        ("fib 10", "(define (fib n) (cond ((= n 0) 0) ((= n 1) 1) (else (+ (fib (- n 1)) (fib (- n 2)))))) (fib 10)", "55"),
        ("sum list", "(define (sum-list lst) (if (null? lst) 0 (+ (car lst) (sum-list (cdr lst))))) (sum-list '(1 2 3 4 5))", "15"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # HIGHER-ORDER FUNCTION TESTS
    # =========================================================================
    print("\n🚀 Higher-Order Functions")
    print("-" * 40)
    
    env = create_global_env()
    load_startup(env)
    lisp_eval(parse("(define (square x) (* x x))")[0], env)
    
    tests = [
        ("every square", "(every square '(1 2 3 4))", "(1 4 9 16)"),
        ("every first", "(every first '(apple banana))", "(a b)"),
        ("keep even", "(keep even? '(1 2 3 4 5 6))", "(2 4 6)"),
        ("keep odd", "(keep odd? '(1 2 3 4 5 6))", "(1 3 5)"),
        ("keep lambda", "(keep (lambda (x) (> x 3)) '(1 5 2 7 3))", "(5 7)"),
        ("accumulate +", "(accumulate + '(1 2 3 4 5))", "15"),
        ("accumulate *", "(accumulate * '(1 2 3 4 5))", "120"),
        ("accumulate word", "(accumulate word '(un believ able))", "unbelievable"),
        ("map", "(map square '(1 2 3 4))", "(1 4 9 16)"),
        ("filter", "(filter even? '(1 2 3 4 5 6))", "(2 4 6)"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected, env)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # QUOTE TESTS
    # =========================================================================
    print("\n💬 Quote")
    print("-" * 40)
    
    tests = [
        ("quote symbol", "'hello", "hello"),
        ("quote list", "'(1 2 3)", "(1 2 3)"),
        ("quote nested", "'(+ 1 2)", "(+ 1 2)"),
        ("quote empty", "'()", "()"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # BEGIN TESTS
    # =========================================================================
    print("\n📜 Begin")
    print("-" * 40)
    
    tests = [
        ("begin single", "(begin 42)", "42"),
        ("begin multi", "(begin 1 2 3)", "3"),
        ("begin with define", "(begin (define x 5) (+ x 10))", "15"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # SET! TESTS
    # =========================================================================
    print("\n✏️  Set!")
    print("-" * 40)
    
    tests = [
        ("set! basic", "(define x 5) (set! x 10) x", "10"),
        ("set! increment", "(define counter 0) (set! counter (+ counter 1)) counter", "1"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # EQUAL? TESTS
    # =========================================================================
    print("\n🔍 Equal?")
    print("-" * 40)
    
    tests = [
        ("equal numbers", "(equal? 5 5)", "#t"),
        ("equal symbols", "(equal? 'hello 'hello)", "#t"),
        ("equal lists", "(equal? '(1 2 3) '(1 2 3))", "#t"),
        ("not equal numbers", "(equal? 5 6)", "#f"),
        ("not equal lists", "(equal? '(1 2) '(1 2 3))", "#f"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # MEMBER TESTS
    # =========================================================================
    print("\n🔎 Member")
    print("-" * 40)
    
    tests = [
        ("member found", "(member 'b '(a b c))", "(b c)"),
        ("member not found", "(member 'x '(a b c))", "#f"),
        ("member first", "(member 'a '(a b c))", "(a b c)"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # VECTOR TESTS
    # =========================================================================
    print("\n📊 Vectors")
    print("-" * 40)
    
    tests = [
        ("make-vector", "(define v (make-vector 3)) (vector-length v)", "3"),
        ("vector-ref", "(define v (make-vector 3 5)) (vector-ref v 1)", "5"),
        ("vector-set!", "(define v (make-vector 3 0)) (vector-set! v 0 42) (vector-ref v 0)", "42"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # CADR/CADDR TESTS (from startup.scm)
    # =========================================================================
    print("\n📚 Library Functions (startup.scm)")
    print("-" * 40)
    
    tests = [
        ("cadr", "(cadr '(a b c))", "b"),
        ("caddr", "(caddr '(a b c d))", "c"),
        ("positive?", "(positive? 5)", "#t"),
        ("negative?", "(negative? -5)", "#t"),
        ("zero?", "(zero? 0)", "#t"),
        ("list-ref", "(list-ref '(a b c d) 2)", "c"),
    ]
    
    for name, code, expected in tests:
        success, error = run_test(name, code, expected)
        if success:
            print(f"  ✓ {name}")
            passed += 1
        else:
            print(f"  ✗ {name}: {error}")
            failed += 1

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 60)
    total = passed + failed
    if failed == 0:
        print(f"🎉 ALL {total} TESTS PASSED!")
    else:
        print(f"Results: {passed}/{total} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
