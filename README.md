# Axiom

**A minimalist, high-speed mathematical expression language.**

## About

Axiom is a simple programming language designed for mathematical computations. Built with Python as an educational project for a Programming Languages course.

For the full language specification, see [Language Specification](docs/language_specification.md).

## Features

- Integer and float data types
- Arithmetic operators: `+`, `-`, `*`, `/`, `^`
- Comparison operators: `>`, `<`, `==`, `!=`, `>=`, `<=`
- Variable declarations with `let`
- Control structures: `if / then / else / end`, `while / do / end`
- Output with `display()`
- Interactive REPL mode

## Project Structure

```
programming_language/
├── main.py                  # Entry point (file runner + REPL)
├── docs/
│   ├── grammar.ebnf         # Formal EBNF grammar
│   └── language_specification.md  # Full language specification
├── src/
│   ├── lexer.py             # Tokenizer
│   ├── ast_nodes.py         # AST node definitions
│   ├── parser.py            # Recursive descent parser
│   └── interpreter.py       # Tree-walking interpreter
└── examples/
    ├── demo.axm             # Feature showcase
    ├── factorial.axm        # 10! calculation
    ├── fibonacci.axm        # First 10 Fibonacci numbers
    ├── power.axm            # 2^10 with a loop
    └── comparison.axm       # Comparison operators demo
```

## Usage

### Run a file
```bash
python main.py examples/demo.axm
```

### Interactive REPL
```bash
python main.py
```

## Example Program

```
let n = 10;
let result = 1;
let i = 1;

while i <= n do
    result = result * i;
    i = i + 1;
end

display(result);
```

Output: `3628800`

## Architecture

```
Source Code (.axm) → Lexer → Token List → Parser → AST → Interpreter → Output
```
