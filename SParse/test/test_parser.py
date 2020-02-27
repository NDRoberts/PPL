# Test parser funx

import unittest
from SParse.parser import Lexer
# from unittest.mock import mock_open, patch


class TestLexFuncs(unittest.TestCase):
    def setUp(self):
        self.lex = Lexer('1024')

    def test_get_char(self):
        c, ctype = self.lex.get_char()
        self.assertEqual('1', c)
        self.assertEqual('DIGIT', ctype)

    def test_add_char(self):
        split = ""
        split = self.lex.add_Char(split)
        self.assertEqual(split, '1')
        self.assertEqual(self.lex.data, '024')


if __name__ == '__main__':
    unittest.main()
