# MiniScript Compiler - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.7 or higher
- No external dependencies required!

### Installation
1. Navigate to the `CC Project` folder
2. That's it! No installation needed.

### First Compilation

```bash
# Navigate to project directory
cd "CC Project"

# Compile an example
python compiler.py examples/example1_arithmetic.ms
```

**Expected Output:**
```
============================================================
MiniScript Compiler
============================================================

Phase 1: Lexical Analysis
------------------------------------------------------------
✓ Tokenization successful (27 tokens)

Phase 2: Syntax Analysis (Parsing)
------------------------------------------------------------
✓ Parsing successful

Phase 3: Semantic Analysis
------------------------------------------------------------
✓ Semantic analysis successful

Phase 4: Intermediate Code Generation (TAC)
------------------------------------------------------------
Generated TAC Code:
------------------------------------------------------------
  0: x = ASSIGN 10
  1: y = ASSIGN 20
  2: t1 = x + y
  3: z = ASSIGN t1
  4: PRINT z

✓ TAC generation successful

============================================================
Compilation completed successfully!
============================================================
```

---

## 📝 Quick MiniScript Tutorial

### Variables
```miniscript
var x = 10;
var y = 20;
print x + y;  // Output: 30
```

### If-Else
```miniscript
var age = 18;
if (age >= 18) {
    print "Adult";
} else {
    print "Minor";
}
```

### While Loop
```miniscript
var i = 1;
var sum = 0;
while (i <= 10) {
    sum = sum + i;
    i = i + 1;
}
print sum;  // Output: 55
```

### For Loop
```miniscript
var factorial = 1;
for (i = 1; i <= 5; i = i + 1) {
    factorial = factorial * i;
}
print factorial;  // Output: 120
```

### Functions
```miniscript
func multiply(a, b) {
    return a * b;
}

var result = multiply(6, 7);
print result;  // Output: 42
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview |
| `LANGUAGE_SPECIFICATION.md` | Language design and features |
| `GRAMMAR_ANALYSIS.md` | Grammar transformations and analysis |
| `PROJECT_REPORT.md` | Detailed 40+ page report |
| `USER_GUIDE.md` | Complete usage examples |
| `IMPLEMENTATION_SUMMARY.md` | Implementation details |

---

## 🗂️ Project Structure

```
CC Project/
├── compiler.py              ← Main entry point
├── src/                     ← Compiler source code
│   ├── lexer.py
│   ├── parser.py
│   ├── semantic_analyzer.py
│   ├── tac_generator.py
│   └── ... (4 more files)
├── examples/                ← Sample programs (8 files)
│   ├── example1_arithmetic.ms
│   ├── example2_if_else.ms
│   └── ... (6 more examples)
├── tests/                   ← Test suite
├── docs/                    ← Documentation
└── README.md
```

---

## 🧪 Run Tests

```bash
python tests/test_compiler.py
```

Expected: All tests pass ✓

---

## 🎯 Key Features

✅ **Complete Compiler Pipeline**
- Lexical analysis
- Parsing
- Semantic analysis
- Intermediate code generation

✅ **Comprehensive Error Handling**
- Line/column error reporting
- Error recovery
- Helpful error messages

✅ **Clean Code**
- Well-documented
- Modular design
- Easy to understand

✅ **Educational**
- Demonstrates all compiler phases
- Suitable for learning
- Professional quality

---

## 💡 Common Commands

```bash
# Basic compilation
python compiler.py examples/example1_arithmetic.ms

# Compile with verbose output (shows tokens and AST)
python compiler.py examples/example2_if_else.ms -v

# Compile a custom file
python compiler.py my_program.ms

# Run all tests
python tests/test_compiler.py
```

---

## 🐛 Troubleshooting

**Error: Python not found**
- Ensure Python 3.7+ is installed
- Add Python to system PATH

**Error: File not found**
- Use correct path to source file
- Check file extension (.ms)

**Compilation errors**
- Check syntax matches MiniScript grammar
- See USER_GUIDE.md for examples
- Refer to error messages for hints

---

## 📋 Supported Language Constructs

| Feature | Supported |
|---------|-----------|
| Variables | ✓ |
| Functions | ✓ |
| If-Else | ✓ |
| While Loops | ✓ |
| For Loops | ✓ |
| Comments | ✓ |
| Operators | ✓ |
| Print | ✓ |
| Type Checking | ✓ |
| Error Recovery | ✓ |

---

## 📖 Learning Path

1. **Start:** Read `LANGUAGE_SPECIFICATION.md`
2. **Explore:** Try examples 1-3
3. **Understand:** Read `GRAMMAR_ANALYSIS.md`
4. **Deep Dive:** Read `PROJECT_REPORT.md`
5. **Advanced:** Explore source code in `src/`

---

## 🎓 For Instructors

This project demonstrates:
- ✓ Lexical analysis principles
- ✓ Parsing techniques (recursive descent)
- ✓ Semantic analysis
- ✓ Intermediate code generation
- ✓ Error handling and recovery
- ✓ Software engineering best practices

Ideal for:
- Compiler design courses
- Programming language courses
- Software engineering projects
- Student learning projects

---

## 📞 Getting Help

1. **Check Documentation:** Read the relevant .md file
2. **Try Examples:** Run example programs
3. **Read Error Messages:** Compiler provides helpful errors
4. **Review Code:** Source code is well-commented

---

## ✨ What's Included

📦 **Source Code** (7 modules)
📚 **Documentation** (6 comprehensive guides)
🧪 **Test Suite** (complete coverage)
📝 **8 Example Programs**
✅ **Zero External Dependencies**

---

## 🎯 Next Steps

1. Run `python compiler.py examples/example1_arithmetic.ms`
2. Explore other examples
3. Create your own MiniScript program
4. Read the documentation
5. Examine the source code

---

**Ready to compile? Let's go! 🚀**

```bash
cd "CC Project"
python compiler.py examples/example1_arithmetic.ms
```

---

For more information, see the full documentation in the `docs/` folder.

**Happy Compiling!** 🎉
