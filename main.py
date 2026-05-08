# ============================================
# Axiom Language - Main Entry Point
# ============================================
# Usage:
#   python main.py <filename.axm>
#   python main.py                   (starts interactive REPL)

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def run_source(source, interp):
    """Tokenize, parse, and execute source code."""
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse_program()
    interp.run(ast)


def run_file(filepath):
    """Run an Axiom source file (.axm)."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    with open(filepath, "r") as f:
        source = f.read()

    interp = Interpreter()
    try:
        run_source(source, interp)
    except (SyntaxError, RuntimeError) as e:
        print(f"Error: {e}")
        sys.exit(1)


def run_repl():
    """Run an interactive REPL (Read-Eval-Print Loop)."""
    print("Axiom Language REPL v0.1")
    print("Type 'exit' to quit.\n")

    interp = Interpreter()

    while True:
        try:
            line = input("axiom> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        line = line.strip()
        if line == "exit":
            print("Goodbye!")
            break
        if line == "":
            continue

        try:
            run_source(line, interp)
        except (SyntaxError, RuntimeError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        run_repl()
