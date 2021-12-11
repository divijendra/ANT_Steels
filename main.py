import math
import numpy as np
from scipy.optimize import minimize


def production_rate(width=0.1, thickness=0.1, length=6, diameter=0.008, density=7.85, speed=22,
                    wt_frac=0.96, vol_frac=0.97, time_gap=5, strands = 2):
    """

    :param width: width of the billet in metres
    :param thickness: thickness of the billet in metres
    :param length: length of the billet in metres
    :param diameter: diameter of the finished product in metres
    :param density: density of the steel in tons per cubic metre
    :param speed: Finishing bar speed in m/s
    :param frac_of_nominal_wt: Fraction of nominal weight to be retained
    :param frac_of_init_vol: Fraction of initial volume retained
    :param time_gap: Time gap between two bars at finishing stage in seconds
    :return: Production rate in tons per hour
    """
    bar_length = vol_frac * width * thickness * length / (strands * wt_frac * math.pi * (diameter ** 2) / 4)
    total_time = time_gap + (bar_length / speed)
    return 3600 * density * width * thickness * length * vol_frac / total_time


def objective(params, *variables):
    """

    :param params: (0_prod_rate (t/hr), 1_speed (am/s), 2_time_gap (s))
    :param variables: 0_vol_frac, 1_wt_frac, 2_strands, 3_diameter, 4_density, 5_width, 6_thickness, 7_length
    :return:
    """
    speed = params[0]
    time_gap = params[1]
    vol_frac = variables[0]
    wt_frac = variables[1]
    strands = variables[2]
    diameter = variables[3]
    density = variables[4]
    width = variables[5]
    thickness = variables[6]
    length = variables[7]
    return -production_rate(width, thickness, length, diameter, density, speed, wt_frac, vol_frac, time_gap, strands)


def constraint(params, *variables):
    return variables[8] + objective(params, *variables)


if __name__ == '__main__':
    density = float(input("Enter value of density (tons/m3): "))
    width = float(input("Enter width of the billet (mm): ")) / 1000
    thickness = float(input("Enter thickness of the billet (mm): ")) / 1000
    length = float(input("Enter length of billet (mm): ")) / 1000
    diameter = float(input("Enter diameter of the finished product (mm): ")) / 1000
    max_speed = float(input("Enter maximum finishing speed (m/sec): "))
    min_speed = float(input("Enter minimum finishing speed (m/sec): "))
    max_prod_rate = float(input("Enter maximum production rate (tons/hr): "))
    wt_frac = float(input("Enter required weight in terms of percentage of nominal weight required (%): ")) / 100
    vol_frac = 1 - float(input("Enter percentage of product lost during processing (%): ")) / 100
    min_time_gap = float(input("Enter minimum time gap at finishing stage (seconds): "))
    efficiency = float(input("Enter utilisation (%): ")) / 100
    strands = float(input("Enter number of strands: "))
    bounds_speed = (min_speed, max_speed)
    bounds_time_gap = (min_time_gap, math.inf)
    bounds = (bounds_speed, bounds_time_gap)
    init_vals = np.array([max_speed, min_time_gap])
    constr = {"type": "ineq", "fun": constraint, "args": (vol_frac, wt_frac, strands, diameter, density, width,
                                                          thickness, length, max_prod_rate)}
    result = minimize(objective, init_vals, method="SLSQP", bounds=bounds, constraints=constr, args=(vol_frac, wt_frac,
                                                                                                     strands, diameter,
                                                                                                     density, width,
                                                                                                     thickness, length,
                                                                                                     max_prod_rate))
    print("Maximum production rate possible:", -result.fun)
    print("Optimum speed and time gap to suit maximum production rate possible: ", result.x[0], "m/s and", result.x[1],
          "seconds")
