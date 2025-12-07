# MiniScript Compiler - User Guide

## Quick Start

### Installation

1. Ensure Python 3.7+ is installed
2. Navigate to the project directory
3. No external dependencies required!

### Running the Compiler

```bash
# Basic usage
python compiler.py <source_file>

# Example
python compiler.py examples/example1_arithmetic.ms

# Verbose mode (shows tokens and AST)
python compiler.py examples/example2_if_else.ms -v
```

---

## Language Syntax

### Variables

```miniscript
// Declaration
var x;

// Declaration with initialization
var y = 10;

// Multiple declarations
var a = 5;
var b = 20;
var c = a + b;
```

### Data Types

```miniscript
var int_val = 42;           // Integer
var float_val = 3.14;       // Float
var bool_val = true;        // Boolean
var str_val = "hello";      // String
```

### Operators

**Arithmetic:**
```miniscript
var sum = 10 + 5;          // 15
var diff = 10 - 3;         // 7
var prod = 4 * 5;          // 20
var quot = 20 / 4;         // 5
var rem = 17 % 5;          // 2
```

**Logical:**
```miniscript
var result = true && false;  // false
var result = true || false;  // true
var result = !true;          // false
```

**Relational:**
```miniscript
var a = 5;
var b = 10;

if (a < b) { print "less"; }
if (a > b) { print "greater"; }
if (a == b) { print "equal"; }
if (a != b) { print "not equal"; }
if (a <= b) { print "less or equal"; }
if (a >= b) { print "greater or equal"; }
```

### Control Flow

**If-Else:**
```miniscript
var x = 15;

if (x > 10) {
    print "x is greater than 10";
} else {
    print "x is not greater than 10";
}
```

**While Loop:**
```miniscript
var i = 0;
while (i < 10) {
    print i;
    i = i + 1;
}
```

**For Loop:**
```miniscript
var sum = 0;
for (i = 1; i <= 10; i = i + 1) {
    sum = sum + i;
}
print sum;  // Output: 55
```

### Functions

**Declaration:**
```miniscript
func add(a, b) {
    return a + b;
}

func greet(name) {
    print "Hello, ";
    print name;
}
```

**Function Call:**
```miniscript
var result = add(3, 4);
greet("World");
```

### Comments

```miniscript
// Single-line comment
var x = 10;  // This is also a comment
```

---

## Examples

### Example 1: Calculate Sum (1 to 100)

```miniscript
var sum = 0;
var i = 1;

while (i <= 100) {
    sum = sum + i;
    i = i + 1;
}

print sum;  // Output: 5050
```

### Example 2: Check Even/Odd

```miniscript
var num = 7;

if (num % 2 == 0) {
    print "Even";
} else {
    print "Odd";
}
```

### Example 3: Fibonacci Series

```miniscript
var a = 0;
var b = 1;
var n = 10;
var i = 0;

while (i < n) {
    print a;
    var temp = a + b;
    a = b;
    b = temp;
    i = i + 1;
}
```

### Example 4: Prime Number Check

```miniscript
var num = 17;
var is_prime = true;
var i = 2;

while (i * i <= num) {
    if (num % i == 0) {
        is_prime = false;
    }
    i = i + 1;
}

if (is_prime) {
    print "Prime";
} else {
    print "Not Prime";
}
```

### Example 5: Function to Calculate Power

```miniscript
func power(base, exp) {
    var result = 1;
    var i = 0;
    
    while (i < exp) {
        result = result * base;
        i = i + 1;
    }
    
    return result;
}

var ans = power(2, 8);
print ans;  // Output: 256
```

---

## Error Messages

### Lexical Errors

```
Unterminated string at line 5
Unexpected character '$' at line 3, column 10
```

### Parse Errors

```
Expected SEMICOLON, got ID at line 10
Expected RPAREN, got RBRACE at line 15
```

### Semantic Errors

```
Line 7, Column 2: Undeclared variable 'x'
Line 3, Column 1: Variable 'count' already declared
Line 9, Column 5: If condition must be bool, got int
```

---

## Compiler Output

Each compilation produces:

1. **Phase 1: Lexical Analysis** - Token stream analysis
2. **Phase 2: Syntax Analysis** - Parse tree verification
3. **Phase 3: Semantic Analysis** - Type and scope checking
4. **Phase 4: Intermediate Code** - Three-address code (TAC)

---

## Tips and Best Practices

1. **Always declare variables before use:**
   ```miniscript
   var x;  // Declare first
   x = 10; // Then use
   ```

2. **Use braces for clarity:**
   ```miniscript
   // Good
   if (condition) {
       statement1;
       statement2;
   }
   
   // Also valid but less clear
   if (condition) statement;
   ```

3. **Initialize loop counters:**
   ```miniscript
   var i = 0;  // Always initialize
   while (i < 10) {
       // ...
       i = i + 1;
   }
   ```

4. **Be careful with operator precedence:**
   ```miniscript
   // Multiplication before addition
   var x = 2 + 3 * 4;  // 14, not 20
   
   // Use parentheses for clarity
   var y = (2 + 3) * 4;  // 20
   ```

---

## Frequently Asked Questions

**Q: Can I declare variables in for loop?**  
A: Not in the initialization; declare outside and initialize in the init section.

**Q: Are there arrays?**  
A: No, this language doesn't support arrays.

**Q: Can functions be nested?**  
A: No, all functions are at module level.

**Q: What's the maximum recursion depth?**  
A: Limited by Python's stack; typically 1000 levels.

**Q: Can I run compiled code?**  
A: This compiler generates TAC; execution requires a separate runtime.

---

**Happy Coding! 🚀**
