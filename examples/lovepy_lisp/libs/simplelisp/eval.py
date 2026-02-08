"""
SimpleLisp Evaluator
Core evaluation logic for the Simply Scheme interpreter.
"""
from typing import List, Optional, Any
from lisp_types import (
    LispValue, LispNumber, LispSymbol, LispString, LispBool,
    LispList, LispVector, LispProcedure, LispPrimitive, LispClosure,
    LispVoid, TRUE, FALSE, VOID, NIL,
    is_truthy, is_list
)
from env import Environment


class EvalError(Exception):
    """Evaluation error."""
    pass


def lisp_eval(expr: LispValue, env: Environment) -> LispValue:
    """Evaluate a Lisp expression in an environment."""
    
    # Self-evaluating types
    if isinstance(expr, (LispNumber, LispString, LispBool, LispVoid, LispVector)):
        return expr
    
    if isinstance(expr, LispProcedure):
        return expr
    
    # Symbol lookup
    if isinstance(expr, LispSymbol):
        return env.lookup(expr.name)
    
    # List evaluation (function call or special form)
    if isinstance(expr, LispList):
        if expr.is_empty():
            return NIL
        
        first = expr[0]
        
        # Check for special forms
        if isinstance(first, LispSymbol):
            name = first.name
            
            if name == "quote":
                return eval_quote(expr, env)
            elif name == "if":
                return eval_if(expr, env)
            elif name == "define":
                return eval_define(expr, env)
            elif name == "lambda":
                return eval_lambda(expr, env)
            elif name == "cond":
                return eval_cond(expr, env)
            elif name == "and":
                return eval_and(expr, env)
            elif name == "or":
                return eval_or(expr, env)
            elif name == "let":
                return eval_let(expr, env)
            elif name == "begin":
                return eval_begin(expr, env)
            elif name == "set!":
                return eval_set(expr, env)
        
        # Function application
        return eval_application(expr, env)
    
    raise EvalError(f"Cannot evaluate: {expr}")


def eval_quote(expr: LispList, env: Environment) -> LispValue:
    """(quote expr) - return expr unevaluated."""
    if len(expr) != 2:
        raise EvalError("quote requires exactly 1 argument")
    return expr[1]


def eval_if(expr: LispList, env: Environment) -> LispValue:
    """(if test then else) - conditional."""
    if len(expr) < 3:
        raise EvalError("if requires at least 2 arguments")
    
    test = lisp_eval(expr[1], env)
    
    if is_truthy(test):
        return lisp_eval(expr[2], env)
    elif len(expr) > 3:
        return lisp_eval(expr[3], env)
    else:
        return VOID


def eval_define(expr: LispList, env: Environment) -> LispValue:
    """
    (define x value) - bind x to value
    (define (f args...) body) - syntactic sugar for (define f (lambda (args...) body))
    """
    if len(expr) < 3:
        raise EvalError("define requires at least 2 arguments")
    
    target = expr[1]
    
    # Function definition sugar: (define (f x y) body...)
    if isinstance(target, LispList) and len(target) > 0:
        func_name = target[0]
        if not isinstance(func_name, LispSymbol):
            raise EvalError("Function name must be a symbol")
        
        params = [p.name for p in target[1:] if isinstance(p, LispSymbol)]
        body = list(expr[2:])
        
        closure = LispClosure(params, body, env, func_name.name)
        env.define(func_name.name, closure)
        return VOID
    
    # Simple binding: (define x value)
    if not isinstance(target, LispSymbol):
        raise EvalError("define target must be a symbol")
    
    value = lisp_eval(expr[2], env)
    env.define(target.name, value)
    return VOID


def eval_lambda(expr: LispList, env: Environment) -> LispClosure:
    """(lambda (params...) body...) - create closure."""
    if len(expr) < 3:
        raise EvalError("lambda requires parameter list and body")
    
    param_list = expr[1]
    if not isinstance(param_list, LispList):
        raise EvalError("lambda parameters must be a list")
    
    params = []
    for p in param_list:
        if not isinstance(p, LispSymbol):
            raise EvalError("lambda parameter must be a symbol")
        params.append(p.name)
    
    body = list(expr[2:])
    return LispClosure(params, body, env)


def eval_cond(expr: LispList, env: Environment) -> LispValue:
    """(cond (test expr...)...) - multi-way conditional."""
    for clause in expr[1:]:
        if not isinstance(clause, LispList) or len(clause) < 1:
            raise EvalError("cond clause must be a non-empty list")
        
        test = clause[0]
        
        # Handle 'else' clause
        if isinstance(test, LispSymbol) and test.name == "else":
            # Evaluate all expressions in else clause, return last
            result = VOID
            for e in clause[1:]:
                result = lisp_eval(e, env)
            return result
        
        # Evaluate test
        test_result = lisp_eval(test, env)
        if is_truthy(test_result):
            # Evaluate all expressions in clause, return last
            if len(clause) == 1:
                return test_result  # Return test result if no body
            result = VOID
            for e in clause[1:]:
                result = lisp_eval(e, env)
            return result
    
    return VOID


def eval_and(expr: LispList, env: Environment) -> LispValue:
    """(and expr...) - short-circuit and."""
    result: LispValue = TRUE
    for e in expr[1:]:
        result = lisp_eval(e, env)
        if not is_truthy(result):
            return FALSE
    return result


def eval_or(expr: LispList, env: Environment) -> LispValue:
    """(or expr...) - short-circuit or."""
    for e in expr[1:]:
        result = lisp_eval(e, env)
        if is_truthy(result):
            return result
    return FALSE


def eval_let(expr: LispList, env: Environment) -> LispValue:
    """
    (let ((a 1) (b 2)) body...) - local bindings
    Rewritten to ((lambda (a b) body...) 1 2)
    """
    if len(expr) < 3:
        raise EvalError("let requires bindings and body")
    
    bindings = expr[1]
    if not isinstance(bindings, LispList):
        raise EvalError("let bindings must be a list")
    
    params = []
    args = []
    
    for binding in bindings:
        if not isinstance(binding, LispList) or len(binding) != 2:
            raise EvalError("let binding must be (name value)")
        name, value_expr = binding[0], binding[1]
        if not isinstance(name, LispSymbol):
            raise EvalError("let binding name must be a symbol")
        params.append(name.name)
        args.append(lisp_eval(value_expr, env))
    
    # Create new environment with bindings
    new_env = env.extend(params, args)
    
    # Evaluate body
    result = VOID
    for body_expr in expr[2:]:
        result = lisp_eval(body_expr, new_env)
    return result


def eval_begin(expr: LispList, env: Environment) -> LispValue:
    """(begin expr...) - evaluate expressions, return last."""
    result = VOID
    for e in expr[1:]:
        result = lisp_eval(e, env)
    return result


def eval_set(expr: LispList, env: Environment) -> LispValue:
    """(set! var value) - modify existing binding."""
    if len(expr) != 3:
        raise EvalError("set! requires exactly 2 arguments")
    
    var = expr[1]
    if not isinstance(var, LispSymbol):
        raise EvalError("set! target must be a symbol")
    
    value = lisp_eval(expr[2], env)
    env.set(var.name, value)
    return VOID


def eval_application(expr: LispList, env: Environment) -> LispValue:
    """Evaluate function application."""
    # Evaluate operator
    operator = lisp_eval(expr[0], env)
    
    # Evaluate arguments
    args = [lisp_eval(arg, env) for arg in expr[1:]]
    
    if isinstance(operator, LispPrimitive):
        return operator.func(*args)
    
    if isinstance(operator, LispClosure):
        # Check arity
        if len(args) != len(operator.params):
            raise EvalError(
                f"Expected {len(operator.params)} arguments, got {len(args)}"
            )
        
        # Extend closure's environment with args
        new_env = operator.env.extend(operator.params, args)
        
        # Evaluate body
        result = VOID
        for body_expr in operator.body:
            result = lisp_eval(body_expr, new_env)
        return result
    
    raise EvalError(f"Cannot apply: {operator}")
