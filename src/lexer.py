"""Lexical analyzer for MiniScript language."""

import re
from typing import List, Optional
from token_types import Token, TokenType, KEYWORDS


class LexicalError(Exception):
    """Raised when lexical analysis encounters an error."""
    pass


class Lexer:
    """Lexical analyzer for MiniScript."""
    
    def __init__(self, source: str):
        """Initialize lexer with source code.
        
        Args:
            source: The source code to tokenize
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.errors: List[str] = []
    
    def current_char(self) -> Optional[str]:
        """Get current character without advancing."""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek ahead at character."""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Move to next character."""
        if self.pos >= len(self.source):
            return None
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char() and self.current_char() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments starting with //."""
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            if self.current_char() == '\n':
                self.advance()
    
    def read_string(self, quote_char: str) -> str:
        """Read string literal."""
        value = ''
        self.advance()  # Skip opening quote
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                next_char = self.current_char()
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == '\\':
                    value += '\\'
                elif next_char == quote_char:
                    value += quote_char
                else:
                    value += next_char
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if not self.current_char():
            raise LexicalError(f"Unterminated string at line {self.line}")
        
        self.advance()  # Skip closing quote
        return value
    
    def read_number(self) -> Token:
        """Read numeric literal (int or float)."""
        start_line = self.line
        start_col = self.column
        value = ''
        
        while self.current_char() and self.current_char().isdigit():
            value += self.current_char()
            self.advance()
        
        # Check for float
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
            value += self.current_char()
            self.advance()
            
            while self.current_char() and self.current_char().isdigit():
                value += self.current_char()
                self.advance()
            
            return Token(TokenType.FLOAT_LIT, value, float(value), start_line, start_col)
        
        return Token(TokenType.INT_LIT, value, int(value), start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read identifier or keyword."""
        start_line = self.line
        start_col = self.column
        value = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            value += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = KEYWORDS.get(value, TokenType.ID)
        
        # Handle boolean literals
        if token_type == TokenType.TRUE:
            return Token(token_type, value, True, start_line, start_col)
        elif token_type == TokenType.FALSE:
            return Token(token_type, value, False, start_line, start_col)
        
        return Token(token_type, value, None, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Tokenize the source code."""
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Skip comments
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue
            
            char = self.current_char()
            start_line = self.line
            start_col = self.column
            
            try:
                # String literals
                if char in '"\'':
                    value = self.read_string(char)
                    self.tokens.append(Token(TokenType.STRING_LIT, f'{char}{value}{char}', value, start_line, start_col))
                
                # Numbers
                elif char.isdigit():
                    self.tokens.append(self.read_number())
                
                # Identifiers and keywords
                elif char.isalpha() or char == '_':
                    self.tokens.append(self.read_identifier())
                
                # Two-character operators
                elif char == '=' and self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.EQ, '==', None, start_line, start_col))
                
                elif char == '!' and self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.NE, '!=', None, start_line, start_col))
                
                elif char == '<' and self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.LE, '<=', None, start_line, start_col))
                
                elif char == '>' and self.peek_char() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.GE, '>=', None, start_line, start_col))
                
                elif char == '&' and self.peek_char() == '&':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.AND, '&&', None, start_line, start_col))
                
                elif char == '|' and self.peek_char() == '|':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.OR, '||', None, start_line, start_col))
                
                # Single-character operators
                elif char == '+':
                    self.advance()
                    self.tokens.append(Token(TokenType.PLUS, '+', None, start_line, start_col))
                
                elif char == '-':
                    self.advance()
                    self.tokens.append(Token(TokenType.MINUS, '-', None, start_line, start_col))
                
                elif char == '*':
                    self.advance()
                    self.tokens.append(Token(TokenType.STAR, '*', None, start_line, start_col))
                
                elif char == '/':
                    self.advance()
                    self.tokens.append(Token(TokenType.SLASH, '/', None, start_line, start_col))
                
                elif char == '%':
                    self.advance()
                    self.tokens.append(Token(TokenType.PERCENT, '%', None, start_line, start_col))
                
                elif char == '<':
                    self.advance()
                    self.tokens.append(Token(TokenType.LT, '<', None, start_line, start_col))
                
                elif char == '>':
                    self.advance()
                    self.tokens.append(Token(TokenType.GT, '>', None, start_line, start_col))
                
                elif char == '!':
                    self.advance()
                    self.tokens.append(Token(TokenType.NOT, '!', None, start_line, start_col))
                
                elif char == '=':
                    self.advance()
                    self.tokens.append(Token(TokenType.ASSIGN, '=', None, start_line, start_col))
                
                elif char == '(':
                    self.advance()
                    self.tokens.append(Token(TokenType.LPAREN, '(', None, start_line, start_col))
                
                elif char == ')':
                    self.advance()
                    self.tokens.append(Token(TokenType.RPAREN, ')', None, start_line, start_col))
                
                elif char == '{':
                    self.advance()
                    self.tokens.append(Token(TokenType.LBRACE, '{', None, start_line, start_col))
                
                elif char == '}':
                    self.advance()
                    self.tokens.append(Token(TokenType.RBRACE, '}', None, start_line, start_col))
                
                elif char == ';':
                    self.advance()
                    self.tokens.append(Token(TokenType.SEMICOLON, ';', None, start_line, start_col))
                
                elif char == ',':
                    self.advance()
                    self.tokens.append(Token(TokenType.COMMA, ',', None, start_line, start_col))
                
                elif char == ':':
                    self.advance()
                    self.tokens.append(Token(TokenType.COLON, ':', None, start_line, start_col))
                
                else:
                    error = f"Unexpected character '{char}' at line {self.line}, column {self.column}"
                    self.errors.append(error)
                    self.advance()
            
            except LexicalError as e:
                self.errors.append(str(e))
                break
        
        self.tokens.append(Token(TokenType.EOF, '', None, self.line, self.column))
        return self.tokens
    
    def has_errors(self) -> bool:
        """Check if lexer encountered any errors."""
        return len(self.errors) > 0
    
    def get_errors(self) -> List[str]:
        """Get all lexical errors."""
        return self.errors
