import math
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


class Billet:
    def __init__(self):
        self.density = float(input("Enter value of density (tons/m3): "))
        self.width = float(input("Enter width of the billet (mm): ")) / 1000
        self.thickness = float(input("Enter thickness of the billet (mm): ")) / 1000
        self.length = float(input("Enter length of billet (mm): ")) / 1000
        self.volume = self.width * self.length * self.thickness


class Product:
    def __init__(self, billet):
        self.diameter = float(input("Enter diameter of the finished product (mm): ")) / 1000
        self.max_speed = float(input("Enter maximum finishing speed (m/sec): "))
        self.min_speed = float(input("Enter minimum finishing speed (m/sec): "))
        self.max_prod_rate = float(input("Enter maximum production rate (tons/hr): "))
        self.wt_frac = 1 - float(input("Enter percentage reduction in weight (%): ")) / 100
        self.vol_frac = 1 - float(input("Enter percentage of product lost during processing (%): ")) / 100
        self.min_time_gap = float(input("Enter minimum time gap at finishing stage (seconds): "))
        self.utilisation = float(input("Enter utilisation (%): ")) / 100
        self.demand = float(input("Enter product mix demand per month (%): ")) / 100
        self.strands = float(input("Enter number of strands: "))
        self.area = math.pi * (self.diameter ** 2) / 4
        self.density = billet.density
        self.prod_rate = 0
        self.speed = 0
        self.time_gap = 0
        self.days_per_month = 0
        self.monthly_production = 0

    def production_rate(self, billet, speed, time_gap):
        bar_length = billet.volume * self.vol_frac / (self.strands * self.wt_frac * self.area)
        total_time = time_gap + (bar_length / speed)
        return 3600 * self.density * billet.width * billet.thickness * billet.length * self.vol_frac / total_time

    def modify(self, billet):
        self.density = billet.density


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
    total_days = int(input("Enter total number of working days per year: ")) / 12
    total = 0
    for product in products:
        total += (product.demand / (24 * product.prod_rate * product.utilisation))
    production_per_month = total_days / total
    for product in products:
        product.days_per_month = product.demand * production_per_month / (24 * product.prod_rate * product.utilisation)
        product.monthly_production = product.demand * production_per_month
    return production_per_month, total_days


def yearly_prod_rate(prod_per_month):
    return 12 * prod_per_month


if __name__ == '__main__':
    billet = Billet()
    n = int(input("Enter number of products: "))
    products = list()
    for i in range(n):
        print("**********Enter details of product " + str(i + 1) + "**********")
        p = Product(billet)
        result = optimal_speed_and_time_gap(p, billet)
        p.speed = result.x[0]
        p.time_gap = result.x[1]
        p.prod_rate = -result.fun
        products.append(p)
    total_monthly_prod, num_days_in_month = monthly_prod_rate(products)
    total_yearly_prod = yearly_prod_rate(total_monthly_prod)

    print("**********Select an option**********")
    print("1. Display optimal speed, time gap and maximum possible production rates for the entered products")
    print("2. Calculate monthly production rate of list of products")
    print("3. Calculate yearly production rate for list of products")
    print("4. Add details of another product")
    print("5. Change details of the billet")
    print("6. quit")
    query = int(input("Enter your choice: "))
    while query in (1, 2, 3, 4, 5):
        if query == 1:
            print("Optimal speed(m/s)\tOptimal time gap(s)\tProduction rate(tonnes/hr)")
            for product in products:
                print("{:.5f}\t\t\t{:.5f}\t\t\t\t{:.5f}".format(product.speed, product.time_gap, product.prod_rate))
        elif query == 2:
            print("Diameter(m)\t\tNo. of days per month\t\tMonthly production in tonnes")
            for product in products:
                print("{:.5f}\t\t\t{:.5f}\t\t{:.5f}".format(product.diameter, product.days_per_month, product.monthly_production))
            print("Total monthly production is", total_monthly_prod,
                  " tonnes and total number of working days in a month are", num_days_in_month)
        elif query == 3:
            print("Diameter(m)\t\tNo. of days per year\t\tYearly production in tonnes")
            for product in products:
                print("{:.5f}\t\t\t{:.5f}\t\t{:.5f}".format(product.diameter, product.days_per_month * 12, product.monthly_production * 12))
            print("Total yearly production is", total_yearly_prod,
                  "tonnes and total number of working days in a year are", num_days_in_month * 12)
        elif query == 4:
            products.append(Product(billet))
        elif query == 5:
            billet = Billet()
            for i in range(len(products)):
                products[i].modify(billet)
                result = optimal_speed_and_time_gap(products[i], billet)
                products[i].prod_rate = -result.fun
                products[i].speed = result.x[0]
                products[i].time_gap = result.x[1]
            print("**********Details updated**********")
        else:
            break
        print("**********Select an option**********")
        print("1. Display optimal speed, time gap and maximum possible production rates for the entered products")
        print("2. Calculate monthly production rate of list of products")
        print("3. Calculate yearly production rate for list of products")
        print("4. Add details of another product")
        print("5. Change details of the billet")
        print("6. quit")
        query = int(input("Enter your choice: "))
