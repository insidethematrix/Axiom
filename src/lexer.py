from enum import Enum

class TokenType(Enum):

    LET = "LET"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    END = "END"
    WHILE = "WHILE"
    DO = "DO"
    DISPLAY = "DISPLAY"


   
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    POWER = "POWER"  #^
    GREATER = "GREATER"
    LESS = "LESS"
    EQUAL_EQUAL = "EQUAL_EQUAL" #==
    NOT_EQUAL = "NOT_EQUAL" #!=
    GREATER_EQUAL = "GREATER_EQUAL" #>=
    LESS_EQUAL = "LESS_EQUAL" #<=

    LPAREN = "LPAREN" #(
    RPAREN = "RPAREN" #)
    ASSIGN = "ASSIGN"   #=
    SEMICOLON = "SEMICOLON" #;

    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    EOF = "EOF"
class Token:
    def __init__(self,type,lexeme):
        self.type = type
        self.lexeme = lexeme

class Lexer:
    def __init__(self,source):
        self.source = source
        self.pos = 0
        self.current_char = source[0]

    def advance(self):
        self.pos+=1
        if self.pos >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]
    
    def peek(self):
        next_pos = self.pos + 1
        if next_pos >=len(self.source):
            return None
        else:
            return self.source[next_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def read_number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        if self.current_char is not None and self.current_char == ".":
            result+=self.current_char
            self.advance()

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return result

    def read_identifier(self):
        result = ""
        while (self.current_char is not None) and (self.current_char.isalnum() or self.current_char == "_") :
            result += self.current_char
            self.advance()
        return result
    
    def tokenize(self):
        tokens = []
        KEYWORDS = {
        "let": TokenType.LET,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "then": TokenType.THEN,
        "end": TokenType.END,
        "do": TokenType.DO,
        "display": TokenType.DISPLAY}

        while self.current_char is not None:
        # 1. Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

        # 2. Number?
            if self.current_char.isdigit():
                # Read number and create NUMBER token
                number_val = self.read_number()
                tokens.append(Token(TokenType.NUMBER, number_val))
                continue

            # 3. Letter? (could be identifier or keyword)
            if self.current_char.isalpha():
                # Read identifier and check if it's a keyword
                word = self.read_identifier()
                if word in KEYWORDS:
                    tokens.append(Token(KEYWORDS[word], word))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, word))
                continue

            # 4. Single-character operators: +, -, *, /, ^, (, ), ;
            if self.current_char == "+":
                tokens.append(Token(TokenType.PLUS, "+"))
                self.advance()
                continue

            if self.current_char == "-":
                tokens.append(Token(TokenType.MINUS, "-"))
                self.advance()
                continue

            if self.current_char == "*":
                tokens.append(Token(TokenType.MULTIPLY, "*"))
                self.advance()
                continue

            if self.current_char == "/":
                tokens.append(Token(TokenType.DIVIDE, "/"))
                self.advance()
                continue

            if self.current_char == "^":
                tokens.append(Token(TokenType.POWER, "^"))
                self.advance()
                continue

            if self.current_char == "(":
                tokens.append(Token(TokenType.LPAREN, "("))
                self.advance()
                continue

            if self.current_char == ")":
                tokens.append(Token(TokenType.RPAREN, ")"))
                self.advance()
                continue

            if self.current_char == ";":
                tokens.append(Token(TokenType.SEMICOLON, ";"))
                self.advance()
                continue

            if self.current_char == ">":
                if self.peek() == "=":       # next char is '='?
                    tokens.append(Token(TokenType.GREATER_EQUAL, ">="))
                    self.advance()           # skip '>'
                    self.advance()           # skip '='
                else:
                    tokens.append(Token(TokenType.GREATER, ">"))
                    self.advance()           # skip '>'
                continue

            if self.current_char == "<":
                if self.peek() == "=":       # next char is '='?
                    tokens.append(Token(TokenType.LESS_EQUAL, "<="))
                    self.advance()           # skip '<'
                    self.advance()           # skip '='
                else:
                    tokens.append(Token(TokenType.LESS, "<"))
                    self.advance()           # skip '<'
                continue

            if self.current_char == "=":
                if self.peek() == "=":       # next char is '='?
                    tokens.append(Token(TokenType.EQUAL_EQUAL, "=="))
                    self.advance()           # skip first '='
                    self.advance()           # skip second '='
                else:
                    tokens.append(Token(TokenType.ASSIGN, "="))
                    self.advance()           # skip '='
                continue

            if self.current_char == "!":
                if self.peek() == "=":       # next char is '='?
                    tokens.append(Token(TokenType.NOT_EQUAL, "!="))
                    self.advance()           # skip '!'
                    self.advance()           # skip '='
                else:
                    raise Exception(f"Invalid character: '!' at position {self.pos}")
                continue
            raise Exception(f"Unexpected character: {self.current_char}")

        tokens.append(Token(TokenType.EOF, "EOF"))
        return tokens



        
        
