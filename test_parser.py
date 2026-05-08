import sys
sys.path.insert(0, "src")
from lexer import Lexer
from parser import Parser

# --- Test 1: simple expression ---
print("=== Test 1: let + display ===")
code1 = "let x = 3 + 5 * 2; display(x);"
tokens1 = Lexer(code1).tokenize()
ast1 = Parser(tokens1).parse_program()
for s in ast1.statements:
    print(" ", s)

# --- Test 2: if/else ---
print("\n=== Test 2: if/else ===")
code2 = """
let a = 10;
if a > 5 then
    display(a);
else
    display(0);
end
"""
tokens2 = Lexer(code2).tokenize()
ast2 = Parser(tokens2).parse_program()
for s in ast2.statements:
    print(" ", s)

# --- Test 3: while loop ---
print("\n=== Test 3: while loop ===")
code3 = """
let i = 0;
while i < 5 do
    display(i);
    i = i + 1;
end
"""
tokens3 = Lexer(code3).tokenize()
ast3 = Parser(tokens3).parse_program()
for s in ast3.statements:
    print(" ", s)

# --- Test 4: nested expressions + unary minus ---
print("\n=== Test 4: unary minus + power ===")
code4 = "let y = -(3 + 2) ^ 2;"
tokens4 = Lexer(code4).tokenize()
ast4 = Parser(tokens4).parse_program()
for s in ast4.statements:
    print(" ", s)

print("\nAll parser tests passed!")
