from SParse.parser import Lexer

file = open('./SParse/input_tests/source1.c', 'r')
luthor = Lexer(file.read())
luthor.lex()
luthor.print_lexed()