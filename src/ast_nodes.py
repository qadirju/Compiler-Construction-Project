"""Abstract Syntax Tree node definitions."""

from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    line: int = 1
    column: int = 1


@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    statements: List['Statement'] = field(default_factory=list)
    line: int = 1
    column: int = 1


@dataclass
class Statement(ASTNode):
    """Base class for all statements."""
    line: int = 1
    column: int = 1


@dataclass
class VarDeclaration(Statement):
    """Variable declaration: var x; or var x = 5;"""
    name: str = ""
    data_type: Optional[str] = None
    initializer: Optional['Expression'] = None
    line: int = 1
    column: int = 1


@dataclass
class Assignment(Statement):
    """Assignment statement: x = 5;"""
    target: str = ""
    value: Optional['Expression'] = None
    line: int = 1
    column: int = 1


@dataclass
class IfStatement(Statement):
    """If statement: if (cond) { ... } else { ... }"""
    condition: Optional['Expression'] = None
    then_body: List[Statement] = field(default_factory=list)
    else_body: Optional[List[Statement]] = None
    line: int = 1
    column: int = 1


@dataclass
class WhileStatement(Statement):
    """While loop: while (cond) { ... }"""
    condition: Optional['Expression'] = None
    body: List[Statement] = field(default_factory=list)
    line: int = 1
    column: int = 1


@dataclass
class ForStatement(Statement):
    """For loop: for (init; cond; update) { ... }"""
    init: Optional[Statement] = None
    condition: Optional['Expression'] = None
    update: Optional[Statement] = None
    body: List[Statement] = field(default_factory=list)
    line: int = 1
    column: int = 1


@dataclass
class FunctionDeclaration(Statement):
    """Function declaration: func foo(a, b) { ... }"""
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)
    line: int = 1
    column: int = 1


@dataclass
class ReturnStatement(Statement):
    """Return statement: return [expr];"""
    value: Optional['Expression'] = None
    line: int = 1
    column: int = 1


@dataclass
class PrintStatement(Statement):
    """Print statement: print expr;"""
    value: Optional['Expression'] = None
    line: int = 1
    column: int = 1


@dataclass
class Expression(ASTNode):
    """Base class for all expressions."""
    line: int = 1
    column: int = 1


@dataclass
class BinaryOp(Expression):
    """Binary operation: left op right"""
    left: Optional[Expression] = None
    operator: str = ""
    right: Optional[Expression] = None
    line: int = 1
    column: int = 1


@dataclass
class UnaryOp(Expression):
    """Unary operation: op operand"""
    operator: str = ""
    operand: Optional[Expression] = None
    line: int = 1
    column: int = 1


@dataclass
class Identifier(Expression):
    """Variable identifier."""
    name: str = ""
    line: int = 1
    column: int = 1


@dataclass
class IntLiteral(Expression):
    """Integer literal."""
    value: int = 0
    line: int = 1
    column: int = 1


@dataclass
class FloatLiteral(Expression):
    """Float literal."""
    value: float = 0.0
    line: int = 1
    column: int = 1


@dataclass
class StringLiteral(Expression):
    """String literal."""
    value: str = ""
    line: int = 1
    column: int = 1


@dataclass
class BoolLiteral(Expression):
    """Boolean literal."""
    value: bool = False
    line: int = 1
    column: int = 1


@dataclass
class FunctionCall(Expression):
    """Function call: func(arg1, arg2, ...)"""
    name: str = ""
    arguments: List[Expression] = field(default_factory=list)
    line: int = 1
    column: int = 1


@dataclass
class ArrayAccess(Expression):
    """Array access: arr[index]"""
    array: Optional[Expression] = None
    index: Optional[Expression] = None
    line: int = 1
    column: int = 1
