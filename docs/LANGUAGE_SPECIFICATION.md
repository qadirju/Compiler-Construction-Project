# MiniScript Language Specification

## Language Overview
**MiniScript** is a simple imperative programming language designed for educational purposes. It supports:
- Variable declarations and assignments
- Arithmetic and logical operations
- Control flow statements (if-else, while loops)
- Functions (simple version)
- Comments

## Purpose
A lightweight scripting language for mathematical computations and simple algorithmic problems with basic functions and control flow.

## Keywords
```
var, int, float, bool, string
if, else, while, for, return
func, print, input
true, false
```

## Operators
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Relational**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `&&`, `||`, `!`
- **Assignment**: `=`

## Data Types
- `int` - Integer numbers
- `float` - Floating-point numbers
- `bool` - Boolean values (true/false)
- `string` - String literals

## Separators
`{`, `}`, `(`, `)`, `,`, `;`, `:`

## Sample Program
```
func add(a, b) {
    return a + b;
}

var result;
result = add(5, 3);
print result;
```

## Grammar (Informal)
```
Program -> Statement*
Statement -> VarDecl | Assignment | IfStmt | WhileStmt | FuncDecl | PrintStmt | ReturnStmt
VarDecl -> var ID [= Expr] ;
Assignment -> ID = Expr ;
IfStmt -> if (Expr) { Statement* } [else { Statement* }]
WhileStmt -> while (Expr) { Statement* }
FuncDecl -> func ID ( ParamList ) { Statement* }
PrintStmt -> print Expr ;
ReturnStmt -> return [Expr] ;
Expr -> LogicalOr
LogicalOr -> LogicalAnd (|| LogicalAnd)*
LogicalAnd -> Equality (&& Equality)*
Equality -> Comparison ((== | !=) Comparison)*
Comparison -> Additive ((< | > | <= | >=) Additive)*
Additive -> Multiplicative ((+ | -) Multiplicative)*
Multiplicative -> Unary ((* | / | %) Unary)*
Unary -> (! | -) Unary | Postfix
Postfix -> Primary (( ArgList ))?
Primary -> ID | NUMBER | STRING | BOOL | ( Expr )
```
