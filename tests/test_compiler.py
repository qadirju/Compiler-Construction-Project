"""Test suite for MiniScript compiler components."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from tac_generator import TACGenerator
from token_types import TokenType


def test_lexer():
    """Test lexical analyzer."""
    print("=" * 60)
    print("Testing Lexer")
    print("=" * 60)
    
    # Test 1: Simple variable declaration
    source = "var x = 10;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.VAR
    assert tokens[1].type == TokenType.ID
    assert tokens[2].type == TokenType.ASSIGN
    assert tokens[3].type == TokenType.INT_LIT
    assert tokens[3].literal == 10
    print("✓ Test 1 passed: Variable declaration tokenization")
    
    # Test 2: String literals
    source = 'print "hello";'
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.PRINT
    assert tokens[1].type == TokenType.STRING_LIT
    assert tokens[1].literal == "hello"
    print("✓ Test 2 passed: String literal tokenization")
    
    # Test 3: Operators
    source = "a + b * c == d && e"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    token_types = [t.type for t in tokens[:-1]]  # Exclude EOF
    assert TokenType.PLUS in token_types
    assert TokenType.STAR in token_types
    assert TokenType.EQ in token_types
    assert TokenType.AND in token_types
    print("✓ Test 3 passed: Operator tokenization")
    
    # Test 4: Comments
    source = "var x = 10; // This is a comment\nvar y = 20;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    var_count = sum(1 for t in tokens if t.type == TokenType.VAR)
    assert var_count == 2
    print("✓ Test 4 passed: Comment handling")
    
    print()


def test_parser():
    """Test parser."""
    print("=" * 60)
    print("Testing Parser")
    print("=" * 60)
    
    # Test 1: Variable declaration
    source = "var x = 10;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1
    print("✓ Test 1 passed: Variable declaration parsing")
    
    # Test 2: If statement
    source = "if (x > 0) { var y = 1; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1
    print("✓ Test 2 passed: If statement parsing")
    
    # Test 3: While loop
    source = "while (i < 10) { i = i + 1; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1
    print("✓ Test 3 passed: While loop parsing")
    
    # Test 4: Function declaration
    source = "func add(a, b) { return a + b; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast.statements) == 1
    print("✓ Test 4 passed: Function declaration parsing")
    
    print()


def test_semantic_analyzer():
    """Test semantic analyzer."""
    print("=" * 60)
    print("Testing Semantic Analyzer")
    print("=" * 60)
    
    # Test 1: Valid program
    source = "var x = 10; print x;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    
    assert success
    print("✓ Test 1 passed: Valid program analysis")
    
    # Test 2: Undeclared variable detection
    source = "print y;"  # y is not declared
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    
    assert not success
    assert any("Undeclared" in str(e) for e in analyzer.get_errors())
    print("✓ Test 2 passed: Undeclared variable detection")
    
    # Test 3: Type checking for if condition
    source = "if (5) { print 1; }"  # Should error: condition must be bool
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    
    assert not success
    print("✓ Test 3 passed: Type checking for control structures")
    
    print()


def test_tac_generator():
    """Test TAC generator."""
    print("=" * 60)
    print("Testing TAC Generator")
    print("=" * 60)
    
    # Test 1: Simple assignment
    source = "var x = 5;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    generator = TACGenerator()
    tac = generator.generate(ast)
    
    assert len(tac) > 0
    print("✓ Test 1 passed: Simple assignment TAC generation")
    
    # Test 2: Binary operation
    source = "var x = 5; var y = 10; var z = x + y;"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    generator = TACGenerator()
    tac = generator.generate(ast)
    
    # Should have assignments and binary operations
    assert len(tac) > 2
    print("✓ Test 2 passed: Binary operation TAC generation")
    
    # Test 3: If statement with labels
    source = "if (x > 0) { print 1; } else { print 2; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    generator = TACGenerator()
    tac = generator.generate(ast)
    
    # Should contain labels and conditional jumps
    tac_str = '\n'.join(str(t) for t in tac)
    assert 'LABEL' in tac_str or 'IF_FALSE' in tac_str or 'GOTO' in tac_str
    print("✓ Test 3 passed: If statement TAC generation")
    
    # Test 4: While loop with labels
    source = "while (i < 10) { i = i + 1; }"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    generator = TACGenerator()
    tac = generator.generate(ast)
    
    tac_str = '\n'.join(str(t) for t in tac)
    assert 'LABEL' in tac_str
    print("✓ Test 4 passed: While loop TAC generation")
    
    print()


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + " MiniScript Compiler - Test Suite ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        test_lexer()
        test_parser()
        test_semantic_analyzer()
        test_tac_generator()
        
        print("=" * 60)
        print("All Tests Passed! ✓")
        print("=" * 60)
        print()
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
