"""Semantic analyzer for MiniScript."""

from typing import Optional, Dict, Tuple
from ast_nodes import *
from symbol_table import SymbolTable, TypeChecker


class SemanticError(Exception):
    """Raised when semantic analysis encounters an error."""
    pass


class SemanticAnalyzer:
    """Semantic analyzer for type checking and symbol table management."""
    
    def __init__(self):
        """Initialize semantic analyzer."""
        self.symbol_table = SymbolTable()
        self.errors: list = []
        self.type_info: Dict[int, str] = {}  # Use id() for node tracking
    
    def analyze(self, program: Program) -> bool:
        """Analyze the AST.
        
        Args:
            program: Root AST node
            
        Returns:
            True if analysis successful, False otherwise
        """
        try:
            self.visit_program(program)
            return len(self.errors) == 0
        except SemanticError as e:
            self.errors.append(str(e))
            return False
    
    def add_error(self, message: str, node: Optional[ASTNode] = None):
        """Add semantic error."""
        if node:
            msg = f"Line {node.line}, Column {node.column}: {message}"
        else:
            msg = message
        self.errors.append(msg)
    
    def visit_program(self, node: Program):
        """Visit program node."""
        for stmt in node.statements:
            self.visit_statement(stmt)
    
    def visit_statement(self, node: Statement):
        """Dispatch to appropriate visit method."""
        if isinstance(node, VarDeclaration):
            self.visit_var_declaration(node)
        elif isinstance(node, Assignment):
            self.visit_assignment(node)
        elif isinstance(node, IfStatement):
            self.visit_if_statement(node)
        elif isinstance(node, WhileStatement):
            self.visit_while_statement(node)
        elif isinstance(node, ForStatement):
            self.visit_for_statement(node)
        elif isinstance(node, FunctionDeclaration):
            self.visit_function_declaration(node)
        elif isinstance(node, ReturnStatement):
            self.visit_return_statement(node)
        elif isinstance(node, PrintStatement):
            self.visit_print_statement(node)
    
    def visit_var_declaration(self, node: VarDeclaration):
        """Visit variable declaration."""
        # Check for redeclaration
        if not self.symbol_table.declare(node.name, 'auto'):
            self.add_error(f"Variable '{node.name}' already declared", node)
            return
        
        # Check initializer if present
        if node.initializer:
            init_type = self.visit_expression(node.initializer)
            self.type_info[id(node)] = init_type
        else:
            self.type_info[id(node)] = 'auto'
    
    def visit_assignment(self, node: Assignment):
        """Visit assignment statement."""
        # Check if variable is declared
        symbol = self.symbol_table.lookup(node.target)
        if not symbol:
            self.add_error(f"Undeclared variable '{node.target}'", node)
            return
        
        # Check type compatibility
        if node.value:
            value_type = self.visit_expression(node.value)
            self.type_info[id(node)] = value_type
    
    def visit_if_statement(self, node: IfStatement):
        """Visit if statement."""
        # Check condition type
        cond_type = self.visit_expression(node.condition)
        if cond_type != 'bool':
            self.add_error(f"If condition must be bool, got {cond_type}", node)
        
        # Analyze then branch
        for stmt in node.then_body:
            self.visit_statement(stmt)
        
        # Analyze else branch
        if node.else_body:
            for stmt in node.else_body:
                self.visit_statement(stmt)
    
    def visit_while_statement(self, node: WhileStatement):
        """Visit while statement."""
        # Check condition type
        cond_type = self.visit_expression(node.condition)
        if cond_type != 'bool':
            self.add_error(f"While condition must be bool, got {cond_type}", node)
        
        # Analyze body
        for stmt in node.body:
            self.visit_statement(stmt)
    
    def visit_for_statement(self, node: ForStatement):
        """Visit for statement."""
        # Enter new scope
        self.symbol_table.enter_scope()
        
        # Analyze init
        if node.init:
            self.visit_statement(node.init)
        
        # Analyze condition
        if node.condition:
            cond_type = self.visit_expression(node.condition)
            if cond_type != 'bool':
                self.add_error(f"For condition must be bool, got {cond_type}", node)
        
        # Analyze update
        if node.update:
            self.visit_statement(node.update)
        
        # Analyze body
        for stmt in node.body:
            self.visit_statement(stmt)
        
        # Exit scope
        self.symbol_table.exit_scope()
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        """Visit function declaration."""
        # Declare function
        if not self.symbol_table.declare(node.name, 'func', is_function=True):
            self.add_error(f"Function '{node.name}' already declared", node)
            return
        
        # Enter function scope
        self.symbol_table.enter_scope()
        
        # Declare parameters
        for param in node.parameters:
            self.symbol_table.declare(param, 'auto')
        
        # Analyze body
        for stmt in node.body:
            self.visit_statement(stmt)
        
        # Exit function scope
        self.symbol_table.exit_scope()
    
    def visit_return_statement(self, node: ReturnStatement):
        """Visit return statement."""
        if node.value:
            return_type = self.visit_expression(node.value)
            self.type_info[id(node)] = return_type
    
    def visit_print_statement(self, node: PrintStatement):
        """Visit print statement."""
        if node.value:
            expr_type = self.visit_expression(node.value)
            self.type_info[id(node)] = expr_type
    
    def visit_expression(self, node: Expression) -> str:
        """Visit expression and return its type."""
        if isinstance(node, BinaryOp):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unary_op(node)
        elif isinstance(node, Identifier):
            return self.visit_identifier(node)
        elif isinstance(node, IntLiteral):
            return self.visit_int_literal(node)
        elif isinstance(node, FloatLiteral):
            return self.visit_float_literal(node)
        elif isinstance(node, StringLiteral):
            return self.visit_string_literal(node)
        elif isinstance(node, BoolLiteral):
            return self.visit_bool_literal(node)
        elif isinstance(node, FunctionCall):
            return self.visit_function_call(node)
        else:
            return 'unknown'
    
    def visit_binary_op(self, node: BinaryOp) -> str:
        """Visit binary operation."""
        left_type = self.visit_expression(node.left)
        right_type = self.visit_expression(node.right)
        
        result_type = TypeChecker.infer_binary_result_type(left_type, node.operator, right_type)
        
        if result_type is None:
            self.add_error(f"Invalid operation: {left_type} {node.operator} {right_type}", node)
            result_type = 'error'
        
        self.type_info[id(node)] = result_type
        return result_type
    
    def visit_unary_op(self, node: UnaryOp) -> str:
        """Visit unary operation."""
        operand_type = self.visit_expression(node.operand)
        
        result_type = TypeChecker.infer_type(operand_type, node.operator)
        
        if result_type is None:
            self.add_error(f"Invalid unary operation: {node.operator} {operand_type}", node)
            result_type = 'error'
        
        self.type_info[id(node)] = result_type
        return result_type
    
    def visit_identifier(self, node: Identifier) -> str:
        """Visit identifier."""
        symbol = self.symbol_table.lookup(node.name)
        
        if not symbol:
            self.add_error(f"Undeclared variable '{node.name}'", node)
            return 'error'
        
        self.type_info[id(node)] = symbol.data_type
        return symbol.data_type
    
    def visit_int_literal(self, node: IntLiteral) -> str:
        """Visit integer literal."""
        self.type_info[id(node)] = 'int'
        return 'int'
    
    def visit_float_literal(self, node: FloatLiteral) -> str:
        """Visit float literal."""
        self.type_info[id(node)] = 'float'
        return 'float'
    
    def visit_string_literal(self, node: StringLiteral) -> str:
        """Visit string literal."""
        self.type_info[id(node)] = 'string'
        return 'string'
    
    def visit_bool_literal(self, node: BoolLiteral) -> str:
        """Visit boolean literal."""
        self.type_info[id(node)] = 'bool'
        return 'bool'
    
    def visit_function_call(self, node: FunctionCall) -> str:
        """Visit function call."""
        symbol = self.symbol_table.lookup(node.name)
        
        if not symbol:
            self.add_error(f"Undeclared function '{node.name}'", node)
            return 'error'
        
        if not symbol.is_function:
            self.add_error(f"'{node.name}' is not a function", node)
            return 'error'
        
        # Visit arguments
        for arg in node.arguments:
            self.visit_expression(arg)
        
        self.type_info[id(node)] = 'auto'  # Function return type
        return 'auto'
    
    def get_errors(self) -> list:
        """Get all semantic errors."""
        return self.errors
    
    def has_errors(self) -> bool:
        """Check if there are errors."""
        return len(self.errors) > 0
