from language import *
import re

class ParseError(Exception):
    pass

def parse(program: str):
    tokens = re.findall(r'\d+\.\d+|\w+|[^\w\s]', program)
    tokens = tokens.__str__().replace("'(', ", "[").replace("')'", "]")
    try:
        tokens = eval(tokens)
    except SyntaxError:
        raise ParseError('Unmatched parentheses')
    tokens = separate_on_semicolon(tokens)
    return get_tree(tokens)

def get_tree(lst: list[str] | str):
    if isinstance(lst, str):
        return get_tree_for_str(lst)
    if len(lst) == 1:
        return get_tree(lst[0])
    if lst[0] == 'lambda':
        if len(lst) != 3:
            raise ParseError('Invalid lambda')
        x = get_tree(lst[1])
        if not isinstance(x, Var):
            raise ParseError('Invalid variable name in lambda')
        t = get_tree(lst[2])
        return Lambda(x, t)
    if lst[1] == '+':
        if len(lst) != 3:
            raise ParseError('Invalid addition')
        t1 = get_tree(lst[0])
        t2 = get_tree(lst[2])
        return Add(t1, t2)
    if lst[1] == '-':
        if len(lst) != 3:
            raise ParseError('Invalid subtraction')
        t1 = get_tree(lst[0])
        t2 = get_tree(lst[2])
        return Subtract(t1, t2)
    if lst[0] == '-':
        if len(lst) != 2:
            raise ParseError('Invalid negation')
        t = get_tree(lst[1])
        return Subtract(t)
    if lst[1] == '*':
        if len(lst) != 3:
            raise ParseError('Invalid multiplication')
        t1 = get_tree(lst[0])
        t2 = get_tree(lst[2])
        return Multiply(t1, t2)
    if lst[1] == '/':
        if len(lst) != 3:
            raise ParseError('Invalid division')
        t1 = get_tree(lst[0])
        t2 = get_tree(lst[2])
        return Divide(t1, t2)
    if lst[0] == 'do':
        if len(lst) != 2:
            raise ParseError('Invalid do')
        return get_tree_for_do(lst[1])
    if lst[0] == 'E':
        if len(lst) != 2:
            raise ParseError('Invalid expectation')
        prog = get_tree(lst[1])
        return E(prog)
    if lst[0] == 'flip':
        if len(lst) != 2:
            raise ParseError('Invalid flip')
        p = get_tree(lst[1])
        return Flip(p)
    if lst[0] == 'normal':
        if len(lst) != 3:
            raise ParseError('Invalid normal')
        m = get_tree(lst[1])
        v = get_tree(lst[2])
        return Normal(m, v)
    if lst[0] == 'geometric':
        if len(lst) != 2:
            raise ParseError('Invalid geometric')
        p = get_tree(lst[1])
        return Geometric(p)
    if len(lst) == 2:
        t1 = get_tree(lst[0])
        t2 = get_tree(lst[1])
        return App(t1, t2)
    return lst
    
def get_tree_for_str(string: str):
    if string[0].isnumeric():
        return Num(float(string))
    return Var(string)

def get_tree_for_do(lst: list[str]):
    m = []
    for xt in lst[:-1]:
        if xt[1] != '~':
            raise ParseError('Invaild do notation')
        x = get_tree(xt[0])
        if not isinstance(x, Var):
            raise ParseError('Invalid variable name in do')
        t = get_tree(xt[2:])
        m.append(Sample(x, t))
    m.append(get_tree(lst[-1]))
    return Do(m)

def separate_on_semicolon(lst: list[str|list]):
    for i in range(len(lst)):
        if isinstance(lst[i], list):
            lst[i] = separate_on_semicolon(lst[i])
    if ';' not in lst:
        return lst
    else:
        new_lst = []
        i = 0
        while True:
            try:
                j = lst.index(';', i)
            except ValueError:
                new_lst.append(lst[i:])
                break
            new_lst.append(lst[i:j])
            i = j + 1
        return new_lst
