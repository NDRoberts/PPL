def get_num_literal(stong):
    fetch = {
        'int': lambda q: numerize(q)[0],
        'float': lambda q: numerize(q)[1]
    }
    lit = ""
    token = 'int'
    c, ctype = get_char(stong)
    while ctype and ctype != "BLANK":
        stong, lit = add_char(stong, lit)
        c, ctype = get_char(stong)
    if '.' in lit:
        token = 'float'
    nl = fetch[token](lit)
    return (nl, token)


def add_char(inpt, unit):
    if len(inpt) > 0:
        unit += inpt[0]
        inpt = inpt[1:]
    else:
        unit = inpt[0]
        inpt = []
    return (inpt, unit)


def get_char(inpt):
    char_is = {
        "EOF": lambda q: q is None,
        "BLANK": lambda q: q in [' ', '\t', '\n', '\r'],
        "LETTER": lambda q: q.isalpha(),
        "DIGIT": lambda q: q.isdigit(),
        "OPERATOR": lambda q: q in ['+', '-', '*', '/'],
        "DELIMITER": lambda q: q in ['(', ')', '[', ']', '{', '}'],
        "PUNCTUATOR": lambda q: q in ['.', ',', ';', ':', '\'', '\"']
    }
    if len(inpt) > 0:
        c = inpt[0]
        ctype = [k for k, v in char_is.items() if char_is[k](c)][0]
        return (c, ctype)
    else:
        return (None, None)


def str_to_int(nstr):
    val = 0
    for i in range(len(nstr)):
        val += (ord(nstr[i]) - 48) * (10 ** (len(nstr) - i - 1))
    return int(val)


def str_to_float(nstr):
    val = 0
    if '.' in nstr:
        for i in range(nstr.index('.')):
            val += (ord(nstr[i]) - 48) * (10 ** (len(nstr) - i - 1))
        for j in range(nstr.index('.'), len(nstr)):
            val += (ord(nstr[j]) - 48) * (10 ** -(j - nstr.index('.') + 1))
    else:
        val = str_to_int(nstr)
    return float(val)


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


limes = input("Put in a number: ")
print(type(limes))
numbo = get_num_literal(limes)
print(f"You wrote '{limes}'.  To me, that means {numbo}.")

nambor = input("Put me a nombro: ")
print(numerize(nambor))
