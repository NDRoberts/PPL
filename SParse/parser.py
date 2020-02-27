'''
CS3210 - Principles of Programming Languages
Programming Assignment 1: Lexical / Syntax Parser
@author Nate Roberts
'''

# Remember that a char_literal is one character in single-quotes, e.g. 'a'

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
    "else": TokenType.ELSE
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
    '&': "AND"
}


class Lexer:
    ''' Instantiable lexical parser '''
    char_is = {
        "EOF": lambda q: q is None,
        "BLANK": lambda q: q in [' ', '\t', '\n', '\r'],
        "LETTER": lambda q: q.isalpha(),
        "DIGIT": lambda q: q.isdigit(),
        "OPERATOR": lambda q: q in ['+', '-', '*', '/'],
        "DELIMITER": lambda q: q in ['(', ')', '[', ']', '{', '}'],
        "PUNCTUATOR": lambda q: q in [',', ';', ':', '\'', '\"'],
        "COMPARATOR": lambda q: q in ['=', '>', '<', '!']
    }

    def __init__(self, inpt):
        self.data = inpt.lower()
        self.parse = []
        c, ctype = self.get_char()
        # TODO: Finish init - determine getter based on char type,
        #       store (unit, token) pairs in self.parse
        for _ in range(len(self.data)):
            if ctype == "BLANK":
                self.get_non_blank()
            elif ctype == "LETTER":
                self.parse.append(self.get_char_seq())
            elif ctype == "DIGIT":
                self.parse.append(self.get_num_literal())
            elif c in SYMBOL:
                self.parse.append(self.get_symbol())
            else:
                self.parse.append(c, ">> BAD TOKEN <<")

    def get_char(self):
        if len(self.data) > 0:
            c = self.data[0]
            ctype = [k for k, v in self.char_is.items() if self.char_is[k](c)][0]
            return (c, ctype)
        else:
            return (None, None)

    def add_char(self, unit):
        unit += self.data[0]
        if len(self.data) > 1:
            self.data = self.data[1:]
        else:
            self.data = []
        return unit

    def get_non_blank(self):
        skip = ""
        c, ctype = self.get_char()
        if ctype == "BLANK":
            skip = self.add_char(skip)

    def get_char_seq(self):
        word = ""
        c, ctype = self.get_char()
        while ctype != "BLANK":
            word = self.add_char(word)
            c, ctype = self.get_char()
        if word in RESERVED:
            return (word, RESERVED[word])
        else:
            # FIXME: determine correct token type to return
            return (word, TokenType.CHAR_LITERAL)

    def get_num_literal(self):
        fetch = {
            TokenType.INT_LITERAL: lambda q: numerize(q)[0],
            TokenType.FLOAT_LITERAL: lambda q: numerize(q)[1]
        }
        lit = ""
        token = TokenType.INT_LITERAL
        c, ctype = self.get_char()
        while ctype and ctype != "BLANK":
            lit = self.add_char(lit)
            c, ctype = self.get_char()
        if '.' in lit:
            token = TokenType.FLOAT_LITERAL
        nl = fetch[token](lit)
        return (nl, token)

    def get_symbol(self):
        sym = ""
        c, ctype = '', ''
        while ctype and ctype not in ['BLANK', 'LETTER', 'DIGIT']:
            sym = self.add_char(sym)
            c, ctype = self.get_char()
        return (sym, SYMBOL[sym])


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
    if len(sys.argv) > 1:
        target = sys.argv[1]
        luthor = Lexer(target)
    else:
        print("Hoggnuts!")
        inpt = input("Make like your have a line of inpoots: ")
        luthor = Lexer(inpt)
    print(luthor.parse)
