class AST:
    pass

class Distribution(AST):
    def mean():
        pass

class Num(AST):
    # r
    def __init__(self, r):
        self.r = r
    def __str__(self):
        return f'{self.r}'
    def __repr__(self):
        return f'Num({repr(self.r)})'

class Var(AST):
    # x
    def __init__(self, x):
        self.x = x
    def __str__(self):
        return f'{self.x}'
    def __repr__(self):
        return f'Var({repr(self.x)})'

class Lambda(AST):
    # λx. t
    def __init__(self, x, t):
        self.x = x
        self.t = t
    def __str__(self):
        return f'lambda ({self.x}) ({self.t})'
    def __repr__(self):
        return f'Lambda({repr(self.x)}, {repr(self.t)})'

class App(AST):
    # t1 t2
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __str__(self):
        return f'({self.t1}) ({self.t2})'
    def __repr__(self):
        return f'App({repr(self.t1)}, {repr(self.t2)})'

class Add(AST):
    # t1 + t2
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __str__(self):
        return f'({self.t1}) + ({self.t2})'
    def __repr__(self):
        return f'Add({repr(self.t1)}, {repr(self.t2)})'

class Subtract(AST):
    # t1 - t2, or -t
    def __init__(self, *args):
        if len(args) == 2:
            self.t1 = args[0]
            self.t2 = args[1]
        elif len(args) == 1:
            self.t1 = None
            self.t2 = args[0]
    def __str__(self):
        if self.t1 is None:
            return f'-({self.t2})'
        else:
            return f'({self.t1}) - ({self.t2})'
    def __repr__(self):
        if self.t1 is None:
            return f'Subtract({repr(self.t2)})'
        else:
            return f'Subtract({repr(self.t1)}, {repr(self.t2)})'

class Multiply(AST):
    # t1 * t2
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __str__(self):
        return f'({self.t1}) * ({self.t2})'
    def __repr__(self):
        return f'Multiply({repr(self.t1)}, {repr(self.t2)})'

class Divide(AST):
    # t1 / t2
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
    def __str__(self):
        return f'({self.t1}) / ({self.t2})'
    def __repr__(self):
        return f'Divide({repr(self.t1)}, {repr(self.t2)})'

class Sample(AST):
    # x ← t
    def __init__(self, x, t):
        self.x = x
        self.t = t
    def __str__(self):
        return f'{self.x} ~ {self.t}'
    def __repr__(self):
        return f'Sample({repr(self.x)}, {repr(self.t)})'

class Do(AST):
    # do{x1 ← t1; x2 ← t2; ... ; xn ← tn; t}
    def __init__(self, m: list[Sample]):
        self.m = m
    def __str__(self):
        return f'do({"; ".join(str(l) for l in self.m)})'
    def __repr__(self):
        return f'Do({repr(self.m)})'

class E(AST):
    # E prog
    def __init__(self, prog):
        self.prog = prog
    def __str__(self):
        return f'E({self.prog})'
    def __repr__(self):
        return f'E({repr(self.prog)})'

class Flip(Distribution):
    # flip p
    def __init__(self, p):
        self.p = p
    def __str__(self):
        return f'flip({self.p})'
    def __repr__(self):
        return f'Flip({repr(self.p)})'
    def mean(self):
        return self.p

class Normal(Distribution):
    # normal m v
    def __init__(self, m, v):
        self.m = m
        self.v = v
    def __str__(self):
        return f'normal({self.m})({self.v})'
    def __repr__(self):
        return f'Normal({repr(self.m)}, {repr(self.v)})'
    def mean(self):
        return self.m
    
class Geometric(Distribution):
    # geom p
    def __init__(self, p):
        self.p = p
    def __str__(self):
        return f'geometric({self.p})'
    def __repr__(self):
        return f'Geometric({repr(self.p)})'
    def mean(self):
        return Divide(Subtract(1, self.p), self.p)
    