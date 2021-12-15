import math
from classes import Billet, Product
from scipy.optimize import minimize

def objective(params, *variables):
    """

    :param params: (0_speed (m/s), 1_time_gap (s))
    :param variables: (product, billet)
    :return:
    """
    return -variables[0].production_rate(variables[1], params[0], params[1])


def constraint(params, *variables):
    """

    :param params: (0_speed (m/s), 1_time_gap (s))
    :param variables: (product, billet)
    :return:
    """
    return variables[0].max_prod_rate + objective(params, *variables)


def optimal_speed_and_time_gap(product, billet):
    speed_bounds = (product.min_speed, product.max_speed)
    time_gap_bounds = (product.min_time_gap, math.inf)
    bounds = (speed_bounds, time_gap_bounds)
    init_vals = np.array([product.max_speed, product.min_time_gap])
    constr = {"type": "ineq", "fun": constraint, "args": (product, billet)}
    result = minimize(objective, init_vals, method="SLSQP", bounds=bounds, constraints=constr, args=(product, billet))
    return result


def monthly_prod_rate(products):
    total_days = int(input("Enter total number of working days_per_month per month: "))
    sum = 0
    for product in products:
        sum += (product.demand / (24 * product.prod_rate * product.utilisation))
    production_per_month = total_days / sum
    for product in products:
        product.days_per_month = product.demand * production_per_month / (24 * product.prod_rate * product.utilisation)
        product.monthly_production = product.demand * production_per_month
    return production_per_month, total_days


def yearly_prod_rate(prod_per_month):
    return 12 * prod_per_month
