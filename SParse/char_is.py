char_is = {
    "EOF": lambda q: q is None,
    "BLANK": lambda q: q in [' ', '\t', '\n', '\r'],
    "LETTER": lambda q: q.isalpha(),
    "DIGIT": lambda q: q.isdigit(),
    "OPERATOR": lambda q: q in ['+', '-', '*', '/'],
    "DELIMITER": lambda q: q in ['(', ')', '[', ']', '{', '}'],
    "PUNCTUATOR": lambda q: q in ['.', ',', ';', ':', '\'', '\"']
}

inpt = input("Enter a string to parse: ")
for c in inpt:
    ctype = [k for k, v in char_is.items() if char_is[k](c)][0]
    print(f"{c} -:: {ctype}")
