"""Main compiler for MiniScript."""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lexer import Lexer, LexicalError
from parser import Parser, ParseError
from semantic_analyzer import SemanticAnalyzer
from tac_generator import TACGenerator


class Compiler:
    """MiniScript Compiler."""
    
    def __init__(self, source: str):
        """Initialize compiler with source code.
        
        Args:
            source: Source code to compile
        """
        self.source = source
        self.tokens = None
        self.ast = None
        self.errors = []
    
    def compile(self) -> bool:
        """Compile the source code.
        
        Returns:
            True if compilation successful, False otherwise
        """
        print("\n" + "=" * 70)
        print("MINISCRIPT COMPILER - STEP-BY-STEP EXECUTION")
        print("=" * 70)
        print()
        
        # Phase 1: Lexical Analysis (Lexer)
        print("╔" + "═" * 68 + "╗")
        print("║ STEP 1: LEXICAL ANALYSIS (LEXER)                                     ║")
        print("╚" + "═" * 68 + "╝")
        print("Purpose: Convert source code into tokens")
        print()
        if not self.lexical_analysis():
            return False
        print(f"✓ Lexer: Generated {len(self.tokens)} tokens successfully")
        print()
        
        # Phase 2: Parsing
        print("╔" + "═" * 68 + "╗")
        print("║ STEP 2: SYNTAX ANALYSIS (PARSER)                                     ║")
        print("╚" + "═" * 68 + "╝")
        print("Purpose: Build Abstract Syntax Tree (AST) from tokens")
        print()
        if not self.parse():
            return False
        print("✓ Parser: Built AST successfully")
        print()
        
        # Phase 3: Semantic Analysis with Symbol Table
        print("╔" + "═" * 68 + "╗")
        print("║ STEP 3: SEMANTIC ANALYSIS (SYMBOL TABLE)                             ║")
        print("╚" + "═" * 68 + "╝")
        print("Purpose: Type checking, scope management, symbol table population")
        print()
        if not self.semantic_analysis():
            return False
        print("✓ Semantic Analyzer: Type checking and symbol table passed")
        print()
        
        # Phase 4: Intermediate Code Generation
        print("╔" + "═" * 68 + "╗")
        print("║ STEP 4: INTERMEDIATE CODE GENERATION (TAC)                           ║")
        print("╚" + "═" * 68 + "╝")
        print("Purpose: Generate Three-Address Code (TAC) for execution")
        print()
        self.generate_tac()
        print("✓ TAC Generator: Generated intermediate code successfully")
        print()
        
        print("=" * 70)
        print("✓ COMPILATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print()
        
        return True
    
    def lexical_analysis(self) -> bool:
        """Perform lexical analysis (Lexer phase)."""
        try:
            print("→ Running Lexer on input...")
            lexer = Lexer(self.source)
            self.tokens = lexer.tokenize()
            
            if lexer.has_errors():
                print("✗ Lexical Errors:")
                for error in lexer.get_errors():
                    print(f"  • {error}")
                    self.errors.append(error)
                return False
            
            # Show tokens
            print(f"\n→ Lexer Output: {len(self.tokens)} Tokens")
            print("-" * 70)
            for i, token in enumerate(self.tokens, 1):
                print(f"  {i:2d}. {token}")
            print()
            
            return True
        
        except LexicalError as e:
            print(f"✗ Lexical Error: {e}")
            self.errors.append(str(e))
            return False
    
    def parse(self) -> bool:
        """Perform parsing (Parser phase - builds AST)."""
        try:
            print("→ Running Parser...")
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            
            if parser.has_errors():
                print("✗ Parse Errors:")
                for error in parser.get_errors():
                    print(f"  • {error}")
                    self.errors.append(error)
                return False
            
            print("→ Parser Output: Abstract Syntax Tree (AST)")
            print("-" * 70)
            self._print_ast_node(self.ast, 0)
            print()
            
            return True
        
        except ParseError as e:
            print(f"✗ Parse Error: {e}")
            self.errors.append(str(e))
            return False
    
    def semantic_analysis(self) -> bool:
        """Perform semantic analysis (Symbol Table & Type Checking)."""
        try:
            print("→ Running Semantic Analyzer (Type Checking & Symbol Table)...")
            analyzer = SemanticAnalyzer()
            success = analyzer.analyze(self.ast)
            
            if analyzer.has_errors():
                print("✗ Semantic Errors:")
                for error in analyzer.get_errors():
                    print(f"  • {error}")
                    self.errors.append(error)
            
            # Show symbol table if available
            if hasattr(analyzer, 'symbol_table') and analyzer.symbol_table:
                print("\n→ Symbol Table (Populated during analysis)")
                print("-" * 70)
                self._print_symbol_table(analyzer.symbol_table)
                print()
            
            return success
        
        except Exception as e:
            print(f"✗ Semantic Analysis Error: {e}")
            self.errors.append(str(e))
            return False
    
    def generate_tac(self) -> None:
        """Generate Three-Address Code (TAC)."""
        try:
            print("→ Running TAC Generator...")
            generator = TACGenerator()
            tac_code = generator.generate(self.ast)
            
            print("\n→ TAC Generator Output: Three-Address Code (Intermediate Representation)")
            print("-" * 70)
            print("TAC Instructions:")
            print()
            for i, instruction in enumerate(tac_code):
                print(f"  {i:3d}: {instruction}")
            print()
            
        except Exception as e:
            print(f"✗ TAC Generation Error: {e}")
            self.errors.append(str(e))
    
    def print_tokens(self) -> None:
        """Print all tokens."""
        print("Tokens:")
        print("-" * 60)
        for token in self.tokens:
            print(f"  {token}")
    
    def print_ast(self) -> None:
        """Print AST structure."""
        print("Abstract Syntax Tree:")
        print("-" * 60)
        self._print_ast_node(self.ast, 0)
    
    def _print_ast_node(self, node, indent: int):
        """Recursively print AST node."""
        if node is None:
            return
        
        indent_str = "  " * indent
        node_type = type(node).__name__
        
        if node_type == "Program":
            print(f"{indent_str}Program")
            for stmt in node.statements:
                self._print_ast_node(stmt, indent + 1)
        
        elif node_type == "VarDeclaration":
            print(f"{indent_str}VarDeclaration: {node.name}")
            if node.initializer:
                self._print_ast_node(node.initializer, indent + 1)
        
        elif node_type == "Assignment":
            print(f"{indent_str}Assignment: {node.target} =")
            self._print_ast_node(node.value, indent + 1)
        
        elif node_type == "BinaryOp":
            print(f"{indent_str}BinaryOp: {node.operator}")
            print(f"{indent_str}  Left:")
            self._print_ast_node(node.left, indent + 2)
            print(f"{indent_str}  Right:")
            self._print_ast_node(node.right, indent + 2)
        
        elif node_type == "UnaryOp":
            print(f"{indent_str}UnaryOp: {node.operator}")
            self._print_ast_node(node.operand, indent + 1)
        
        elif node_type == "Identifier":
            print(f"{indent_str}Identifier: {node.name}")
        
        elif node_type == "IntLiteral":
            print(f"{indent_str}IntLiteral: {node.value}")
        
        elif node_type == "FloatLiteral":
            print(f"{indent_str}FloatLiteral: {node.value}")
        
        elif node_type == "StringLiteral":
            print(f"{indent_str}StringLiteral: {node.value}")
        
        elif node_type == "BoolLiteral":
            print(f"{indent_str}BoolLiteral: {node.value}")
        
        elif node_type == "FunctionCall":
            print(f"{indent_str}FunctionCall: {node.name}")
            for arg in node.arguments:
                self._print_ast_node(arg, indent + 1)
        
        elif node_type == "PrintStatement":
            print(f"{indent_str}PrintStatement:")
            self._print_ast_node(node.value, indent + 1)
        
        else:
            print(f"{indent_str}{node_type}")
    
    def _print_symbol_table(self, symbol_table):
        """Print symbol table contents."""
        try:
            # Try to access symbols
            if hasattr(symbol_table, 'symbols') and symbol_table.symbols:
                print("  Symbols in Current Scope:")
                for name, symbol in symbol_table.symbols.items():
                    if hasattr(symbol, 'type'):
                        type_str = symbol.type if isinstance(symbol.type, str) else str(symbol.type)
                        print(f"    • Name: {name:15} Type: {type_str}")
                    else:
                        print(f"    • {name}")
            else:
                print("  (Symbol table available but checking...)")
        except Exception as e:
            print(f"  (Symbol table info: {type(symbol_table).__name__})")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source_file>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    if not os.path.exists(source_file):
        print(f"Error: File '{source_file}' not found")
        sys.exit(1)
    
    with open(source_file, 'r') as f:
        source = f.read()
    
    compiler = Compiler(source)
    success = compiler.compile()
    
    # Always show detailed information by default
    print("\n" + "=" * 60)
    print("DETAILED RESULTS")
    print("=" * 60)
    print()
    
    compiler.print_tokens()
    print()
    compiler.print_ast()
    print()
    
    # Optional: quiet mode
    if '--quiet' in sys.argv or '-q' in sys.argv:
        pass  # Skip detailed output
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
