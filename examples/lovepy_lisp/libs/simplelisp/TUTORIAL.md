# SimpleLisp Tutorial: A Complete Guide to Lisp Programming

Welcome to SimpleLisp! This tutorial will teach you everything you need to write real programs in Lisp. By the end, you'll understand the core concepts and be able to build your own projects.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Basic Data Types](#2-basic-data-types)
3. [Arithmetic and Math](#3-arithmetic-and-math)
4. [Words and Text](#4-words-and-text)
5. [Sentences and Lists](#5-sentences-and-lists)
6. [Variables with Define](#6-variables-with-define)
7. [Functions](#7-functions)
8. [Conditionals](#8-conditionals)
9. [Recursion](#9-recursion)
10. [Higher-Order Functions](#10-higher-order-functions)
11. [Lambda Expressions](#11-lambda-expressions)
12. [Local Variables with Let](#12-local-variables-with-let)
13. [Input and Output](#13-input-and-output)
14. [Vectors (Arrays)](#14-vectors-arrays)
15. [Loading Libraries](#15-loading-libraries)
16. [Command-Line Programs](#16-command-line-programs)
17. [Complete Examples](#17-complete-examples)
18. [Quick Reference](#18-quick-reference)

---

## 1. Getting Started

### Starting the Interpreter

Open your terminal and run:

```bash
python main.py
```

You'll see a prompt where you can type expressions:

```
SimpleLisp - Simply Scheme Interpreter
Type (exit) to quit, (help) for help

>
```

### Your First Expression

Type an expression and press Enter:

```scheme
> (+ 2 3)
5
```

**Key concept:** In Lisp, every expression is wrapped in parentheses, with the operator first. This is called **prefix notation**.

### Running a File

Save your code to a `.scm` file and run it:

```bash
python main.py myprogram.scm
```

### Exiting

Type `quit`, `exit`, or press Ctrl+D.

---

## 2. Basic Data Types

SimpleLisp has several data types:

### Numbers

```scheme
> 42          ; Integer
42
> 3.14        ; Float
3.14
> -17         ; Negative
-17
```

### Booleans

```scheme
> #t          ; True
#t
> #f          ; False
#f
```

### Strings

```scheme
> "Hello, World!"
"Hello, World!"
> "Line 1\nLine 2"   ; \n is newline
"Line 1
Line 2"
```

### Symbols

Symbols are like names. Use a quote `'` to create one:

```scheme
> 'hello
hello
> 'my-variable
my-variable
```

### Lists

Lists hold multiple values:

```scheme
> '(1 2 3)
(1 2 3)
> '(apple banana cherry)
(apple banana cherry)
> '()         ; Empty list
()
```

**The Quote `'`:** Without a quote, Lisp tries to evaluate. With a quote, it takes the value literally.

```scheme
> (+ 1 2)     ; Evaluates to 3
3
> '(+ 1 2)    ; Just the list (+ 1 2)
(+ 1 2)
```

---

## 3. Arithmetic and Math

### Basic Operations

```scheme
> (+ 1 2 3 4)       ; Addition (variadic)
10
> (- 10 3)          ; Subtraction
7
> (- 5)             ; Negation
-5
> (* 2 3 4)         ; Multiplication
24
> (/ 20 4)          ; Division
5
> (/ 10 3)          ; Returns float
3.3333333333333335
```

### Integer Operations

```scheme
> (quotient 10 3)   ; Integer division
3
> (remainder 10 3)  ; Modulo
1
```

### Other Math Functions

```scheme
> (abs -5)          ; Absolute value
5
> (sqrt 16)         ; Square root
4
> (max 3 7 2 9 1)   ; Maximum
9
> (min 3 7 2 9 1)   ; Minimum
1
> (random 100)      ; Random 0-99
42
```

### Comparisons

All return `#t` or `#f`:

```scheme
> (= 5 5)           ; Equal
#t
> (< 3 5)           ; Less than
#t
> (> 3 5)           ; Greater than
#f
> (<= 5 5)          ; Less or equal
#t
> (>= 5 5)          ; Greater or equal
#t
```

### Nested Expressions

Combine expressions by nesting:

```scheme
> (* 2 (+ 3 4))
14
> (+ (* 2 3) (* 4 5))
26
> (sqrt (+ (* 3 3) (* 4 4)))   ; Pythagorean: sqrt(9+16) = 5
5
```

---

## 4. Words and Text

In SimpleLisp, **words** include symbols, strings, and numbers. This makes text manipulation easy.

### Creating Words

```scheme
> 'hello
hello
> "hello"
"hello"
```

### Combining Words

```scheme
> (word 'super 'hero)
superhero
> (word 'pine 'apple)
pineapple
> (word "Hello" " " "World")
Hello World
> (word 'item 1)
item1
```

### Taking Apart Words

**`first`** - Get the first character:
```scheme
> (first 'hello)
h
> (first "goodbye")
g
```

**`butfirst` (or `bf`)** - Everything except the first:
```scheme
> (butfirst 'hello)
ello
> (bf 'hello)
ello
```

**`last`** - Get the last character:
```scheme
> (last 'hello)
o
```

**`butlast` (or `bl`)** - Everything except the last:
```scheme
> (butlast 'hello)
hell
> (bl 'hello)
hell
```

### Accessing by Position

**`item`** - Get the nth character (1-indexed):
```scheme
> (item 1 'hello)   ; First
h
> (item 3 'hello)   ; Third
l
```

### Word Properties

```scheme
> (count 'hello)    ; Length
5
> (empty? "")       ; Is empty?
#t
> (empty? 'hello)
#f
```

---

## 5. Sentences and Lists

A **sentence** is a list of words. SimpleLisp provides special functions for working with sentences.

### Creating Sentences

```scheme
> '(the quick brown fox)
(the quick brown fox)
> (sentence 'hello 'world)
(hello world)
> (se 'I 'love 'Lisp)          ; se is short for sentence
(I love Lisp)
```

### Sentence Flattens Lists

```scheme
> (sentence 'hello '(my friend))
(hello my friend)
> (se '(1 2) '(3 4))
(1 2 3 4)
```

### Taking Apart Sentences

**`first`** and **`butfirst`** work on sentences too:

```scheme
> (first '(apple banana cherry))
apple
> (butfirst '(apple banana cherry))
(banana cherry)
> (last '(apple banana cherry))
cherry
> (butlast '(apple banana cherry))
(apple banana)
```

### Accessing by Position

```scheme
> (item 2 '(apple banana cherry))
banana
```

### List Properties

```scheme
> (count '(a b c d e))
5
> (empty? '())
#t
> (empty? '(1 2 3))
#f
```

### Traditional List Operations

```scheme
> (cons 'a '(b c))              ; Add to front
(a b c)
> (car '(a b c))                ; First element (same as first)
a
> (cdr '(a b c))                ; Rest (same as butfirst)
(b c)
> (list 'a 'b 'c)               ; Create a list
(a b c)
> (append '(a b) '(c d))        ; Join lists
(a b c d)
> (reverse '(1 2 3))            ; Reverse
(3 2 1)
> (length '(a b c d))           ; Length (same as count)
4
> (null? '())                   ; Is empty list?
#t
> (list? '(1 2 3))              ; Is it a list?
#t
```

---

## 6. Variables with Define

Use `define` to create variables:

```scheme
> (define pi 3.14159)
> pi
3.14159

> (define greeting "Hello, World!")
> greeting
"Hello, World!"

> (define my-list '(1 2 3 4 5))
> my-list
(1 2 3 4 5)
```

### Updating Variables

Use `set!` to change a variable's value:

```scheme
> (define counter 0)
> counter
0
> (set! counter (+ counter 1))
> counter
1
```

---

## 7. Functions

### Defining Functions

```scheme
(define (function-name parameters) body)
```

**Example - Square a number:**
```scheme
> (define (square x)
    (* x x))
> (square 5)
25
> (square 12)
144
```

**Example - Multiple parameters:**
```scheme
> (define (add a b)
    (+ a b))
> (add 3 4)
7
```

**Example - Greeting function:**
```scheme
> (define (greet name)
    (se 'Hello name))
> (greet 'Alice)
(Hello Alice)
```

### Functions with Multiple Expressions

The last expression is returned:

```scheme
> (define (greet-and-welcome name)
    (display "Processing...")
    (newline)
    (se 'Welcome name))
> (greet-and-welcome 'Bob)
Processing...
(Welcome Bob)
```

### Using `begin` for Multiple Expressions

```scheme
> (begin
    (display "Step 1")
    (newline)
    (display "Step 2")
    (newline)
    (+ 1 2))
Step 1
Step 2
3
```

---

## 8. Conditionals

### The `if` Expression

```scheme
(if condition then-expression else-expression)
```

```scheme
> (if (> 5 3) 'yes 'no)
yes
> (if (< 5 3) 'yes 'no)
no
```

**Example - Absolute value:**
```scheme
> (define (my-abs x)
    (if (< x 0)
        (- x)
        x))
> (my-abs -7)
7
> (my-abs 10)
10
```

### The `cond` Expression

For multiple conditions:

```scheme
(cond
  ((condition1) result1)
  ((condition2) result2)
  (else default-result))
```

**Example - Letter grade:**
```scheme
> (define (grade score)
    (cond
      ((>= score 90) 'A)
      ((>= score 80) 'B)
      ((>= score 70) 'C)
      ((>= score 60) 'D)
      (else 'F)))
> (grade 95)
A
> (grade 72)
C
> (grade 55)
F
```

### Logical Operators

**`and`** - Returns `#f` if any argument is false, otherwise the last value:
```scheme
> (and #t #t)
#t
> (and #t #f)
#f
> (and (> 5 3) (< 10 20))
#t
```

**`or`** - Returns the first true value, or `#f`:
```scheme
> (or #f #f)
#f
> (or #f #t)
#t
> (or 'hello #f)
hello
```

**`not`** - Negates:
```scheme
> (not #t)
#f
> (not #f)
#t
```

### Type Predicates

```scheme
> (number? 42)
#t
> (number? 'hello)
#f
> (symbol? 'hello)
#t
> (string? "hello")
#t
> (list? '(1 2 3))
#t
> (boolean? #t)
#t
> (procedure? +)
#t
> (word? 'hello)      ; True for symbol, string, or number
#t
> (even? 4)
#t
> (odd? 5)
#t
> (integer? 5)
#t
> (integer? 5.5)
#f
```

---

## 9. Recursion

Functions can call themselves. This is how we process lists and repeat actions.

### Simple Countdown

```scheme
> (define (countdown n)
    (if (= n 0)
        'blastoff
        (se n (countdown (- n 1)))))
> (countdown 5)
(5 4 3 2 1 blastoff)
```

### Factorial

```scheme
> (define (factorial n)
    (if (= n 0)
        1
        (* n (factorial (- n 1)))))
> (factorial 5)
120
> (factorial 10)
3628800
```

### Fibonacci

```scheme
> (define (fib n)
    (cond
      ((= n 0) 0)
      ((= n 1) 1)
      (else (+ (fib (- n 1)) (fib (- n 2))))))
> (fib 10)
55
```

### Sum of a List

```scheme
> (define (sum-list lst)
    (if (null? lst)
        0
        (+ (car lst) (sum-list (cdr lst)))))
> (sum-list '(1 2 3 4 5))
15
```

### Reverse a Word

```scheme
> (define (reverse-word w)
    (if (empty? (butfirst w))
        w
        (word (last w) (reverse-word (butlast w)))))
> (reverse-word 'hello)
olleh
```

---

## 10. Higher-Order Functions

Higher-order functions take other functions as arguments.

### `every` - Apply to Each Element

```scheme
> (define (square x) (* x x))
> (every square '(1 2 3 4 5))
(1 4 9 16 25)

> (every first '(apple banana cherry))
(a b c)

> (every butfirst '(hello world lisp))
(ello orld isp)
```

### `keep` - Filter Elements

```scheme
> (keep even? '(1 2 3 4 5 6 7 8))
(2 4 6 8)

> (keep odd? '(1 2 3 4 5 6 7 8))
(1 3 5 7)

> (define (long-word? w) (> (count w) 4))
> (keep long-word? '(I love programming in Lisp))
(programming)
```

### `accumulate` - Combine All Elements

```scheme
> (accumulate + '(1 2 3 4 5))
15

> (accumulate * '(1 2 3 4 5))
120

> (accumulate word '(un believ able))
unbelievable

> (accumulate max '(3 7 2 9 4))
9
```

### Using with `map`, `filter`, `reduce`

These standard functions are also available:

```scheme
> (map square '(1 2 3 4))
(1 4 9 16)

> (filter even? '(1 2 3 4 5 6))
(2 4 6)

> (reduce + 0 '(1 2 3 4 5))
15
```

---

## 11. Lambda Expressions

**Lambda** creates an anonymous (unnamed) function.

```scheme
(lambda (parameters) body)
```

### Basic Usage

```scheme
> ((lambda (x) (* x x)) 5)
25

> ((lambda (a b) (+ a b)) 3 4)
7
```

### With Higher-Order Functions

```scheme
> (every (lambda (x) (* x 2)) '(1 2 3 4))
(2 4 6 8)

> (keep (lambda (x) (> x 3)) '(1 5 2 7 3 8))
(5 7 8)

> (accumulate (lambda (a b) (+ a b)) '(1 2 3))
6
```

### Assigning Lambdas

```scheme
> (define double (lambda (x) (* x 2)))
> (double 5)
10

; This is equivalent to:
> (define (double x) (* x 2))
```

---

## 12. Local Variables with Let

**`let`** creates temporary variable bindings.

```scheme
(let ((var1 value1)
      (var2 value2))
  body)
```

### Basic Usage

```scheme
> (let ((x 10)
        (y 20))
    (+ x y))
30

> (let ((a 5))
    (* a a))
25
```

### Useful for Complex Calculations

```scheme
> (define (distance x1 y1 x2 y2)
    (let ((dx (- x2 x1))
          (dy (- y2 y1)))
      (sqrt (+ (* dx dx) (* dy dy)))))
> (distance 0 0 3 4)
5
```

### Avoiding Repeated Computation

```scheme
> (define (quadratic a b c x)
    (let ((x2 (* x x)))
      (+ (* a x2) (* b x) c)))
> (quadratic 1 2 3 5)    ; 1*25 + 2*5 + 3 = 38
38
```

---

## 13. Input and Output

### Printing

**`display`** - Print without newline:
```scheme
> (display "Hello")
Hello
> (display 42)
42
```

**`show`** - Print with newline:
```scheme
> (show "Hello")
Hello
> (show '(1 2 3))
(1 2 3)
```

**`newline`** - Print a blank line:
```scheme
> (newline)

```

### Interactive Example

```scheme
> (display "Enter a number: ")
> (define n (read))
5
> (show (* n n))
25
```

### Reading Input

**`read`** - Read a Lisp expression:
```scheme
> (read)
(+ 1 2)      ; User types this
(+ 1 2)      ; Returns as data
```

**`read-line`** - Read a line as string:
```scheme
> (read-line)
Hello World  ; User types this
"Hello World"
```

---

## 14. Vectors (Arrays)

Vectors are mutable, fixed-size arrays with O(1) access.

### Creating Vectors

```scheme
> (define v (make-vector 5))       ; 5 elements, default 0
> v
#(0 0 0 0 0)

> (define v2 (make-vector 3 'x))   ; 3 elements, filled with 'x
> v2
#(x x x)
```

### Accessing Elements

```scheme
> (vector-ref v 0)     ; Get element at index 0
0
> (vector-ref v2 2)    ; Get element at index 2
x
```

### Modifying Elements

```scheme
> (vector-set! v 0 100)
> (vector-set! v 1 200)
> v
#(100 200 0 0 0)
```

### Vector Length

```scheme
> (vector-length v)
5
```

### Example: Counting

```scheme
> (define counts (make-vector 10 0))
> (vector-set! counts 5 (+ 1 (vector-ref counts 5)))
> (vector-ref counts 5)
1
```

---

## 15. Loading Libraries

### Creating a Library

Save reusable functions in a `.scm` file:

**mathlib.scm:**
```scheme
; Math library

(define (square x) (* x x))

(define (cube x) (* x x x))

(define (average a b) (/ (+ a b) 2))

(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))
```

### Loading a Library

```scheme
> (load "mathlib.scm")
> (square 5)
25
> (factorial 6)
720
```

### In a Script

**main.scm:**
```scheme
(load "mathlib.scm")

(show (square 10))
(show (cube 3))
(show (average 10 20))
```

Run:
```bash
python main.py main.scm
```

---

## 16. Command-Line Programs

### Command-Line Arguments

When running a script, arguments are available in `*command-line-args*`:

**greet.scm:**
```scheme
; Greet each person on command line
(define (greet-all names)
  (if (null? names)
      'done
      (begin
        (display "Hello, ")
        (display (first names))
        (display "!")
        (newline)
        (greet-all (butfirst names)))))

(greet-all *command-line-args*)
```

Run:
```bash
python main.py greet.scm Alice Bob Charlie
```

Output:
```
Hello, Alice!
Hello, Bob!
Hello, Charlie!
```

### Complete Example: Calculator

**calc.scm:**
```scheme
; Simple calculator
; Usage: python main.py calc.scm 5 + 3

(define args *command-line-args*)

(define a (first args))
(define op (item 2 args))
(define b (item 3 args))

; Convert string numbers
(define (parse-num s)
  (if (string? s)
      ; Simple hack: evaluate as expression
      (first (sentence s))
      s))

(define x (parse-num a))
(define y (parse-num b))

(define result
  (cond
    ((equal? op "+") (+ x y))
    ((equal? op "-") (- x y))
    ((equal? op "*") (* x y))
    ((equal? op "/") (/ x y))
    (else 'unknown-operator)))

(show result)
```

---

## 17. Complete Examples

### Example 1: FizzBuzz

```scheme
(define (fizzbuzz n)
  (define (fb i)
    (cond
      ((> i n) 'done)
      (else
        (cond
          ((= (remainder i 15) 0) (show 'FizzBuzz))
          ((= (remainder i 3) 0) (show 'Fizz))
          ((= (remainder i 5) 0) (show 'Buzz))
          (else (show i)))
        (fb (+ i 1)))))
  (fb 1))

(fizzbuzz 20)
```

### Example 2: Pig Latin

```scheme
(define (pig-latin word)
  (word (butfirst word) (first word) 'ay))

(every pig-latin '(hello world lisp is fun))
; => (ellohay orldway isplay isay unfay)
```

### Example 3: Number Guessing Game

```scheme
(define secret (+ 1 (random 100)))

(define (guess-game)
  (display "Guess a number (1-100): ")
  (let ((guess (read)))
    (cond
      ((= guess secret)
       (show "Correct! You win!"))
      ((< guess secret)
       (show "Too low!")
       (guess-game))
      (else
       (show "Too high!")
       (guess-game)))))

(guess-game)
```

### Example 4: List Stats

```scheme
(define (list-stats lst)
  (let ((n (length lst))
        (total (accumulate + lst))
        (smallest (accumulate min lst))
        (largest (accumulate max lst)))
    (display "Count: ") (show n)
    (display "Sum: ") (show total)
    (display "Average: ") (show (/ total n))
    (display "Min: ") (show smallest)
    (display "Max: ") (show largest)))

(list-stats '(10 25 3 47 8 19 33))
```

### Example 5: Simple Database

```scheme
; A person is (name age city)
(define people '(
  (Alice 30 NYC)
  (Bob 25 LA)
  (Charlie 35 Chicago)
  (Diana 28 NYC)))

(define (get-name person) (first person))
(define (get-age person) (item 2 person))
(define (get-city person) (item 3 person))

; Find people in a city
(define (in-city city people)
  (keep (lambda (p) (equal? (get-city p) city)) people))

; Find adults (age >= 30)
(define (adults people)
  (keep (lambda (p) (>= (get-age p) 30)) people))

(show "People in NYC:")
(show (every get-name (in-city 'NYC people)))

(show "Adults:")
(show (every get-name (adults people)))
```

---

## 18. Quick Reference

### Math
| Function | Example | Result |
|----------|---------|--------|
| `+` | `(+ 1 2 3)` | `6` |
| `-` | `(- 10 3)` | `7` |
| `*` | `(* 2 3 4)` | `24` |
| `/` | `(/ 10 4)` | `2.5` |
| `quotient` | `(quotient 10 3)` | `3` |
| `remainder` | `(remainder 10 3)` | `1` |
| `abs` | `(abs -5)` | `5` |
| `sqrt` | `(sqrt 16)` | `4` |
| `max` | `(max 3 7 2)` | `7` |
| `min` | `(min 3 7 2)` | `2` |
| `random` | `(random 10)` | `0-9` |

### Comparison
| Function | Example | Result |
|----------|---------|--------|
| `=` | `(= 5 5)` | `#t` |
| `<` | `(< 3 5)` | `#t` |
| `>` | `(> 3 5)` | `#f` |
| `<=` | `(<= 5 5)` | `#t` |
| `>=` | `(>= 5 5)` | `#t` |
| `equal?` | `(equal? '(1 2) '(1 2))` | `#t` |

### Words
| Function | Example | Result |
|----------|---------|--------|
| `word` | `(word 'a 'b)` | `ab` |
| `first` | `(first 'hello)` | `h` |
| `butfirst`/`bf` | `(bf 'hello)` | `ello` |
| `last` | `(last 'hello)` | `o` |
| `butlast`/`bl` | `(bl 'hello)` | `hell` |
| `count` | `(count 'hello)` | `5` |
| `item` | `(item 2 'hello)` | `e` |
| `empty?` | `(empty? "")` | `#t` |

### Sentences/Lists
| Function | Example | Result |
|----------|---------|--------|
| `sentence`/`se` | `(se 'a 'b)` | `(a b)` |
| `cons` | `(cons 'a '(b c))` | `(a b c)` |
| `car` | `(car '(a b c))` | `a` |
| `cdr` | `(cdr '(a b c))` | `(b c)` |
| `list` | `(list 1 2 3)` | `(1 2 3)` |
| `append` | `(append '(a) '(b))` | `(a b)` |
| `reverse` | `(reverse '(1 2 3))` | `(3 2 1)` |
| `length` | `(length '(a b c))` | `3` |
| `null?` | `(null? '())` | `#t` |
| `list?` | `(list? '(1 2))` | `#t` |

### Higher-Order
| Function | Example | Result |
|----------|---------|--------|
| `every` | `(every square '(1 2 3))` | `(1 4 9)` |
| `keep` | `(keep even? '(1 2 3 4))` | `(2 4)` |
| `accumulate` | `(accumulate + '(1 2 3))` | `6` |
| `map` | `(map square '(1 2 3))` | `(1 4 9)` |
| `filter` | `(filter odd? '(1 2 3))` | `(1 3)` |

### Type Predicates
| Function | Tests For |
|----------|-----------|
| `number?` | Number |
| `symbol?` | Symbol |
| `string?` | String |
| `list?` | List |
| `boolean?` | Boolean |
| `procedure?` | Function |
| `word?` | Symbol/String/Number |
| `even?` | Even number |
| `odd?` | Odd number |
| `integer?` | Integer |

### Special Forms
```scheme
(quote expr)            ; or 'expr
(if test then else)
(cond ((t1) e1) ... (else en))
(define name value)
(define (fn args) body)
(lambda (args) body)
(let ((v1 e1) ...) body)
(begin e1 e2 ... en)
(set! var value)
(and e1 e2 ...)
(or e1 e2 ...)
(load "filename.scm")
```

### I/O
```scheme
(display expr)          ; Print
(show expr)             ; Print + newline
(newline)               ; Blank line
(read)                  ; Read expression
(read-line)             ; Read line as string
```

### Vectors
```scheme
(make-vector n)         ; Create vector
(make-vector n fill)    ; Create with fill value
(vector-ref v i)        ; Get element
(vector-set! v i val)   ; Set element
(vector-length v)       ; Get length
```

---

**Congratulations!** You now know everything you need to write real programs in SimpleLisp. Happy coding! 🎉
