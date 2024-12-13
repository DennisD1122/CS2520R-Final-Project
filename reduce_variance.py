from language import *

def reduce_variance(program: AST):
    return _reduce_variance(program, {}, set(), False)

def _reduce_variance(program: AST, dist_info: dict[str, Distribution], exclude: set[str], expect: bool):
    if isinstance(program, Num):
        return program
    elif isinstance(program, Var):
        x = program.x
        if x in dist_info and x not in exclude:
            return dist_info[x].mean()
        else:
            return Var(x)
    elif isinstance(program, Lambda):
        x = program.x
        t = _reduce_variance(program.t, dist_info, exclude, expect)
        return Lambda(x, t)
    elif isinstance(program, Add):
        t1 = _reduce_variance(program.t1, dist_info, exclude, expect)
        t2 = _reduce_variance(program.t2, dist_info, exclude, expect)
        return Add(t1, t2)
    elif isinstance(program, Subtract):
        if program.t1 is None:
            t1 = None
        else:
            t1 = _reduce_variance(program.t1, dist_info, exclude, expect)
        t2 = _reduce_variance(program.t2, dist_info, exclude, expect)
        return Subtract(t1, t2)
    elif isinstance(program, Multiply):
        vars1 = set()
        vars2 = set()
        find_vars(program.t1, vars1)
        find_vars(program.t2, vars2)
        common_vars = set.intersection(vars1, vars2)
        exclude = set(exclude)
        for v in common_vars:
            exclude.add(v)
        t1 = _reduce_variance(program.t1, dist_info, exclude, expect)
        t2 = _reduce_variance(program.t2, dist_info, exclude, expect)
        return Multiply(t1, t2)
    elif isinstance(program, Divide):
        t1 = _reduce_variance(program.t1, dist_info, exclude, expect)
        t2 = program.t2
        return Divide(t1, t2)
    elif isinstance(program, Do):
        m = program.m
        expr = _reduce_variance(m[-1], dist_info, exclude, expect)
        if expect and len(m) > 1:
            for sample in reversed(m[:-1]):
                x = sample.x.x
                t = sample.t
                dist_info[x] = t
                expr = _reduce_variance(expr, dist_info, exclude, expect)
        m_new = []
        vars = set()
        find_vars(expr, vars)
        for sample in m[:-1]:
            if sample.x.x in vars:
                m_new.append(sample)
        m_new.append(expr)
        return Do(m_new)
    elif isinstance(program, E):
        prog = _reduce_variance(program.prog, dist_info, exclude, True)
        return E(prog)

def find_vars(program, vars: set[str]):
    if isinstance(program, Var):
        vars.add(program.x)
    elif isinstance(program, Lambda):
        find_vars(program.x, vars)
        find_vars(program.t, vars)
    elif isinstance(program, Add) or isinstance(program, Subtract) or \
         isinstance(program, Multiply) or isinstance(program, Divide):
        find_vars(program.t1, vars)
        find_vars(program.t2, vars)
    elif isinstance(program, Do):
        find_vars(program.m[-1], vars)
    elif isinstance(program, E):
        find_vars(program.prog, vars)
