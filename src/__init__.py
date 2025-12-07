"""MiniScript Compiler Package."""

from .token_types import Token, TokenType, KEYWORDS
from .lexer import Lexer, LexicalError
from .ast_nodes import *
from .parser import Parser, ParseError
from .symbol_table import SymbolTable, Symbol, TypeChecker
from .semantic_analyzer import SemanticAnalyzer, SemanticError
from .tac_generator import TACGenerator, TAC

__version__ = "1.0.0"
__author__ = "Compiler Construction Project"

__all__ = [
    'Token',
    'TokenType',
    'KEYWORDS',
    'Lexer',
    'LexicalError',
    'Parser',
    'ParseError',
    'SymbolTable',
    'Symbol',
    'TypeChecker',
    'SemanticAnalyzer',
    'SemanticError',
    'TACGenerator',
    'TAC',
]
