# Axiom Language Specification

## 1. Purpose and Goals

Axiom is a minimalist programming language designed specifically for **mathematical computations**. It provides a clean, readable syntax for performing arithmetic calculations, working with variables, and implementing basic control flow.

**Target use cases:**
- Mathematical expression evaluation
- Iterative numerical computations (summations, factorials, etc.)
- Educational demonstrations of programming language concepts

## 2. Data Types

Axiom supports two numeric data types:

| Type    | Description            | Example       |
|---------|------------------------|---------------|
| Integer | Whole numbers          | `0`, `42`, `7` |
| Float   | Decimal numbers        | `3.14`, `0.5`  |

Type conversion is automatic — operations between integers and floats produce floats.

## 3. Variables

Variables are declared with the `let` keyword and reassigned with `=`:

```
let x = 10;
let pi = 3.14;
x = x + 1;
```

**Rules:**
- Variables must be declared with `let` before use.
- Variable names start with a letter (a-z, A-Z) and may contain letters, digits, and underscores.
- Variables are dynamically typed (no type annotations).

## 4. Operators

### 4.1 Arithmetic Operators

| Operator | Description    | Example     | Precedence |
|----------|----------------|-------------|------------|
| `+`      | Addition       | `3 + 2` → 5  | Low        |
| `-`      | Subtraction    | `5 - 1` → 4  | Low        |
| `*`      | Multiplication | `4 * 3` → 12 | Medium     |
| `/`      | Division       | `10 / 3` → 3.33 | Medium  |
| `^`      | Exponentiation | `2 ^ 3` → 8  | High       |
| `-` (unary) | Negation    | `-5` → -5    | Highest    |

**Precedence order (low to high):** `+, -` → `*, /` → `^` → unary `-`

**Associativity:**
- `+`, `-`, `*`, `/` are **left-associative**: `8 - 3 - 2` = `(8 - 3) - 2` = 3
- `^` is **right-associative**: `2 ^ 3 ^ 2` = `2 ^ (3 ^ 2)` = 512

### 4.2 Comparison Operators

| Operator | Description          | Example     |
|----------|----------------------|-------------|
| `>`      | Greater than         | `5 > 3`     |
| `<`      | Less than            | `2 < 7`     |
| `==`     | Equal to             | `x == 10`   |
| `!=`     | Not equal to         | `x != 0`    |
| `>=`     | Greater than or equal| `x >= 5`    |
| `<=`     | Less than or equal   | `x <= 100`  |

## 5. Control Structures

### 5.1 Conditional (if / then / else / end)

```
if condition then
    statements
end

if condition then
    statements
else
    statements
end
```

### 5.2 Loop (while / do / end)

```
while condition do
    statements
end
```

## 6. Built-in Functions

| Function     | Description                    | Example          |
|--------------|--------------------------------|------------------|
| `display(x)` | Prints the value to the console | `display(42);`  |

## 7. Statement Separator

All simple statements (let, assignment, display) must end with a semicolon (`;`).
Control structures (if, while) do **not** require a semicolon — they are terminated by `end`.

```
let x = 5;           // semicolon required
display(x);           // semicolon required
if x > 3 then        // no semicolon
    display(x);       // semicolon required
end                   // no semicolon
```

## 8. Formal Grammar (EBNF)

The complete formal grammar is defined in `grammar.ebnf`. Below is a summary:

```ebnf
program              = {statement};
statement            = (variable_declaration | assignment | display_statement) ";"
                     | if_statement | while_statement;
variable_declaration = "let" identifier "=" expression;
assignment           = identifier "=" expression;
display_statement    = "display" "(" expression ")";
if_statement         = "if" condition "then" {statement} ["else" {statement}] "end";
while_statement      = "while" condition "do" {statement} "end";
condition            = expression (">" | "<" | "==" | "!=" | ">=" | "<=") expression;
expression           = term {("+" | "-") term};
term                 = factor {("*" | "/") factor};
factor               = atom ["^" factor];
atom                 = ["-"] (number | identifier | "(" expression ")");
```

## 9. Implementation Architecture

Axiom follows a classic **three-stage interpreter pipeline**:

```
Source Code (.axm)
       │
       ▼
  ┌─────────┐
  │  LEXER  │   Converts source text into a stream of tokens.
  │         │   (src/lexer.py)
  └────┬────┘
       │ Token List
       ▼
  ┌─────────┐
  │ PARSER  │   Builds an Abstract Syntax Tree (AST) from tokens.
  │         │   (src/parser.py)
  └────┬────┘
       │ AST
       ▼
  ┌────────────┐
  │INTERPRETER │   Walks the AST and executes each node.
  │            │   (src/interpreter.py)
  └────────────┘
```

## 10. Keywords

The following words are reserved and cannot be used as variable names:

`let`, `if`, `then`, `else`, `end`, `while`, `do`, `display`

## 11. Error Handling

Axiom reports errors at two stages:

- **Syntax Errors** (during parsing): unexpected tokens, missing semicolons, unclosed blocks
- **Runtime Errors** (during execution): undefined variables, division by zero
