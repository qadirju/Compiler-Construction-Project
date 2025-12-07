"""Symbol table and type system for semantic analysis."""

from typing import Dict, Optional, Tuple


class Symbol:
    """Represents a symbol in the symbol table."""
    
    def __init__(self, name: str, data_type: str, scope: int, is_function: bool = False):
        """Initialize a symbol.
        
        Args:
            name: Symbol name
            data_type: Data type (int, float, bool, string)
            scope: Scope level
            is_function: Whether this is a function
        """
        self.name = name
        self.data_type = data_type
        self.scope = scope
        self.is_function = is_function
        self.is_declared = True


class SymbolTable:
    """Symbol table for managing variables and functions."""
    
    def __init__(self):
        """Initialize the symbol table."""
        self.symbols: Dict[str, Symbol] = {}
        self.scope = 0
        self.scope_stack = [0]
    
    def enter_scope(self):
        """Enter a new scope."""
        self.scope += 1
        self.scope_stack.append(self.scope)
    
    def exit_scope(self):
        """Exit current scope and remove symbols."""
        if self.scope_stack:
            current_scope = self.scope_stack.pop()
            # Remove symbols from this scope
            self.symbols = {k: v for k, v in self.symbols.items() 
                          if v.scope != current_scope}
            self.scope = self.scope_stack[-1] if self.scope_stack else 0
    
    def declare(self, name: str, data_type: str, is_function: bool = False) -> bool:
        """Declare a symbol.
        
        Args:
            name: Symbol name
            data_type: Data type
            is_function: Whether it's a function
            
        Returns:
            True if declaration successful, False if duplicate
        """
        current_scope_key = f"{name}_{self.scope}"
        
        # Check for duplicate in current scope
        for symbol_name, symbol in self.symbols.items():
            if symbol.name == name and symbol.scope == self.scope:
                return False
        
        self.symbols[current_scope_key] = Symbol(name, data_type, self.scope, is_function)
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol.
        
        Args:
            name: Symbol name
            
        Returns:
            Symbol if found, None otherwise
        """
        # Search from current scope upward
        for symbol in self.symbols.values():
            if symbol.name == name and symbol.scope <= self.scope:
                return symbol
        return None
    
    def get_all_symbols(self) -> Dict[str, Symbol]:
        """Get all symbols."""
        return self.symbols


class TypeChecker:
    """Type checking utility."""
    
    PRIMITIVE_TYPES = {'int', 'float', 'bool', 'string'}
    
    @staticmethod
    def is_valid_type(data_type: str) -> bool:
        """Check if type is valid."""
        return data_type in TypeChecker.PRIMITIVE_TYPES
    
    @staticmethod
    def are_compatible(type1: str, type2: str) -> bool:
        """Check if two types are compatible.
        
        Args:
            type1: First type
            type2: Second type
            
        Returns:
            True if compatible
        """
        if type1 == type2:
            return True
        
        # Allow implicit conversion between int and float
        if (type1 in ['int', 'float']) and (type2 in ['int', 'float']):
            return True
        
        return False
    
    @staticmethod
    def infer_type(operand_type: str, operator: str) -> Optional[str]:
        """Infer result type of unary operation.
        
        Args:
            operand_type: Type of operand
            operator: Operator symbol
            
        Returns:
            Result type
        """
        if operator == '!':
            return 'bool'
        elif operator == '-':
            return operand_type if operand_type in ['int', 'float'] else None
        return None
    
    @staticmethod
    def infer_binary_result_type(left_type: str, operator: str, right_type: str) -> Optional[str]:
        """Infer result type of binary operation.
        
        Args:
            left_type: Left operand type
            operator: Operator symbol
            right_type: Right operand type
            
        Returns:
            Result type
        """
        # Comparison operators return bool
        if operator in ['<', '>', '<=', '>=', '==', '!=']:
            return 'bool'
        
        # Logical operators return bool
        if operator in ['&&', '||']:
            return 'bool'
        
        # Handle auto types - assume numeric
        if left_type == 'auto' or right_type == 'auto':
            if operator in ['+', '-', '*', '/', '%']:
                # Infer numeric type
                if left_type in ['int', 'float']:
                    return left_type
                elif right_type in ['int', 'float']:
                    return right_type
                else:
                    return 'int'  # Default to int for auto
        
        # Arithmetic operators
        if operator in ['+', '-', '*', '/', '%']:
            if left_type == right_type and left_type in ['int', 'float']:
                return left_type
            elif left_type in ['int', 'float'] and right_type in ['int', 'float']:
                return 'float'  # Promote to float
        
        return None
