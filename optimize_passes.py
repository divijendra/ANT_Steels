import math
from math import pow, log, sqrt
import subprocess
import sys
import pkg_resources

try:
    import numpy as np
    from scipy.optimize import minimize
except ImportError:
    required = ["numpy", "scipy"]
    installed = [pkg.key for pkg in pkg_resources.working_set]
    missing = [pkg for pkg in required if pkg not in installed]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    # noinspection PyUnresolvedReferences
    import numpy as np
    # noinspection PyUnresolvedReferences
    from scipy.optimize import minimize


class Input:
    def __init__(self, a0, an, n, ranges):
        self.a0 = a0
        self.an = an
        self.n = n
        self.ranges = ranges


def objective(x, *args):
    lever = x[0]
    r = x[1]
    red_ratio_per_pass = pow(args[0].an / args[0].a0, 1 / args[0].n)
    return (red_ratio_per_pass * pow(lever, (-args[0].n + 1) / 2)) - r


def ineq_constr1(x, *args):
    val = objective(x, *args)
    return val


def ineq_constr2(x, *args):
    lever = x[0]
    r = x[1]
    n = args[0].n
    in_range = []
    val = objective(x, * args)
    if val < 0:
        return -1
    for i in range(len(args[0].ranges)):
        for j in range(1, n + 1):
            flag = 0
            ak = args[0].a0 * math.pow(lever, j - 1) * r
            if args[0].ranges[i][0] <= ak <= args[0].ranges[i][1]:
                flag = 1
            in_range.append(flag)
    return sum(in_range) - 4


if __name__ == '__main__':
    input_vals = Input(3934, 50, 16, [(302, 327), (193, 209), (109, 118), (75, 82), (48, 52)])
    args = (input_vals, 0)
    r_bounds = (0, 1)
    lever_bounds = (1, 1.1)
    bounds = (lever_bounds, r_bounds)
    init_vals = (1, 0.7612)
    constr1 = {"type": "ineq", "fun": ineq_constr1, "args": args}
    constr2 = {"type": "ineq", "fun": ineq_constr2, "args": args}
    constraints = [constr1, constr2]
    result = minimize(objective, init_vals, method="SLSQP", bounds=bounds, constraints=constraints, args=args)
    print(result)
    lever = result.x[0]
    n = input_vals.n
    r = result.x[1]
    print("*****Areas*****")
    for j in range(1, n+1):
        ak = args[0].a0 * math.pow(lever, j * (j - 1) / 2) * math.pow(r, j - 1)
        print(j, ak, sep="\t")


"""def objective1(x, *args):
    lever = x[0]
    rr = x[1]
    lr2 = lever * math.pow(rr, 2)
    under_root = pow(log(lr2), 2) - 8 * log(lever) * log(rr / (args[0].an / args[0].a0))
    if under_root < 0:
        return math.inf
    plus = (-log(lr2) + sqrt(under_root)) / (2 * log(lever))
    return plus


def objective2(x, *args):
    lever = x[0]
    rr = x[1]
    lr2 = lever * math.pow(rr, 2)
    under_root = pow(log(lr2), 2) - 8 * log(lever) * log(rr / (args[0].an / args[0].a0))
    minus = (-log(lr2) + sqrt(under_root)) / (2 * log(lever))
    return minus


def ineq_constr1(x, *args):
    return objective1(x, args[0]) - 2


def eq_constr1(x, *args):
    return math.ceil(objective1(x, args[0])) % 2


def eq_constr(x, *args):
    lever = x[0]
    n = math.ceil(x[1])
    rr = x[2]
    in_range = []
    if objective(x, *args) > 0 and n % 2 == 0:
        return 0
    for i in range(len(args[0].ranges)):
        flag = 0
        for j in range(n + 1):
            ak = args[0].a0 * math.pow(lever, j * (j + 1) / 2) * math.pow(rr, j + 1)
            if args[0].ranges[i][0] <= ak <= args[0].ranges[i][1]:
                flag = 1
            in_range.append(flag)
    if sum(in_range) >= 1:
        return 0
    else:
        return -1



if __name__ == '__main__':
    input_vals = Input(3934, 50, [(302, 327), (193, 209), (109, 118), (75, 82), (48, 52)])
    args = (input_vals, 0)
    rr_bounds = (0.1, 1)
    lever_bounds = (1, 2)
    bounds = (lever_bounds, rr_bounds)
    init_vals = (1.0096, 16)
    constr1 = {"type": "ineq", "fun": ineq_constr1, "args": args}
    constr2 = {"type": "eq", "fun": eq_constr1, "args": args}
    constraints = [constr1, constr2]
    result = minimize(objective1, init_vals, method="SLSQP", bounds=bounds, constraints=constraints, args=args)
    print(result)"""
