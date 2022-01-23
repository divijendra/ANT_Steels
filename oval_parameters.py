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
    return (((total_area / 2) - ((r ** 2) * np.arccos(1 - (h / r)))) ** 2) - (((r + h - H) ** 2) * h * (2 * r - h))
#    return (total_area / 2) - ((r ** 2) * np.arccos(1 - (h / r))) + ((r + h - H) * math.sqrt(h * (2 * r - h)))


def h_prime_eqn(x, *args):
    r = args[0]
    B = args[1]
    return (B ** 2) - (4 * (x * (2 * r - x)))
#    return B - 2 * math.sqrt(x * (2 * r - x))


area_1 = float(input("Enter area of oval bar(sq mm): "))
area_2 = float(input("Enter area of next round (sq mm): "))
mult_factor = float(input("Enter b/B ratio: "))

Ds = math.sqrt(4 * area_2 / math.pi)
main_radius_oval = round((0.012 * Ds * Ds) + (1.01 * Ds) + 10.47, 0)
H = round((0.816 * Ds) - 0.975, 1)

h0 = 0.4 * H - 0.75 if area_1 > 150 else 0.3 * H - 0.14
h_result = root(h_eqn, h0, args=(main_radius_oval, area_1, H))
h = round(h_result.x[0], 1)

# h is height of the chords
# h_prime is grove depth (greater than h).

b = round(2 * math.sqrt(h * (2 * main_radius_oval - h)), 3)
B = round(b / mult_factor, 3)

h_prime_result = root(h_prime_eqn, h0, args=(main_radius_oval, B))
h_prime = round(h_prime_result.x[0], 1)

roll_gap = round(H - 2 * h_prime, 1)

print("H =", H, "mm")
print("R =", main_radius_oval, "mm")
print("h =", h_prime, "mm")
print("S =", roll_gap, "mm")
print("B =", B, "mm")
print("b =", b, "mm")
