'''
CS3210 - Principles of Programming Languages
Programming Assignment 1: Lexical / Syntax Parser
@author Nate Roberts
'''

import sys
from enum import Enum


class TokenType(Enum):
    EOF = 0
    INT_TYPE = 1
    MAIN = 2
    OPEN_PAR = 3
    CLOSE_PAR = 4
    OPEN_CURLY = 5
    CLOSE_CURLY = 6
    OPEN_BRACKET = 7
    CLOSE_BRACKET = 8
    COMMA = 9
    ASSIGNMENT = 10
    SEMICOLON = 11
    IF = 12
    ELSE = 13
    WHILE = 14
    OR = 15
    AND = 16
    EQUALITY = 17
    INEQUALITY = 18
    LESS = 19
    LESS_EQUAL = 20
    GREATER = 21
    GREATER_EQUAL = 22
    ADD = 23
    SUBTRACT = 24
    MULTIPLY = 25
    DIVIDE = 26
    BOOL_TYPE = 27
    FLOAT_TYPE = 28
    CHAR_TYPE = 29
    IDENTIFIER = 30
    INT_LITERAL = 31
    TRUE = 32
    FALSE = 33
    FLOAT_LITERAL = 34
    CHAR_LITERAL = 35


ERRORS = {
    1: "Source file missing",
    2: "Couldn't open source file",
    3: "Lexical error",
    4: "Digit expected",
    5: "Symbol missing",
    6: "EOF expected",
    7: "'}' expected",
    8: "'{' expected",
    9: "')' expected",
    10: "'(' expected",
    11: "main expected",
    12: "int type expected",
    13: "']' expected",
    14: "int literal expected",
    15: "'[' expected",
    16: "identifier expected",
    17: "';' expected",
    18: "'=' expected",
    19: "identifier, if, or while expected",
    42: "What were you even TRYING to do?!",
    99: "Syntax error"
}


RESERVED = {
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "int": TokenType.INT_TYPE,
    "bool": TokenType.BOOL_TYPE,
    "float": TokenType.FLOAT_TYPE,
    "char": TokenType.CHAR_TYPE,
    "while": TokenType.WHILE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "main": TokenType.MAIN,
    "or": TokenType.OR,
    "and": TokenType.AND
}


SYMBOL = {
    # Operators:
    '+': TokenType.ADD,
    '-': TokenType.SUBTRACT,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVIDE,
    # Logicals:
    '=': TokenType.ASSIGNMENT,
    '==': TokenType.EQUALITY,
    '!=': TokenType.INEQUALITY,
    '>': TokenType.GREATER,
    '<': TokenType.LESS,
    '>=': TokenType.GREATER_EQUAL,
    '<=': TokenType.LESS_EQUAL,
    '||': TokenType.OR,
    '&&': TokenType.AND,
    # Delimiters:
    '(': TokenType.OPEN_PAR,
    ')': TokenType.CLOSE_PAR,
    '[': TokenType.OPEN_BRACKET,
    ']': TokenType.CLOSE_BRACKET,
    '{': TokenType.OPEN_CURLY,
    '}': TokenType.CLOSE_CURLY,
    ',': TokenType.COMMA,
    ';': TokenType.SEMICOLON,
    # Partial tokens:
    '!': "NOT",
    '|': "OR",
    '&': "AND",
    '\'': "SQUOTE",
    '\"': "DQUOTE"
}


class Lexer:
    ''' Instantiable lexical parser '''
    char_is = {
        "EOF": lambda q: q is None,
        "BLANK": lambda q: q in [' ', '\t', '\n', '\r'],
        "LETTER": lambda q: q.isalpha() or q == '_',
        "DIGIT": lambda q: q.isdigit(),
        "OPERATOR": lambda q: q in ['+', '-', '*', '/'],
        "DELIMITER": lambda q: q in ['(', ')', '[', ']', '{', '}'],
        "PUNCTUATOR": lambda q: q in [',', ';', ':', '\'', '\"', '.'],
        "COMPARATOR": lambda q: q in ['=', '>', '<', '!'],
        "LOGICAL": lambda q: q in ['|', '&']
        # "SOMETHING ELSE": lambda q: type(q) == chr
    }

    def __init__(self, inpt):
        self.input = inpt
        self.data = self.input.lower()
        self.parse = []

    def get_char(self):
        if len(self.data) > 0:
            c = self.data[0]
            ctype = [k for k, v in self.char_is.items()
                     if self.char_is[k](c)][0]
            return (c, ctype)
        return (None, "EOF")

    def add_char(self, unit):
        if len(self.data) > 0:
            unit += self.data[0]
        if len(self.data) > 1:
            self.data = self.data[1:]
        else:
            self.data = []
        return unit

    def get_non_blank(self):
        skip = ""
        c, ctype = self.get_char()
        while ctype == "BLANK":
            skip = self.add_char(skip)
            c, ctype = self.get_char()
        return (c, ctype)

    def get_word(self):
        word = ""
        c, ctype = self.get_non_blank()
        while c and (ctype == "LETTER" or ctype == "DIGIT"):
            word = self.add_char(word)
            c, ctype = self.get_char()
        if word in RESERVED:
            return (word, RESERVED[word])
        return (word, TokenType.IDENTIFIER)

    def get_num_literal(self):
        fetch = {
            TokenType.INT_LITERAL: lambda q: numerize(q)[0],
            TokenType.FLOAT_LITERAL: lambda q: numerize(q)[1]
        }
        lit = ""
        token = TokenType.INT_LITERAL
        c, ctype = self.get_non_blank()
        while c and (c == '.' or ctype == "DIGIT"):
            lit = self.add_char(lit)
            c, ctype = self.get_char()
        if '.' in lit:
            token = TokenType.FLOAT_LITERAL
        if len(lit) > 0:
            nl = fetch[token](lit)
            return (nl, token)
        return (None, None)
    
    def get_char_literal(self):
        ch = ""
        c, ctype = self.get_non_blank()
        while c and ctype != "BLANK":
            ch = self.add_char(ch)
            c, ctype = self.get_char()
        if len(ch) == 3 and ch[0] == '\'' and ch[1].isalpha() and ch[2] == '\'':
            return (ch[1], TokenType.CHAR_LITERAL)
        return (None, None)

    def get_symbol(self):
        sym = ""
        c, ctype = self.get_non_blank()
        while c and ctype not in ['BLANK', 'LETTER', 'DIGIT']:
            sym = self.add_char(sym)
            c, ctype = self.get_char()
        if sym in SYMBOL:
            return (sym, SYMBOL[sym])
        return (None, None)

    def lex(self):
        while (None, TokenType.EOF) not in self.parse:
            token = None
            c, ctype = self.get_non_blank()
            if ctype == "EOF":
                token = (None, TokenType.EOF)
            elif ctype == "LETTER":
                token = self.get_word()
            elif ctype == "DIGIT":
                token = self.get_num_literal()
            elif ctype == "OPERATOR" or ctype == "DELIMITER" or ctype == "PUNCTUATOR" or ctype == "COMPARATOR" or ctype == "LOGICAL":
                token = self.get_symbol()
            else:
                tk, tp = self.get_word()
                token = (tk, "INVALID TOKEN!")
            if token[0] is not None or token[1] is not None:
                self.parse.append(token)

    def print_lexed(self):
        max_token_length = 8
        for t in self.parse:
            if len(str(t[0])) > max_token_length:
                max_token_length = len(t[0])
        print(f"Longest token: {max_token_length}")
        print("Lexical tokens in source:")
        for token in self.parse:
            if token[0] is not None:
                ttxt = '{:>{width}}'.format(f"{chr(183)}{token[0]}{chr(183)}", width=max_token_length)
            else:
                ttxt = '{:{width}}'.format("<<None>>", width=max_token_length)
            print(f"|->{ttxt} {token[1]}")


def numerize(nstr):
    ingr, frac = 0, 0
    if '.' in nstr:
        pt = nstr.index('.')
        for i in range(pt):
            ingr += (ord(nstr[i]) - 48) * (10 ** (pt - i - 1))
        for j in range(len(nstr) - pt):
            if j > 0:
                frac += (ord(nstr[j + pt]) - 48) * (10 ** -j)
    else:
        pt = len(nstr)
        for i in range(pt):
            ingr += (ord(nstr[i]) - 48) * (10 ** (pt - i - 1))
    if frac >= 0.5:
        return (int(ingr + 1), float(ingr + frac))
    else:
        return (int(ingr), float(ingr + frac))


if __name__ == '__main__':
    # data = ""
    # if len(sys.argv) > 1:
    #     if sys.argv[1][0] == '\"':
    #         data = sys.argv[1]
    #     else:
    #         test_file = open(sys.argv[1], "r")
    #         data = test_file.read()
    #         test_file.close()
    #     luthor = Lexer(data)
    # else:
    #     print("No input file specified.")
    #     inpt = input("Enter a line to be parsed as input: ")
    #     luthor = Lexer(inpt)
    #     luthor.lex()
    data = (open("./SParse/input_tests/source1.c", "r")).read()
    luthor = Lexer(data)
    luthor.lex()
    # print(luthor.parse)
    luthor.print_lexed()
    # print("Lexical tokens found in source file:")
    # for k, t in luthor.parse:
    #     print(f"| {k}   -> {t}")
