"""
SimpleLisp Lexer
Tokenizes S-expressions for the Simply Scheme interpreter.
"""
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum, auto


class TokenType(Enum):
    LPAREN = auto()    # (
    RPAREN = auto()    # )
    QUOTE = auto()     # '
    NUMBER = auto()    # 123, 3.14, -42
    STRING = auto()    # "hello"
    SYMBOL = auto()    # hello, +, define
    BOOL_TRUE = auto() # #t
    BOOL_FALSE = auto()# #f
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.line = line
        self.column = column
        super().__init__(f"Lexer error at {line}:{column}: {message}")


class Lexer:
    """Tokenizes Lisp source code into tokens."""
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source and return list of tokens."""
        while not self._at_end():
            self._skip_whitespace_and_comments()
            if self._at_end():
                break
            self._scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _at_end(self) -> bool:
        return self.pos >= len(self.source)
    
    def _peek(self) -> str:
        if self._at_end():
            return '\0'
        return self.source[self.pos]
    
    def _peek_next(self) -> str:
        if self.pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.pos + 1]
    
    def _advance(self) -> str:
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def _skip_whitespace_and_comments(self):
        """Skip whitespace and ; comments."""
        while not self._at_end():
            c = self._peek()
            if c in ' \t\n\r':
                self._advance()
            elif c == ';':
                # Skip until end of line
                while not self._at_end() and self._peek() != '\n':
                    self._advance()
            else:
                break
    
    def _scan_token(self):
        """Scan a single token."""
        start_line = self.line
        start_col = self.column
        c = self._advance()
        
        if c == '(':
            self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col))
        elif c == ')':
            self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col))
        elif c == "'":
            self.tokens.append(Token(TokenType.QUOTE, "'", start_line, start_col))
        elif c == '"':
            self._scan_string(start_line, start_col)
        elif c == '#':
            self._scan_hash(start_line, start_col)
        elif c == '-' and self._peek().isdigit():
            self._scan_number(c, start_line, start_col)
        elif c.isdigit():
            self._scan_number(c, start_line, start_col)
        elif self._is_symbol_start(c):
            self._scan_symbol(c, start_line, start_col)
        else:
            raise LexerError(f"Unexpected character: {c!r}", start_line, start_col)
    
    def _scan_string(self, start_line: int, start_col: int):
        """Scan a string literal."""
        chars = []
        while not self._at_end() and self._peek() != '"':
            c = self._advance()
            if c == '\\':
                # Handle escape sequences
                if not self._at_end():
                    escaped = self._advance()
                    if escaped == 'n':
                        chars.append('\n')
                    elif escaped == 't':
                        chars.append('\t')
                    elif escaped == '\\':
                        chars.append('\\')
                    elif escaped == '"':
                        chars.append('"')
                    else:
                        chars.append(escaped)
            else:
                chars.append(c)
        
        if self._at_end():
            raise LexerError("Unterminated string", start_line, start_col)
        
        self._advance()  # Consume closing "
        self.tokens.append(Token(TokenType.STRING, ''.join(chars), start_line, start_col))
    
    def _scan_hash(self, start_line: int, start_col: int):
        """Scan # tokens like #t, #f."""
        if self._at_end():
            raise LexerError("Unexpected end after #", start_line, start_col)
        
        c = self._advance()
        if c == 't':
            self.tokens.append(Token(TokenType.BOOL_TRUE, '#t', start_line, start_col))
        elif c == 'f':
            self.tokens.append(Token(TokenType.BOOL_FALSE, '#f', start_line, start_col))
        else:
            raise LexerError(f"Unknown # sequence: #{c}", start_line, start_col)
    
    def _scan_number(self, first: str, start_line: int, start_col: int):
        """Scan a numeric literal."""
        chars = [first]
        has_dot = False
        
        while not self._at_end():
            c = self._peek()
            if c.isdigit():
                chars.append(self._advance())
            elif c == '.' and not has_dot:
                has_dot = True
                chars.append(self._advance())
            else:
                break
        
        value = ''.join(chars)
        self.tokens.append(Token(TokenType.NUMBER, value, start_line, start_col))
    
    def _scan_symbol(self, first: str, start_line: int, start_col: int):
        """Scan a symbol."""
        chars = [first]
        
        while not self._at_end() and self._is_symbol_char(self._peek()):
            chars.append(self._advance())
        
        value = ''.join(chars)
        self.tokens.append(Token(TokenType.SYMBOL, value, start_line, start_col))
    
    def _is_symbol_start(self, c: str) -> bool:
        """Check if character can start a symbol."""
        return c.isalpha() or c in '!$%&*+-./:<=>?@^_~'
    
    def _is_symbol_char(self, c: str) -> bool:
        """Check if character can be part of a symbol."""
        return c.isalnum() or c in '!$%&*+-./:<=>?@^_~'


def tokenize(source: str) -> List[Token]:
    """Convenience function to tokenize source code."""
    return Lexer(source).tokenize()
