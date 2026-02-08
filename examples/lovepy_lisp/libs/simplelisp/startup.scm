;; SimpleLisp Standard Library
;; Loaded automatically at startup

;; The book uses 'every', not 'map'.
;; 'every' works on words AND sentences.
(define (every fn stuff)
  (if (word? stuff)
      (every fn (sentence stuff))
      (if (empty? stuff)
          '()
          (sentence (fn (first stuff))
                    (every fn (butfirst stuff))))))

;; 'keep' works like filter
(define (keep pred stuff)
  (cond ((empty? stuff) '())
        ((pred (first stuff)) 
         (sentence (first stuff) (keep pred (butfirst stuff))))
        (else (keep pred (butfirst stuff)))))

;; 'accumulate' folds from right
(define (accumulate combiner stuff)
  (if (empty? (butfirst stuff))
      (first stuff)
      (combiner (first stuff) (accumulate combiner (butfirst stuff)))))

;; Helper: apply a function to each item and filter by predicate
(define (filter pred lst)
  (cond ((null? lst) '())
        ((pred (car lst)) (cons (car lst) (filter pred (cdr lst))))
        (else (filter pred (cdr lst)))))

;; Map over a list
(define (map fn lst)
  (if (null? lst)
      '()
      (cons (fn (car lst)) (map fn (cdr lst)))))

;; Reduce/fold-left
(define (reduce combiner init lst)
  (if (null? lst)
      init
      (reduce combiner (combiner init (car lst)) (cdr lst))))

;; Common predicates
(define (positive? n) (> n 0))
(define (negative? n) (< n 0))
(define (zero? n) (= n 0))

;; List utilities
(define (cadr lst) (car (cdr lst)))
(define (caddr lst) (car (cdr (cdr lst))))
(define (cadddr lst) (car (cdr (cdr (cdr lst)))))

;; nth element (0-indexed, unlike item which is 1-indexed)
(define (list-ref lst n)
  (if (= n 0)
      (car lst)
      (list-ref (cdr lst) (- n 1))))

;; Simple assert for testing
(define (assert-equal expected actual message)
  (if (equal? expected actual)
      (begin (display "PASS: ") (show message))
      (begin (display "FAIL: ") (display message)
             (display " - expected: ") (display expected)
             (display " got: ") (show actual))))
