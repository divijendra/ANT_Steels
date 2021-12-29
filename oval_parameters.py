import math
import subprocess
import sys
import pkg_resources

try:
    import numpy as np
    from scipy.optimize import root
except ImportError:
    required = ["numpy", "scipy"]
    installed = [pkg.key for pkg in pkg_resources.working_set]
    missing = [pkg for pkg in required if pkg not in installed]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    # noinspection PyUnresolvedReferences
    import numpy as np
    # noinspection PyUnresolvedReferences
    from scipy.optimize import root


def h_eqn(x, *args):
    r = args[0]
    total_area = args[1]
    H = args[2]
    h = x
    return (total_area / 2) - ((r ** 2) * np.arccos(1 - (h / r))) + ((r + h - H) * math.sqrt(h * (2 * r - h)))


def h_prime_eqn(x, *args):
    r = args[0]
    B = args[1]
    return B - 2 * math.sqrt(x * (2 * r - x))


radius = float(input("Enter main radius of oval pass (mm): "))
area = float(input("Enter area of oval bar(sq mm): "))
H = float(input("Enter thickness of oval bar (H in mm): "))
mult_factor = float(input("Enter b/B ratio: "))
h0 = float(input("Enter an initial guess for groove depth (mm): "))
h_result = root(h_eqn, h0, args=(radius, area, H))
h = h_result.x[0]
# h is height of the chords
# h_prime is grove depth (greater than h).
b = 2 * math.sqrt(h * (2 * radius - h))
B = b / mult_factor
h_prime_result = root(h_prime_eqn, h0, args=(radius, B))
h_prime = h_prime_result.x[0]
roll_gap = H - 2 * h_prime
print("Groove depth (h in mm): ", h_prime)
print("Roll gap at collars (S in mm): ", roll_gap)
print("Width of oval pass (B in mm): ", B)
print("Width of oval bar cross-section (b in mm): ", b)