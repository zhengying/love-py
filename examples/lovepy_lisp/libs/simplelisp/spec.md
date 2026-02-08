Here is the specification. Ensure the code behaves exactly as described in *Simply Scheme*.

---

# 📜 Specification: The "Simply Scheme" Teaching Interpreter

**Target Audience:** 12-year-old student.
**Goal:** Run examples from the Harvey/Wright book without friction.
**Implementation Strategy:** Lexical scoping, dynamic typing, host-language primitives for the "Simply Scheme" specific functions.

---

## 1️⃣ Data Model
The interpreter must support these distinct types.

1.  **Atom (Word):**
    *   **Number:** Integer and Float.
    *   **Symbol:** Interned strings (e.g., `'hello`).
    *   **String:** `"hello world"`.
    *   *Note:* The book treats Numbers, Symbols, and Strings as "Words." Your primitives should handle them interchangeably where possible.
2.  **List:** Standard linked list (Cons cells).
3.  **Boolean:** `#t` and `#f`.
4.  **Vector (New):** Mutable, fixed-length array. Required for Ch 23.
5.  **Procedure:**
    *   **Primitive:** Code defined in Host Language (Python/JS/etc).
    *   **Closure:** User-defined `(lambda ...)` capturing environment.
6.  **Void/Undefined:** Returned by side-effect functions (like `define` or `display`).

---

## 2️⃣ Reader / Parser
Standard S-Expression parsing with specific sugars.

**Tokens:** `(`, `)`, `'`, `Symbols`, `Numbers`, `Strings`.

**Rewrites (Sugar):**
*   `'expr` $\rightarrow$ `(quote expr)`

**Handling Comments:**
*   Lines starting with `;` must be ignored (used heavily in the book for explanations).

---

## 3️⃣ Evaluation & Environment
**Scope:** Lexical.
**Structure:** Dictionary/Map of `{ symbol: value }` with a pointer to a `parent` environment.

**The "Define" Rule (Global vs Local):**
*   `define` always acts on the *Current* environment (usually Global).
*   `set!` (needed later) modifies the *nearest* environment where the variable exists.

---

## 4️⃣ Special Forms (The Compiler Core)
Implement these inside the `eval` loop.

1.  **`quote`**: Returns argument unevaluated.
2.  **`if`**: `(if test then else)`. Evaluate `test`. If truthy, eval `then`, else eval `else`.
3.  **`define`**:
    *   `(define x 10)`: Bind `x` in current env.
    *   `(define (f x) ...)`: Syntactic sugar for `(define f (lambda (x) ...))`.
4.  **`lambda`**: Returns a **Closure** storing `{parameters, body, current_env}`.
5.  **`cond`**: Evaluate clauses sequentially. Essential for Chapter 6.
6.  **`and` / `or`**: Short-circuit evaluation.
7.  **`let`**: **Critical.** Rewrite this in the parser or evaluator:
    *   `Source`: `(let ((a 1) (b 2)) (+ a b))`
    *   `Target`: `((lambda (a b) (+ a b)) 1 2)`
8.  **`begin`**: Evaluate list of expressions, return result of the last one.

---

## 5️⃣ The "Simply Scheme" Primitives (Built-ins)
*These must be implemented in the Host Language to mimic the book's specific behavior.*

### Word & Sentence Logic (Ch 5)
This is where standard Scheme differs from the book. Implement these logic rules carefully:

*   **`word`**: Concatenates arguments.
    *   `(word 'a 'b)` $\to$ `'ab`
*   **`sentence` (or `se`)**: Variadic flattening constructor.
    *   Iterate through arguments.
    *   If arg is a list $\to$ unwrap/splice it.
    *   If arg is an atom $\to$ add to result list.
    *   *Ex:* `(se 'hello '(my friend))` $\to$ `(hello my friend)`
*   **`first`**:
    *   If arg is list $\to$ return 1st element.
    *   If arg is word $\to$ return 1st letter (as a symbol).
*   **`butfirst` (or `bf`)**:
    *   If arg is list $\to$ return `cdr` (rest of list).
    *   If arg is word $\to$ return string slice [1:] (as a symbol).
    *   *Ex:* `(bf 'hello)` $\to$ `'ello`
*   **`last` / `butlast` (or `bl`)**:
    *   Symmetric logic to `first` and `bf`.
*   **`item`**:
    *   `(item n object)` returns $n$-th element (1-based index!).
*   **`empty?`**:
    *   Returns true for `()` (empty list) AND `""` (empty string).

---

## 6️⃣ Standard Primitives
Implement these standard functions.

**Math:** `+`, `-`, `*`, `/`, `quotient`, `remainder`, `=`, `<`, `>`, `<=`, `>=`.
**Logic:** `not`, `equal?` (deep comparison).
**Lists:** `cons`, `car`, `cdr`, `list`, `length`, `append`, `null?`, `list?`.
**Type Checks:** `number?`, `word?` (true for string/symbol/number), `boolean?`, `procedure?`.

---

## 7️⃣ I/O & State Primitives (For Ch 20-23)
**I/O:**
*   **`display`**: Print representation to stdout (no quotes).
*   **`show`**: (Book specific) Same as `display` but follows with a newline.
*   **`read`**: Parse one S-expression from stdin/prompt.
    *   *Note:* This must pause execution and wait for user input.

**Vectors (Arrays):**
*   **`make-vector`**: `(make-vector size [fill])`
*   **`vector-ref`**: `(vector-ref vec index)`
*   **`vector-set!`**: `(vector-set! vec index val)`

---

## 8️⃣ Higher-Order Library (Implement in Lisp)
Do not implement these in the host language. Define them in a `startup.scm` file that runs when your interpreter boots. This teaches your daughter that "Library functions are just code."

```scheme
;; The book uses 'every', not 'map'.
;; 'every' works on words AND sentences.
(define (every fn stuff)
  (if (word? stuff)
      (every fn (sentence stuff)) ;; Convert word to list
      (if (empty? stuff)
          '()
          (sentence (fn (first stuff))
                    (every fn (butfirst stuff))))))

;; 'keep' works like filter
(define (keep pred stuff)
  (cond ((empty? stuff) '())
        ((pred (first stuff)) (sentence (first stuff) (keep pred (butfirst stuff))))
        (else (keep pred (butfirst stuff)))))

(define (accumulate combiner stuff)
  (if (empty? (butfirst stuff))
      (first stuff)
      (combiner (first stuff) (accumulate combiner (butfirst stuff)))))
```

---