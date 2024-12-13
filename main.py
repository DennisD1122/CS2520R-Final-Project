from parse import *
from reduce_variance import *

programs = [
    """
    lambda (theta) (E(do(
        X ~ normal(theta)(1);
        X
    )))
    """,
    """
    lambda (theta) (E(do(
        X ~ normal(theta)(1);
        Y ~ normal(X)(2);
        Y
    )))
    """,
    """
    lambda (theta) (E(do(
        X ~ normal(theta)(1);
        X+X
    )))
    """,
    """
    lambda (theta) (E(do(
        X ~ normal(theta)(1);
        Y ~ normal(theta+1)(2);
        X*Y
    )))
    """,
    """
    lambda (theta) (E(do(
        X ~ normal(theta)(1);
        Y ~ normal(X)(2);
        X*Y
    )))
    """,
    """
    lambda (theta) (E(do(
        X ~ normal(theta)(1);
        Y ~ normal(theta+1)(2);
        X/Y
    )))
    """,
    """
    lambda (theta) (E(do(
        X ~ geometric(p/2);
        Y ~ geometric(p);
        X/(Y+1)
    )))
    """,
]

for program in programs:
    t = parse(program)
    print('ORIGINAL PROGRAM:')
    print(t)
    print('TRANSFORMED PROGRAM:')
    print(reduce_variance(t))
    print()
