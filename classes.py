import math

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