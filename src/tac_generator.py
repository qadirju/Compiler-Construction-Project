"""Three-Address Code (TAC) generator for MiniScript."""

from typing import List, Dict, Optional, Tuple
from ast_nodes import *


class TAC:
    """Represents a three-address code instruction."""
    
    def __init__(self, op: str, arg1: Optional[str] = None, 
                 arg2: Optional[str] = None, result: Optional[str] = None):
        """Initialize TAC instruction.
        
        Args:
            op: Operation type
            arg1: First argument
            arg2: Second argument
            result: Result variable
        """
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    
    def __repr__(self) -> str:
        if self.result:
            if self.arg2:
                return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
            else:
                return f"{self.result} = {self.op} {self.arg1}"
        else:
            if self.arg2:
                return f"{self.op} {self.arg1} {self.arg2}"
            elif self.arg1:
                return f"{self.op} {self.arg1}"
            else:
                return f"{self.op}"


class TACGenerator:
    """Generates three-address code from AST."""
    
    def __init__(self):
        """Initialize TAC generator."""
        self.tac_code: List[TAC] = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self) -> str:
        """Generate a new temporary variable."""
        self.temp_counter += 1
        return f"t{self.temp_counter}"
    
    def new_label(self) -> str:
        """Generate a new label."""
        self.label_counter += 1
        return f"L{self.label_counter}"
    
    def emit(self, op: str, arg1: Optional[str] = None, 
             arg2: Optional[str] = None, result: Optional[str] = None) -> str:
        """Emit a TAC instruction.
        
        Args:
            op: Operation
            arg1: First argument
            arg2: Second argument
            result: Result variable
            
        Returns:
            Result variable if applicable
        """
        instruction = TAC(op, arg1, arg2, result)
        self.tac_code.append(instruction)
        return result if result else ""
    
    def generate(self, program: Program) -> List[TAC]:
        """Generate TAC for program."""
        for stmt in program.statements:
            self.visit_statement(stmt)
        return self.tac_code
    
    def visit_statement(self, node: Statement):
        """Visit statement."""
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
        if node.initializer:
            expr_result = self.visit_expression(node.initializer)
            self.emit("ASSIGN", expr_result, result=node.name)
    
    def visit_assignment(self, node: Assignment):
        """Visit assignment."""
        expr_result = self.visit_expression(node.value)
        self.emit("ASSIGN", expr_result, result=node.target)
    
    def visit_if_statement(self, node: IfStatement):
        """Visit if statement."""
        cond_result = self.visit_expression(node.condition)
        
        false_label = self.new_label()
        end_label = self.new_label()
        
        self.emit("IF_FALSE", cond_result, false_label)
        
        for stmt in node.then_body:
            self.visit_statement(stmt)
        
        self.emit("GOTO", end_label)
        self.emit("LABEL", false_label)
        
        if node.else_body:
            for stmt in node.else_body:
                self.visit_statement(stmt)
        
        self.emit("LABEL", end_label)
    
    def visit_while_statement(self, node: WhileStatement):
        """Visit while statement."""
        loop_label = self.new_label()
        end_label = self.new_label()
        
        self.emit("LABEL", loop_label)
        cond_result = self.visit_expression(node.condition)
        self.emit("IF_FALSE", cond_result, end_label)
        
        for stmt in node.body:
            self.visit_statement(stmt)
        
        self.emit("GOTO", loop_label)
        self.emit("LABEL", end_label)
    
    def visit_for_statement(self, node: ForStatement):
        """Visit for statement."""
        if node.init:
            self.visit_statement(node.init)
        
        loop_label = self.new_label()
        end_label = self.new_label()
        
        self.emit("LABEL", loop_label)
        
        if node.condition:
            cond_result = self.visit_expression(node.condition)
            self.emit("IF_FALSE", cond_result, end_label)
        
        for stmt in node.body:
            self.visit_statement(stmt)
        
        if node.update:
            self.visit_statement(node.update)
        
        self.emit("GOTO", loop_label)
        self.emit("LABEL", end_label)
    
    def visit_function_declaration(self, node: FunctionDeclaration):
        """Visit function declaration."""
        self.emit("FUNCTION", node.name)
        
        for param in node.parameters:
            self.emit("PARAM", param)
        
        for stmt in node.body:
            self.visit_statement(stmt)
        
        self.emit("RETURN")
    
    def visit_return_statement(self, node: ReturnStatement):
        """Visit return statement."""
        if node.value:
            result = self.visit_expression(node.value)
            self.emit("RETURN", result)
        else:
            self.emit("RETURN")
    
    def visit_print_statement(self, node: PrintStatement):
        """Visit print statement."""
        expr_result = self.visit_expression(node.value)
        self.emit("PRINT", expr_result)
    
    def visit_expression(self, node: Expression) -> str:
        """Visit expression and return result variable."""
        if isinstance(node, BinaryOp):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unary_op(node)
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, IntLiteral):
            return str(node.value)
        elif isinstance(node, FloatLiteral):
            return str(node.value)
        elif isinstance(node, StringLiteral):
            return f'"{node.value}"'
        elif isinstance(node, BoolLiteral):
            return str(node.value).lower()
        elif isinstance(node, FunctionCall):
            return self.visit_function_call(node)
        else:
            return "unknown"
    
    def visit_binary_op(self, node: BinaryOp) -> str:
        """Visit binary operation."""
        left = self.visit_expression(node.left)
        right = self.visit_expression(node.right)
        
        result = self.new_temp()
        self.emit(node.operator, left, right, result)
        return result
    
    def visit_unary_op(self, node: UnaryOp) -> str:
        """Visit unary operation."""
        operand = self.visit_expression(node.operand)
        
        result = self.new_temp()
        self.emit(node.operator, operand, result=result)
        return result
    
    def visit_function_call(self, node: FunctionCall) -> str:
        """Visit function call."""
        result = self.new_temp()
        
        # Emit arguments
        for arg in node.arguments:
            arg_result = self.visit_expression(arg)
            self.emit("ARG", arg_result)
        
        self.emit("CALL", node.name, result=result)
        return result
    
    def get_tac_code(self) -> List[TAC]:
        """Get generated TAC code."""
        return self.tac_code
    
    def print_tac(self):
        """Print all TAC instructions."""
        for i, instruction in enumerate(self.tac_code):
            print(f"{i:3d}: {instruction}")
