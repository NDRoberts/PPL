# Test parser funx

import unittest
from SParse.parser import Lexer
from SParse.parser import TokenType
# from unittest.mock import mock_open, patch


class TestLexFuncs(unittest.TestCase):
    def setUp(self):
        self.lex = Lexer("{ Input String }")
        # pass

    def test_init(self):
        self.assertIsNotNone(self.lex)
        self.assertIsInstance(self.lex, Lexer)
        self.assertIsInstance(self.lex.input, str)
        self.assertEqual(self.lex.input, "{ input string }")
        self.assertEqual(self.lex.data, "{ input string }")
        # TODO: Examine the rest of __init__ (?)

    def test_get_char(self):
        self.lex.data = "1024 abc"
        c, ctype = self.lex.get_char()
        self.assertEqual('1', c)
        self.assertEqual('DIGIT', ctype)

    def test_add_char(self):
        self.lex.data = "1024 abc"
        split = ""
        split = self.lex.add_char(split)
        self.assertEqual(split, '1')
        self.assertEqual(self.lex.data, '024 abc')

    def test_get_non_blank(self):
        self.lex.data = "   \t   \n   \r   :"
        c, ctype = self.lex.get_char()
        self.assertIsNotNone(c)
        self.assertEqual(c, ' ')
        self.assertEqual(ctype, 'BLANK')
        self.lex.get_non_blank()
        self.assertEqual(self.lex.data, ':')

    def test_get_char_seq(self):
        self.lex.data = "idnt false word_soup while"
        w, t = self.lex.get_char_seq()
        self.assertEqual(w, "idnt")
        self.assertEqual(t, TokenType.IDENTIFIER)
        w, t = self.lex.get_char_seq()
        self.assertEqual(w, "false")
        self.assertEqual(t, TokenType.FALSE)
        w, t = self.lex.get_char_seq()
        self.assertEqual(w, "word_soup")
        self.assertEqual(t, TokenType.IDENTIFIER)
        w, t = self.lex.get_char_seq()
        self.assertEqual(w, "while")
        self.assertEqual(t, TokenType.WHILE)

    def test_get_num_literal(self):
        self.lex.data = "1024 512.256"
        l, t = self.lex.get_num_literal()
        self.assertEqual(l, 1024)
        self.assertEqual(t, TokenType.INT_LITERAL)
        l, t = self.lex.get_num_literal()
        self.assertEqual(l, 512.256)
        self.assertEqual(t, TokenType.FLOAT_LITERAL)
        l, t = self.lex.get_num_literal()
        self.assertIsNone(l)
        self.assertIsNone(t)

    def test_get_symbol(self):
        self.lex.data = " + } >= ;q"
        s, t = self.lex.get_symbol()
        self.assertEqual(s, '+')
        self.assertEqual(t, TokenType.ADD)
        s, t = self.lex.get_symbol()
        self.assertEqual(s, '}')
        self.assertEqual(t, TokenType.CLOSE_CURLY)
        s, t = self.lex.get_symbol()
        self.assertEqual(s, '>=')
        self.assertEqual(t, TokenType.GREATER_EQUAL)
        s, t = self.lex.get_symbol()
        self.assertEqual(s, ';')
        self.assertEqual(t, TokenType.SEMICOLON)
        s, t = self.lex.get_symbol()
        self.assertIsNone(s)
        self.assertIsNone(t)
    



if __name__ == '__main__':
    unittest.main()
