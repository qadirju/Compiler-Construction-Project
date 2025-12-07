"""Token types and token class for MiniScript lexer."""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    """Token types for MiniScript language."""
    
    # Literals
    ID = auto()
    INT_LIT = auto()
    FLOAT_LIT = auto()
    STRING_LIT = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Keywords
    VAR = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    STRING = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    FUNC = auto()
    RETURN = auto()
    PRINT = auto()
    INPUT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    
    # Comparison
    EQ = auto()        # ==
    NE = auto()        # !=
    LT = auto()        # <
    GT = auto()        # >
    LE = auto()        # <=
    GE = auto()        # >=
    
    # Logical
    AND = auto()       # &&
    OR = auto()        # ||
    NOT = auto()       # !
    
    # Assignment
    ASSIGN = auto()    # =
    
    # Delimiters
    LPAREN = auto()    # (
    RPAREN = auto()    # )
    LBRACE = auto()    # {
    RBRACE = auto()    # }
    SEMICOLON = auto() # ;
    COMMA = auto()     # ,
    COLON = auto()     # :
    
    # Special
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    """Represents a token in the source code."""
    
    type: TokenType
    lexeme: str
    literal: Optional[Any] = None
    line: int = 1
    column: int = 1
    
    def __repr__(self) -> str:
        if self.literal is not None:
            return f"Token({self.type.name}, '{self.lexeme}', {self.literal}, {self.line}, {self.column})"
        return f"Token({self.type.name}, '{self.lexeme}', {self.line}, {self.column})"


KEYWORDS = {
    'var': TokenType.VAR,
    'int': TokenType.INT,
    'float': TokenType.FLOAT,
    'bool': TokenType.BOOL,
    'string': TokenType.STRING,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'func': TokenType.FUNC,
    'return': TokenType.RETURN,
    'print': TokenType.PRINT,
    'input': TokenType.INPUT,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
}
