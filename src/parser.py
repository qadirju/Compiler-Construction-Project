"""Recursive descent parser for MiniScript language."""

from typing import List, Optional
from token_types import Token, TokenType
from ast_nodes import *


class ParseError(Exception):
    """Raised when parser encounters a syntax error."""
    pass


class Parser:
    """Recursive descent parser for MiniScript."""
    
    def __init__(self, tokens: List[Token]):
        """Initialize parser with token list.
        
        Args:
            tokens: List of tokens from lexer
        """
        self.tokens = tokens
        self.pos = 0
        self.errors: List[str] = []
    
    def current_token(self) -> Token:
        """Get current token."""
        if self.pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF
        return self.tokens[self.pos]
    
    def peek_token(self, offset: int = 1) -> Token:
        """Peek ahead at token."""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]  # Return EOF
        return self.tokens[pos]
    
    def advance(self) -> Token:
        """Move to next token."""
        token = self.current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self.current_token().type in types
    
    def consume(self, token_type: TokenType, message: str = "") -> Token:
        """Consume token of expected type or raise error."""
        if self.current_token().type != token_type:
            error = f"Expected {token_type.name}, got {self.current_token().type.name} at line {self.current_token().line}"
            if message:
                error += f": {message}"
            self.errors.append(error)
            raise ParseError(error)
        token = self.current_token()
        self.advance()
        return token
    
    def synchronize(self):
        """Recover from parse error by advancing to next statement."""
        self.advance()
        
        while not self.match(TokenType.EOF):
            if self.current_token().type in [TokenType.VAR, TokenType.IF, TokenType.WHILE, 
                                              TokenType.FUNC, TokenType.RETURN, TokenType.PRINT]:
                return
            self.advance()
    
    def parse(self) -> Program:
        """Parse the program."""
        statements = []
        
        while not self.match(TokenType.EOF):
            try:
                stmt = self.statement()
                if stmt:
                    statements.append(stmt)
            except ParseError:
                self.synchronize()
        
        return Program(statements=statements)
    
    def statement(self) -> Optional[Statement]:
        """Parse a statement."""
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            elif self.match(TokenType.IF):
                return self.if_statement()
            elif self.match(TokenType.WHILE):
                return self.while_statement()
            elif self.match(TokenType.FOR):
                return self.for_statement()
            elif self.match(TokenType.FUNC):
                return self.function_declaration()
            elif self.match(TokenType.RETURN):
                return self.return_statement()
            elif self.match(TokenType.PRINT):
                return self.print_statement()
            elif self.match(TokenType.LBRACE):
                self.advance()
                statements = []
                while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
                    stmt = self.statement()
                    if stmt:
                        statements.append(stmt)
                self.consume(TokenType.RBRACE)
                return None  # Block is handled in context
            else:
                return self.expression_statement()
        except ParseError:
            return None
    
    def var_declaration(self) -> VarDeclaration:
        """Parse variable declaration: var x; or var x = expr;"""
        var_token = self.consume(TokenType.VAR)
        name_token = self.consume(TokenType.ID)
        name = name_token.lexeme
        
        initializer = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            initializer = self.expression()
        
        self.consume(TokenType.SEMICOLON)
        return VarDeclaration(name=name, data_type=None, initializer=initializer,
                              line=var_token.line, column=var_token.column)
    
    def if_statement(self) -> IfStatement:
        """Parse if statement: if (cond) { ... } else { ... }"""
        if_token = self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN)
        condition = self.expression()
        self.consume(TokenType.RPAREN)
        
        self.consume(TokenType.LBRACE)
        then_body = self.block()
        self.consume(TokenType.RBRACE)
        
        else_body = None
        if self.match(TokenType.ELSE):
            self.advance()
            self.consume(TokenType.LBRACE)
            else_body = self.block()
            self.consume(TokenType.RBRACE)
        
        return IfStatement(condition=condition, then_body=then_body, else_body=else_body,
                           line=if_token.line, column=if_token.column)
    
    def while_statement(self) -> WhileStatement:
        """Parse while statement: while (cond) { ... }"""
        while_token = self.consume(TokenType.WHILE)
        self.consume(TokenType.LPAREN)
        condition = self.expression()
        self.consume(TokenType.RPAREN)
        
        self.consume(TokenType.LBRACE)
        body = self.block()
        self.consume(TokenType.RBRACE)
        
        return WhileStatement(condition=condition, body=body,
                              line=while_token.line, column=while_token.column)
    
    def for_statement(self) -> ForStatement:
        """Parse for statement: for (init; cond; update) { ... }"""
        for_token = self.consume(TokenType.FOR)
        self.consume(TokenType.LPAREN)
        
        init = None
        if not self.match(TokenType.SEMICOLON):
            if self.match(TokenType.VAR):
                init = self.var_declaration()
            else:
                init = self.expression_statement()
        else:
            self.advance()
        
        condition = None
        if not self.match(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON)
        
        update = None
        if not self.match(TokenType.RPAREN):
            update = self.expression_statement()
        self.consume(TokenType.RPAREN)
        
        self.consume(TokenType.LBRACE)
        body = self.block()
        self.consume(TokenType.RBRACE)
        
        return ForStatement(init=init, condition=condition, update=update, body=body,
                            line=for_token.line, column=for_token.column)
    
    def function_declaration(self) -> FunctionDeclaration:
        """Parse function declaration: func name(params) { ... }"""
        func_token = self.consume(TokenType.FUNC)
        name_token = self.consume(TokenType.ID)
        name = name_token.lexeme
        
        self.consume(TokenType.LPAREN)
        parameters = []
        if not self.match(TokenType.RPAREN):
            parameters.append(self.consume(TokenType.ID).lexeme)
            while self.match(TokenType.COMMA):
                self.advance()
                parameters.append(self.consume(TokenType.ID).lexeme)
        self.consume(TokenType.RPAREN)
        
        self.consume(TokenType.LBRACE)
        body = self.block()
        self.consume(TokenType.RBRACE)
        
        return FunctionDeclaration(name=name, parameters=parameters, body=body,
                                   line=func_token.line, column=func_token.column)
    
    def return_statement(self) -> ReturnStatement:
        """Parse return statement: return [expr];"""
        return_token = self.consume(TokenType.RETURN)
        
        value = None
        if not self.match(TokenType.SEMICOLON):
            value = self.expression()
        
        self.consume(TokenType.SEMICOLON)
        return ReturnStatement(value=value, line=return_token.line, column=return_token.column)
    
    def print_statement(self) -> PrintStatement:
        """Parse print statement: print expr;"""
        print_token = self.consume(TokenType.PRINT)
        value = self.expression()
        self.consume(TokenType.SEMICOLON)
        
        return PrintStatement(value=value, line=print_token.line, column=print_token.column)
    
    def expression_statement(self) -> Assignment:
        """Parse expression statement (usually assignment): x = expr;"""
        expr = self.expression()
        
        if isinstance(expr, Identifier) and self.match(TokenType.ASSIGN):
            self.advance()
            value = self.expression()
            self.consume(TokenType.SEMICOLON)
            return Assignment(target=expr.name, value=value,
                            line=expr.line, column=expr.column)
        
        self.consume(TokenType.SEMICOLON)
        raise ParseError("Expected assignment or expression statement")
    
    def block(self) -> List[Statement]:
        """Parse a block of statements."""
        statements = []
        
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def expression(self) -> Expression:
        """Parse expression."""
        return self.logical_or()
    
    def logical_or(self) -> Expression:
        """Parse logical OR expression."""
        expr = self.logical_and()
        
        while self.match(TokenType.OR):
            op_token = self.advance()
            right = self.logical_and()
            expr = BinaryOp(left=expr, operator=op_token.lexeme, right=right,
                          line=op_token.line, column=op_token.column)
        
        return expr
    
    def logical_and(self) -> Expression:
        """Parse logical AND expression."""
        expr = self.equality()
        
        while self.match(TokenType.AND):
            op_token = self.advance()
            right = self.equality()
            expr = BinaryOp(left=expr, operator=op_token.lexeme, right=right,
                          line=op_token.line, column=op_token.column)
        
        return expr
    
    def equality(self) -> Expression:
        """Parse equality expression."""
        expr = self.comparison()
        
        while self.match(TokenType.EQ, TokenType.NE):
            op_token = self.advance()
            right = self.comparison()
            expr = BinaryOp(left=expr, operator=op_token.lexeme, right=right,
                          line=op_token.line, column=op_token.column)
        
        return expr
    
    def comparison(self) -> Expression:
        """Parse comparison expression."""
        expr = self.additive()
        
        while self.match(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            op_token = self.advance()
            right = self.additive()
            expr = BinaryOp(left=expr, operator=op_token.lexeme, right=right,
                          line=op_token.line, column=op_token.column)
        
        return expr
    
    def additive(self) -> Expression:
        """Parse addition/subtraction expression."""
        expr = self.multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            right = self.multiplicative()
            expr = BinaryOp(left=expr, operator=op_token.lexeme, right=right,
                          line=op_token.line, column=op_token.column)
        
        return expr
    
    def multiplicative(self) -> Expression:
        """Parse multiplication/division/modulo expression."""
        expr = self.unary()
        
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_token = self.advance()
            right = self.unary()
            expr = BinaryOp(left=expr, operator=op_token.lexeme, right=right,
                          line=op_token.line, column=op_token.column)
        
        return expr
    
    def unary(self) -> Expression:
        """Parse unary expression."""
        if self.match(TokenType.NOT, TokenType.MINUS):
            op_token = self.advance()
            expr = self.unary()
            return UnaryOp(operator=op_token.lexeme, operand=expr,
                         line=op_token.line, column=op_token.column)
        
        return self.call()
    
    def call(self) -> Expression:
        """Parse function call."""
        expr = self.primary()
        
        while self.match(TokenType.LPAREN):
            self.advance()
            arguments = []
            
            if not self.match(TokenType.RPAREN):
                arguments.append(self.expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    arguments.append(self.expression())
            
            self.consume(TokenType.RPAREN)
            
            if isinstance(expr, Identifier):
                expr = FunctionCall(name=expr.name, arguments=arguments,
                                  line=expr.line, column=expr.column)
            else:
                raise ParseError("Can only call functions by name")
        
        return expr
    
    def primary(self) -> Expression:
        """Parse primary expression."""
        if self.match(TokenType.INT_LIT):
            token = self.advance()
            return IntLiteral(value=token.literal, line=token.line, column=token.column)
        
        elif self.match(TokenType.FLOAT_LIT):
            token = self.advance()
            return FloatLiteral(value=token.literal, line=token.line, column=token.column)
        
        elif self.match(TokenType.STRING_LIT):
            token = self.advance()
            return StringLiteral(value=token.literal, line=token.line, column=token.column)
        
        elif self.match(TokenType.TRUE, TokenType.FALSE):
            token = self.advance()
            return BoolLiteral(value=token.literal, line=token.line, column=token.column)
        
        elif self.match(TokenType.ID):
            token = self.advance()
            return Identifier(name=token.lexeme, line=token.line, column=token.column)
        
        elif self.match(TokenType.LPAREN):
            self.advance()
            expr = self.expression()
            self.consume(TokenType.RPAREN)
            return expr
        
        else:
            raise ParseError(f"Unexpected token: {self.current_token().type.name}")
    
    def has_errors(self) -> bool:
        """Check if parser encountered any errors."""
        return len(self.errors) > 0
    
    def get_errors(self) -> List[str]:
        """Get all parse errors."""
        return self.errors
