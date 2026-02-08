"""
SimpleLisp Parser
Parses tokens into Lisp AST for the Simply Scheme interpreter.
"""
from typing import List, Optional
from lexer import Token, TokenType, tokenize, LexerError
from lisp_types import (
    LispValue, LispNumber, LispSymbol, LispString, LispBool,
    LispList, TRUE, FALSE, NIL
)


class ParseError(Exception):
    def __init__(self, message: str, token: Optional[Token] = None):
        self.token = token
        if token:
            super().__init__(f"Parse error at {token.line}:{token.column}: {message}")
        else:
            super().__init__(f"Parse error: {message}")


class Parser:
    """Parses tokens into Lisp expressions."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> List[LispValue]:
        """Parse all expressions from tokens."""
        expressions = []
        while not self._at_end():
            expr = self._parse_expr()
            if expr is not None:
                expressions.append(expr)
        return expressions
    
    def parse_one(self) -> Optional[LispValue]:
        """Parse a single expression."""
        if self._at_end():
            return None
        return self._parse_expr()
    
    def _at_end(self) -> bool:
        return self._peek().type == TokenType.EOF
    
    def _peek(self) -> Token:
        return self.tokens[self.pos]
    
    def _advance(self) -> Token:
        token = self.tokens[self.pos]
        if token.type != TokenType.EOF:
            self.pos += 1
        return token
    
    def _check(self, type: TokenType) -> bool:
        return self._peek().type == type
    
    def _match(self, *types: TokenType) -> Optional[Token]:
        for t in types:
            if self._check(t):
                return self._advance()
        return None
    
    def _expect(self, type: TokenType, message: str) -> Token:
        if self._check(type):
            return self._advance()
        raise ParseError(message, self._peek())
    
    def _parse_expr(self) -> LispValue:
        """Parse a single expression."""
        token = self._peek()
        
        if token.type == TokenType.LPAREN:
            return self._parse_list()
        elif token.type == TokenType.QUOTE:
            return self._parse_quote()
        elif token.type == TokenType.NUMBER:
            return self._parse_number()
        elif token.type == TokenType.STRING:
            return self._parse_string()
        elif token.type == TokenType.SYMBOL:
            return self._parse_symbol()
        elif token.type == TokenType.BOOL_TRUE:
            self._advance()
            return TRUE
        elif token.type == TokenType.BOOL_FALSE:
            self._advance()
            return FALSE
        elif token.type == TokenType.RPAREN:
            raise ParseError("Unexpected ')'", token)
        else:
            raise ParseError(f"Unexpected token: {token}", token)
    
    def _parse_list(self) -> LispList:
        """Parse a list (...)."""
        self._expect(TokenType.LPAREN, "Expected '('")
        
        elements = []
        while not self._check(TokenType.RPAREN) and not self._at_end():
            elements.append(self._parse_expr())
        
        self._expect(TokenType.RPAREN, "Expected ')'")
        return LispList(elements)
    
    def _parse_quote(self) -> LispList:
        """Parse 'expr into (quote expr)."""
        self._advance()  # Consume '
        expr = self._parse_expr()
        return LispList([LispSymbol("quote"), expr])
    
    def _parse_number(self) -> LispNumber:
        """Parse a number literal."""
        token = self._advance()
        value = token.value
        if '.' in value:
            return LispNumber(float(value))
        else:
            return LispNumber(int(value))
    
    def _parse_string(self) -> LispString:
        """Parse a string literal."""
        token = self._advance()
        return LispString(token.value)
    
    def _parse_symbol(self) -> LispSymbol:
        """Parse a symbol."""
        token = self._advance()
        return LispSymbol(token.value)


def parse(source: str) -> List[LispValue]:
    """Parse source code into list of expressions."""
    tokens = tokenize(source)
    return Parser(tokens).parse()


def parse_one(source: str) -> Optional[LispValue]:
    """Parse a single expression from source."""
    tokens = tokenize(source)
    return Parser(tokens).parse_one()
