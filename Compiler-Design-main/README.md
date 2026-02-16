# 🔬 Compiler Design Lab Experiments

A comprehensive collection of compiler design implementations covering lexical analysis, syntax analysis, parsing techniques, and automata theory conversions.

## 📚 Table of Contents

- [Overview](#overview)
- [Experiments](#experiments)
- [Prerequisites](#prerequisites)
- [How to Run](#how-to-run)
- [Experiment Details](#experiment-details)
- [Key Concepts](#key-concepts)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository contains Python implementations of fundamental compiler design concepts and algorithms, developed as part of college laboratory coursework. Each experiment demonstrates a critical phase or technique used in building compilers and interpreters.

## 🧪 Experiments

| #   | Experiment Name                                                                   | Description                                        |
| --- | --------------------------------------------------------------------------------- | -------------------------------------------------- |
| 1   | [Implementation of Lexical Analyzer](#1-lexical-analyzer)                         | Tokenizes input source code into lexemes           |
| 2   | [Conversion from Regular Expression to NFA](#2-regex-to-nfa)                      | Implements Thompson's Construction algorithm       |
| 3   | [Conversion from NFA to DFA](#3-nfa-to-dfa)                                       | Subset construction method for automata conversion |
| 4   | [Elimination of Left Recursion & Left Factoring](#4-left-recursion-and-factoring) | Grammar transformation techniques                  |
| 5   | [Elimination of Ambiguity](#5-ambiguity-elimination)                              | Resolving ambiguous grammar productions            |
| 6   | [FIRST and FOLLOW Computation](#6-first-and-follow)                               | Essential for predictive parsing                   |
| 7   | [Computation of LEADING and TRAILING](#7-leading-and-trailing)                    | Operator precedence parsing support                |
| 8   | [Predictive Parsing Table](#8-predictive-parsing)                                 | LL(1) parsing table construction                   |
| 9   | [Shift Reduce Parsing](#9-shift-reduce-parsing)                                   | Bottom-up parsing technique                        |

## 🛠️ Prerequisites

- **Python 3.7+**
- No external libraries required (uses only standard library)

## 🚀 How to Run

### Running Individual Experiments

```bash
# Navigate to the repository directory
cd "Compiler Design"

# Run any experiment
python "Implementation of Lexical Analyzer.py"
python "Conversion from Regular Expression to NFA.py"
python "Conversion from NFA to DFA.py"
# ... and so on
```

### Example Output

```bash
python "Conversion from Regular Expression to NFA.py"
```

Output:

```
Converting Postfix Regex: ab|*c.
------------------------------
State 640:
  --[ε]--> State 688
...
```

## 📖 Experiment Details

### 1. Lexical Analyzer

**File:** `Implementation of Lexical Analyzer.py`

Implements a lexical analyzer (scanner) that breaks down source code into tokens. Recognizes:

- Keywords (if, else, while, etc.)
- Identifiers
- Operators
- Numbers
- Special symbols

**Key Concepts:** Tokenization, Pattern Matching, Lexemes

---

### 2. Regex to NFA

**File:** `Conversion from Regular Expression to NFA.py`

Converts regular expressions to Non-deterministic Finite Automata using **Thompson's Construction** algorithm.

**Features:**

- Supports operators: `*` (Kleene star), `|` (union), `.` (concatenation)
- Uses epsilon (ε) transitions
- Builds NFA from postfix notation

**Example:** `(a|b)*c` → NFA with epsilon transitions

---

### 3. NFA to DFA

**File:** `Conversion from NFA to DFA.py`

Converts NFA to DFA using the **Subset Construction** algorithm.

**Features:**

- Epsilon closure computation
- Move operation implementation
- State minimization through subset construction
- **Integrated with Experiment 2:** Automatically imports NFA from the Regex to NFA file

**Key Concepts:** Subset Construction, Epsilon Closure, DFA State Transitions

---

### 4. Left Recursion and Factoring

**File:** `Elimination of Left Recursion & Left Factoring.py`

Transforms context-free grammars to eliminate:

- **Left Recursion:** Prevents infinite loops in top-down parsing
- **Left Factoring:** Reduces backtracking by factoring common prefixes

**Example:**

```
Before: A → Aα | β
After:  A → βA'
        A' → αA' | ε
```

---

### 5. Ambiguity Elimination

**File:** `Elimination of Ambiguity.py`

Resolves ambiguous grammar by introducing operator precedence and associativity rules.

**Techniques:**

- Operator precedence assignment
- Associativity disambiguation
- Grammar restructuring

---

### 6. FIRST and FOLLOW

**File:** `FIRST and FOLLOW Computation.py`

Computes FIRST and FOLLOW sets for grammar symbols, essential for:

- Constructing predictive parsing tables
- LL(1) parser implementation
- Detecting grammar conflicts

**FIRST(X):** Set of terminals that begin strings derived from X  
**FOLLOW(X):** Set of terminals that can appear immediately after X

---

### 7. LEADING and TRAILING

**File:** `Computation of LEADING and TRAILING.py`

Computes LEADING and TRAILING sets for operator precedence parsing.

**LEADING(X):** Terminals that can appear as leftmost in strings derived from X  
**TRAILING(X):** Terminals that can appear as rightmost in strings derived from X

---

### 8. Predictive Parsing Table

**File:** `Predictive Parsing Table.py`

Constructs LL(1) predictive parsing table using FIRST and FOLLOW sets.

**Features:**

- Table-driven parsing
- Non-recursive implementation
- Conflict detection (ensures LL(1) property)

---

### 9. Shift Reduce Parsing

**File:** `Shift Reduce Parsing.py`

Implements bottom-up shift-reduce parser for context-free grammars.

**Operations:**

- **Shift:** Push input symbol onto stack
- **Reduce:** Replace handle with production head
- **Accept:** Successful parse completion
- **Error:** Invalid input detection

## 🔑 Key Concepts

### Phases of Compilation

1. **Lexical Analysis** ← Experiments 1
2. **Syntax Analysis** ← Experiments 4-9
3. **Semantic Analysis**
4. **Intermediate Code Generation**
5. **Code Optimization**
6. **Code Generation**

### Automata Theory

- **Regular Expressions** → **NFA** → **DFA** (Experiments 2-3)
- Finite state machines
- Thompson's Construction
- Subset Construction

### Parsing Techniques

- **Top-Down Parsing:** LL(1), Predictive Parsing (Experiments 6, 8)
- **Bottom-Up Parsing:** Shift-Reduce, LR Parsing (Experiment 9)
- **Operator Precedence Parsing:** (Experiment 7)

## 📊 Learning Outcomes

After completing these experiments, you will understand:

✅ How compilers tokenize and parse source code  
✅ Automata theory and state machine conversions  
✅ Grammar transformation techniques  
✅ Different parsing strategies and their trade-offs  
✅ Building blocks of compiler front-end implementation

## 🤝 Contributing

Contributions are welcome! If you'd like to:

- Add new experiments
- Improve existing implementations
- Fix bugs or enhance documentation

Please feel free to open an issue or submit a pull request.

## 📝 Notes

- All implementations prioritize **clarity** over optimization for educational purposes
- Code includes detailed comments explaining each step
- Some experiments (like NFA to DFA) are designed to work together through imports

## 📧 Contact

For questions or discussions about these implementations:

- Open an issue in this repository
- Contributions and feedback are appreciated!

## 📄 License

This project is open source and available for educational purposes.

---

⭐ **Star this repository** if you find it helpful for your compiler design studies!

**Happy Compiling! 🚀**
