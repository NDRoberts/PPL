'''
CS3210 - Principles of Programming Languages
Programming Assignment 1: Lexical / Syntax Parser
@author Nate Roberts
I do hereby solemnly swear that I whacked this train wreck of code together all by myself, excepting only those blocks expressly credited to other authors.  No one else is to blame.
'''

import sys
from enum import Enum


# TokenType class based on example by Thyago Mota
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


# Error table provided by Thyago Mota
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


# Tree class by Thyago Mota
class Tree:

    TAB = "   "

    def __init__(self):
        self.data = None
        self.children = []

    def add(self, child):
        self.children.append(child)

    def print(self, tab=""):
        if self.data is not None:
            print(tab + self.data)
            tab += self.TAB
            for child in self.children:
                if isinstance(child, Tree):
                    child.print(tab)
                else:
                    print(tab + child)


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
        if len(ch) == 3 and ch[0] == '\'' and \
                ch[1].isalpha() and ch[2] == '\'':
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
            # print(f"Character [ {c} ] is a {ctype}.")
            if ctype == "EOF":
                token = (None, TokenType.EOF)
            elif ctype == "LETTER":
                token = self.get_word()
            elif ctype == "DIGIT":
                token = self.get_num_literal()
            elif ctype == "OPERATOR" or ctype == "DELIMITER" or \
                    ctype == "PUNCTUATOR" or ctype == "COMPARATOR" or \
                    ctype == "LOGICAL":
                token = self.get_symbol()
            else:
                tk, tp = self.get_word()
                token = (tk, "INVALID TOKEN!")
            if token[0] is not None or token[1] is not None:
                self.parse.append(token)

    def print_lexed(self):
        max_txt_length = 8
        for t in self.parse:
            if len(str(t[0])) > max_txt_length:
                max_txt_length = len(str(t[0]))
        print(f"Longest token: {max_txt_length}")
        print("Lexical tokens in source:")
        for token in self.parse:
            if token[0] is not None:
                ttxt = '{:>{width}}'.format(token[0], width=max_txt_length)
            else:
                ttxt = '{:>{width}}'.format("<<None>>", width=max_txt_length)
            print(f"|-> {ttxt} ({token[1]})")


class Synter:
    ''' Instantiable Syntactic Parser '''

    def __init__(self, src):
        pfile = open(src, 'r')
        if not pfile:
            raise IOError(ERRORS[2])
        lexida = Lexer(pfile.read())
        lexida.lex()
        self.data = lexida.parse
        self.tree = Tree()
        self.tree.data = "<ROOT>"
        self.tree = self.parse_program(self.tree)
        self.tree.print()

    def has_tokens(self):
        ''' Return True if tokens remain to be parsed (for readability) '''
        return len(self.data) > 0

    def pluck(self):
        ''' Remove next available (lexeme, token) pair from queue and return it '''
        if not self.has_tokens():
            raise Exception(ERRORS[99])
        lexeme, token = self.data[0]
        self.data = self.data[1:]
        return lexeme, token

    def parse_program(self, tree):
        ''' Parse a <program> unit (should be top level parse) '''
        # TODOne: read "int main ( ) { ... }" I guess?
        # TODO: call parse_declaration, parse_statement
        types = [TokenType.INT_TYPE,
                 TokenType.FLOAT_TYPE,
                 TokenType.BOOL_TYPE,
                 TokenType.CHAR_TYPE]
        bgn_stmt = [TokenType.OPEN_CURLY, TokenType.IDENTIFIER, TokenType.IF, TokenType.WHILE]
        sub_tree = Tree()
        sub_tree.data = "<program>"
        tree.add(sub_tree)
        END = False

        # Required: 'int'
        lexeme, token = self.pluck()
        if token == TokenType.INT_TYPE:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[12])

        # Required: 'main'
        lexeme, token = self.pluck()
        if token == TokenType.MAIN:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[11])

        # Required: '()'
        lexeme, token = self.pluck()
        if token == TokenType.OPEN_PAR:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[10])
        lexeme, token = self.pluck()
        if token == TokenType.CLOSE_PAR:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[9])

        # Required: '{'
        lexeme, token = self.pluck()
        if token == TokenType.OPEN_CURLY:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[8])

        # Program Body
        # Required: One or more <declaration>s
        if self.data[0][1] in types:
            self.parse_declaration(sub_tree)
        else:
            raise Exception(ERRORS[99])
        while self.data[0][1] in types:
            self.parse_declaration(sub_tree)
        # Required: One or more <statement>s
        if self.data[0][1] in bgn_stmt:
            self.parse_statement(sub_tree)
        else:
            raise Exception(ERRORS[99])
        while self.data[0][1] in bgn_stmt:
            self.parse_statement(sub_tree)

        # Required: '}'
        lexeme, token = self.pluck()
        if token == TokenType.CLOSE_CURLY:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[7])
        
        # Required: <EOF>
        lexeme, token = self.pluck()
        if token == TokenType.EOF:
            sub_tree.add("")
        else:
            raise Exception(ERRORS[6])

        tree.add(sub_tree)
        return tree

    def parse_addition(self, tree):
        # TODOne: call parse_term; also takes add/sub operators
        add_sub_ops = [TokenType.ADD, TokenType.SUBTRACT]
        sub_tree = Tree()
        sub_tree.data = '<addition>'
        self.parse_term(sub_tree)
        while self.data[0][1] in add_sub_ops:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            self.parse_term(sub_tree)
        tree.add(sub_tree)
        return tree

    def parse_assignment(self, tree):
        # TODOne: takes Identifiers and Expressions
        sub_tree = Tree()
        sub_tree.data = '<assignment>'
        # Required: <identifier>
        lexeme, token = self.pluck()
        if token == TokenType.IDENTIFIER:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[16])
        # OPTIONAL: [<expression>]
        if self.data[0][1] == TokenType.OPEN_BRACKET:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            self.parse_expression(sub_tree)
            lexeme, token = self.pluck()
            if token == TokenType.CLOSE_BRACKET:
                sub_tree.add(lexeme)
            else:
                raise Exception(ERRORS[13])
        # Required: '='
        lexeme, token = self.pluck()
        if token == TokenType.ASSIGNMENT:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[18])
        # Required: <expression>
        self.parse_expression(sub_tree)
        # Required: ';'
        lexeme, token = self.pluck()
        if token == TokenType.SEMICOLON:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[17])
        tree.add(sub_tree)
        return tree

    def parse_conjunction(self, tree):
        # TODOne: call parse_equality
        sub_tree = Tree()
        sub_tree.data = '<conjunction>'
        self.parse_equality(sub_tree)
        while self.data[0][1] == TokenType.AND:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            self.parse_equality(sub_tree)
        tree.add(sub_tree)
        return tree

    def parse_declaration(self, tree):
        # TODOne: takes Types, Identifiers, Int_literals
        types = [TokenType.INT_TYPE,
                 TokenType.FLOAT_TYPE,
                 TokenType.BOOL_TYPE,
                 TokenType.CHAR_TYPE]
        sub_tree = Tree()
        sub_tree.data = "<declaration>"
        finished = False

        # Required: <type>
        lexeme, token = self.pluck()
        if token in types:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[99])

        # Required: <identifier>
        lexeme, token = self.pluck()
        if token == TokenType.IDENTIFIER:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[16])

        # OPTIONAL: '[ <int_literal> ]'
        if self.data[0][1] == TokenType.OPEN_BRACKET:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            lexeme, token = self.pluck()
            if token == TokenType.INT_LITERAL:
                sub_tree.add(lexeme)
            else:
                raise Exception(ERRORS[14])
            lexeme, token = self.pluck()
            if token == TokenType.CLOSE_BRACKET:
                sub_tree.add(lexeme)
            else:
                raise Exception(ERRORS[13])

        # OPTIONAL: Further <identifier> [<int_literal>] pairs
        while not finished:
            if self.data[0][1] == TokenType.COMMA:
                lexeme, token = self.pluck()
                sub_tree.add(lexeme)
            else:
                finished
                break
            lexeme, token = self.pluck()
            if token == TokenType.IDENTIFIER:
                sub_tree.add(lexeme)
            else:
                raise Exception(ERRORS[16])
            if self.data[0][1] == TokenType.OPEN_BRACKET:
                lexeme, token = self.pluck()
                sub_tree.add(lexeme)
                lexeme, token = self.pluck()
                if token == TokenType.INT_LITERAL:
                    sub_tree.add(lexeme)
                else:
                    raise Exception(ERRORS[14])
                lexeme, token = self.pluck()
                if token == TokenType.CLOSE_BRACKET:
                    sub_tree.add(lexeme)
                else:
                    raise Exception(ERRORS[13])
        # Required: ';'
        lexeme, token = self.pluck()
        if token == TokenType.SEMICOLON:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[17])

        tree.add(sub_tree)
        return tree

    def parse_equality(self, tree):
        # TODOne: call parse_relation; also takes eq/neq operators?
        eq_neq_ops = [TokenType.EQUALITY, TokenType.INEQUALITY]
        sub_tree = Tree()
        sub_tree.data = '<equality>'
        self.parse_relation(sub_tree)
        if self.data[0][1] in eq_neq_ops:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            self.parse_relation(sub_tree)
        tree.add(sub_tree)
        return tree

    def parse_expression(self, tree):
        # TODOne: call parse_conjunction
        sub_tree = Tree()
        sub_tree.data = '<expression>'
        self.parse_conjunction(sub_tree)
        while self.data[0][1] == TokenType.OR:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            self.parse_conjunction(sub_tree)
        tree.add(sub_tree)
        return tree

    def parse_factor(self, tree):
        # TODOne: call parse_expression, parse_literal; also takes identifiers
        literals = [TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL, TokenType.CHAR_LITERAL, TokenType.TRUE, TokenType.FALSE]
        sub_tree = Tree()
        sub_tree.data = '<factor>'
        # Required: <identifier> OR <identifier> [<expression>] OR
        # <literal> OR (<expression>)
        next_token = self.data[0][1]
        if next_token == TokenType.IDENTIFIER:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            if self.data[0][1] == TokenType.OPEN_BRACKET:
                lexeme, token = self.pluck()
                sub_tree.add(lexeme)
                self.parse_expression(sub_tree)
                lexeme, token = self.pluck()
                if token == TokenType.CLOSE_BRACKET:
                    sub_tree.add(lexeme)
                else:
                    raise Exception(ERRORS[13])
        elif next_token in literals:
            self.parse_literal(sub_tree)
        elif next_token == TokenType.OPEN_PAR:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            self.parse_expression(sub_tree)
            lexeme, token = self.pluck()
            if token == TokenType.CLOSE_PAR:
                sub_tree.add(lexeme)
            else:
                raise Exception(ERRORS[9])
        else:
            raise Exception(ERRORS[16])
        tree.add(sub_tree)
        return tree

    def parse_if(self, tree):
        # TODOne: call parse_expression, parse_statement
        sub_tree = Tree()
        sub_tree.data = '<if>'
        lexeme, token = self.pluck()
        if token == TokenType.IF:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[99])
        # Required: '('
        lexeme, token = self.pluck()
        if token == TokenType.OPEN_PAR:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[10])
        self.parse_expression(sub_tree)
        lexeme, token = self.pluck()
        if token == TokenType.CLOSE_PAR:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[9])
        if self.data[0][1] == TokenType.ELSE:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            self.parse_statement(sub_tree)
        tree.add(sub_tree)
        return tree

    def parse_literal(self, tree):
        # TODOne: Figure out which kind it is or something
        literals = [TokenType.INT_LITERAL, TokenType.FLOAT_LITERAL, TokenType.CHAR_LITERAL, TokenType.TRUE, TokenType.FALSE]
        sub_tree = Tree()
        sub_tree.data = '<literal>'
        lexeme, token = self.pluck()
        if token in literals:
            sub_tree.add(str(lexeme))
        else:
            raise Exception(ERRORS[99])
        tree.add(sub_tree)
        return tree

    def parse_relation(self, tree):
        # TODOne: call parse_addition; also takes rel_ops?
        rel_ops = [TokenType.LESS, TokenType.LESS_EQUAL,
                   TokenType.GREATER, TokenType.GREATER_EQUAL]
        sub_tree = Tree()
        sub_tree.data = '<relation>'
        self.parse_addition(sub_tree)
        if self.data[0][1] in rel_ops:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            self.parse_addition(sub_tree)
        tree.add(sub_tree)
        return tree

    def parse_statement(self, tree):
        # TODOne: call parse_assignment, parse_if, parse_while
        sub_tree = Tree()
        sub_tree.data = '<statement>'
        next_token = self.data[0][1]
        # Required: <assignment>, <if>, <while>, or {<statement>+}
        if next_token == TokenType.IDENTIFIER:
            self.parse_assignment(sub_tree)
        elif next_token == TokenType.IF:
            self.parse_if(sub_tree)
        elif next_token == TokenType.WHILE:
            self.parse_while(sub_tree)
        elif next_token == TokenType.OPEN_CURLY:
            # TODO: handle substatements
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            self.parse_statement(sub_tree)
            lexeme, token = self.pluck()
            if token == TokenType.CLOSE_CURLY:
                sub_tree.add(lexeme)
            else:
                raise Exception(ERRORS[7])
        else:
            raise Exception(ERRORS[19])
        tree.add(sub_tree)
        return tree

    def parse_term(self, tree):
        # TODOne: call parse_factor; also takes mult/div operators
        mul_div_ops = [TokenType.MULTIPLY, TokenType.DIVIDE]
        sub_tree = Tree()
        sub_tree.data = '<term>'
        self.parse_factor(sub_tree)
        while self.data[0][1] in mul_div_ops:
            lexeme, token = self.pluck()
            sub_tree.add(lexeme)
            self.parse_factor(sub_tree)
        tree.add(sub_tree)
        return tree

    def parse_while(self, tree):
        # TODOne: call parse_expression, parse_statement
        sub_tree = Tree()
        sub_tree.data = '<while>'
        lexeme, token = self.pluck()
        if token == TokenType.WHILE:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[99])
        # Required: '('
        lexeme, token = self.pluck()
        if token == TokenType.OPEN_PAR:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[10])
        self.parse_expression(sub_tree)
        # Required: ')'
        lexeme, token = self.pluck()
        if token == TokenType.CLOSE_PAR:
            sub_tree.add(lexeme)
        else:
            raise Exception(ERRORS[9])
        self.parse_statement(sub_tree)
        tree.add(sub_tree)
        return tree


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        zamp = Synter(file_name)
        # luthor = Lexer(open(file_name, 'r').read())
        # luthor.lex()
        # luthor.print_lexed()
    else:
        zomp = Synter('./SParse/input_tests/source2.c')
        # raise Exception(ERRORS[1])
    # data = (open("./SParse/input_tests/source1.c", "r")).read()
    # data = open(file_name, 'r')
    # luthor = Lexer(data.read())
