# Test parser funx

import unittest
from SParse.parser import Lexer
from SParse.parser import TokenType
from unittest.mock import MagicMock
from unittest.mock import patch


class TestLexFuncs(unittest.TestCase):

    def setUp(self):
        self.lex = Lexer("{ Input String }")
        self.salt_file = "Identifier = 1; \n 4.082 >= \t true"

        # pass

    def test_init(self):
        self.assertIsNotNone(self.lex)
        self.assertIsInstance(self.lex, Lexer)
        self.assertIsInstance(self.lex.input, str)
        self.assertEqual(self.lex.input, "{ Input String }")
        self.assertEqual(self.lex.data, "{ input string }")

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
        c, ctype = self.lex.get_non_blank()
        self.assertEqual(c, ':')
        self.assertEqual(ctype, "PUNCTUATOR")
        self.assertEqual(self.lex.data, ':')

    def test_get_word(self):
        self.lex.data = "idnt false word_soup while"
        w, t = self.lex.get_word()
        self.assertEqual(w, "idnt")
        self.assertEqual(t, TokenType.IDENTIFIER)
        w, t = self.lex.get_word()
        self.assertEqual(w, "false")
        self.assertEqual(t, TokenType.FALSE)
        w, t = self.lex.get_word()
        self.assertEqual(w, "word_soup")
        self.assertEqual(t, TokenType.IDENTIFIER)
        w, t = self.lex.get_word()
        self.assertEqual(w, "while")
        self.assertEqual(t, TokenType.WHILE)

    def test_get_num_literal(self):
        self.lex.data = "1024 512.256 1"
        l, t = self.lex.get_num_literal()
        self.assertEqual(l, 1024)
        self.assertEqual(t, TokenType.INT_LITERAL)
        l, t = self.lex.get_num_literal()
        self.assertEqual(l, 512.256)
        self.assertEqual(t, TokenType.FLOAT_LITERAL)
        l, t = self.lex.get_num_literal()
        self.assertEqual(l, 1)
        self.assertEqual(t, TokenType.INT_LITERAL)
        l, t = self.lex.get_num_literal()
        self.assertIsNone(l)
        self.assertIsNone(t)
    
    def test_get_char_literal(self):
        self.lex.data = "'a' 'b' 'c"
        tk1 = self.lex.get_char_literal()
        tk2 = self.lex.get_char_literal()
        tk3 = self.lex.get_char_literal()
        self.assertEqual(tk1, ('a', TokenType.CHAR_LITERAL))
        self.assertEqual(tk2, ('b', TokenType.CHAR_LITERAL))
        self.assertEqual(tk3, (None, None))

    def test_get_symbol(self):
        self.lex.data = " + } >= ;q"
        tk1 = self.lex.get_symbol()
        tk2 = self.lex.get_symbol()
        tk3 = self.lex.get_symbol()
        tk4 = self.lex.get_symbol()
        tk5 = self.lex.get_symbol()
        self.assertEqual(tk1, ('+', TokenType.ADD))
        self.assertEqual(tk2, ('}', TokenType.CLOSE_CURLY))
        self.assertEqual(tk3, ('>=', TokenType.GREATER_EQUAL))
        self.assertEqual(tk4, (';', TokenType.SEMICOLON))
        self.assertEqual(tk5, (None, None))

    def test_lex(self):
        self.lex.data = self.salt_file
        self.lex.lex()
        self.assertEqual(len(self.lex.parse), 8)
        self.assertEqual(self.lex.parse[0], ("Identifier",
                         TokenType.IDENTIFIER))
        self.assertEqual(self.lex.parse[6], ("true", TokenType.TRUE))

    # TODO: I am suspending TDD, temporarily, because my knowledge
    # of it is no longer adequate relative to the time available
    # to me to turn this project in.  I will return to it at a later
    # date; for now, I hope I can make things work.
    @patch(Lexer.print)
    def test_print_lexed(self, mock_print):
        self.lex.print_lexed()
        mock_print.assertCalled()


if __name__ == '__main__':
    unittest.main()
