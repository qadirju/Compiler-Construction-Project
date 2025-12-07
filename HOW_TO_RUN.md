# 🚀 How to Run the MiniScript Compiler

## Quick Start

```powershell
cd "e:\CC Project"
python compiler.py examples/example1_arithmetic.ms
```

## What You Will See

When you run the compiler, it displays **4 steps** with complete details:

### STEP 1: LEXICAL ANALYSIS (LEXER)
- **Input**: Raw source code (your `.ms` file)
- **Process**: Tokenizes the code character by character
- **Output**: List of tokens with:
  - Token type (VAR, ID, INT_LIT, PRINT, etc.)
  - Token value
  - Line and column position
- **Example**:
  ```
  1. Token(VAR, 'var', 2, 1)
  2. Token(ID, 'x', 2, 5)
  3. Token(SEMICOLON, ';', 2, 6)
  ...
  ```

### STEP 2: SYNTAX ANALYSIS (PARSER)
- **Input**: Token stream from Lexer
- **Process**: Builds Abstract Syntax Tree (AST) following grammar rules
- **Output**: Hierarchical tree structure showing:
  - Variable declarations
  - Assignments
  - Expressions
  - Control structures (if, while, for)
  - Function calls
- **Example**:
  ```
  Program
    VarDeclaration: x
    VarDeclaration: y
    Assignment: x =
      IntLiteral: 10
    BinaryOp: +
      Left: Identifier: x
      Right: Identifier: y
  ```

### STEP 3: SEMANTIC ANALYSIS (SYMBOL TABLE)
- **Input**: AST from Parser
- **Process**: Type checking and scope management
- **Output**: 
  - Symbol table with variable names and types
  - Type compatibility validation
  - Scope resolution
- **Example**:
  ```
  Symbols in Current Scope:
    • x_0    Type: int
    • y_0    Type: int
    • z_0    Type: int
  ```

### STEP 4: INTERMEDIATE CODE GENERATION (TAC)
- **Input**: Validated AST from Semantic Analyzer
- **Process**: Generates Three-Address Code (TAC)
- **Output**: Linear sequence of instructions suitable for execution:
  - Assignments
  - Binary operations
  - Control flow (labels, jumps)
  - Built-in operations (print, input)
- **Example**:
  ```
  TAC Instructions:
    0: x = ASSIGN 10
    1: y = ASSIGN 20
    2: t1 = x + y          (temporary variable)
    3: z = ASSIGN t1
    4: PRINT z
  ```

## Examples to Try

### Basic Arithmetic
```powershell
python compiler.py examples/example1_arithmetic.ms
```

### If-Else Statement
```powershell
python compiler.py examples/example2_if_else.ms
```

### While Loop
```powershell
python compiler.py examples/example3_while_loop.ms
```

### For Loop
```powershell
python compiler.py examples/example4_for_loop.ms
```

### Functions
```powershell
python compiler.py examples/example5_function.ms
```

### Operator Precedence
```powershell
python compiler.py examples/example6_precedence.ms
```

### Boolean Operations
```powershell
python compiler.py examples/example7_boolean.ms
```

### Nested Structures
```powershell
python compiler.py examples/example8_nested.ms
```

## Options

### Run with Quiet Mode (Skip Detailed Results)
```powershell
python compiler.py examples/example1_arithmetic.ms --quiet
# or
python compiler.py examples/example1_arithmetic.ms -q
```

This shows only the 4 main phases but skips the extra detailed token/AST listing at the end.

## Create Your Own Program

1. Create a file with `.ms` extension (e.g., `myprogram.ms`):
```miniscript
var x = 5;
var y = 10;
var sum = x + y;
print sum;
```

2. Compile it:
```powershell
python compiler.py myprogram.ms
```

## What Each Phase Shows

| Phase | Input | Output | What It Shows |
|-------|-------|--------|--------------|
| **Lexer** | Source code text | Tokens | Breaking code into meaningful tokens (keywords, identifiers, operators, literals) |
| **Parser** | Token stream | AST (Abstract Syntax Tree) | Structure of the program (what statements and expressions it contains) |
| **Semantic Analyzer** | AST | Symbol Table + Validation | Variable types, scope, and whether code is semantically valid |
| **TAC Generator** | Validated AST | Three-Address Code | Intermediate representation ready for execution/interpretation |

## Understanding the Output

### Lexer Output
- Shows every token found in your source code
- Line/column info helps identify where tokens are in the source
- Useful for debugging tokenization issues

### Parser Output (AST)
- Shows the tree structure of your program
- Indentation shows nesting level
- Node types show what kind of statement/expression it is

### Semantic Analysis Output (Symbol Table)
- Lists all variables and their types
- Names like `x_0`, `y_0` indicate variable instances
- Shows successful type checking

### TAC Output
- Instructions numbered 0, 1, 2, ...
- Labels (L1, L2, etc.) for jumps
- Temporary variables (t1, t2, etc.) for intermediate results
- Final code ready for interpretation

## All 4 Phases Working Together

```
Your MiniScript Code
        ↓
    [LEXER] → Tokens
        ↓
    [PARSER] → AST
        ↓
[SEMANTIC ANALYZER] → Validated AST + Symbol Table
        ↓
  [TAC GENERATOR] → Three-Address Code
        ↓
    Ready for Execution
```

## Run All Tests

To verify everything is working:
```powershell
python tests/test_compiler.py
```

This runs 16 comprehensive tests covering all 4 phases.

---

**Now try running an example and observe all 4 compilation steps!** 🎉
