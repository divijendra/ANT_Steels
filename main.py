# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



# Press the green button in the gutter to run the script.
import production_rate

if __name__ == '__main__':
    density = float(input("Enter value of density (tons/m3): "))
    width = float(input("Enter width of the billet (mm): ")) / 1000
    thickness = float(input("Enter thickness of the billet (mm): ")) / 1000
    length = float(input("Enter length of billet (mm): ")) / 1000
    diameter = float(input("Enter diameter of the finished product (mm): ")) /1000
    velocity = float(input("Enter finishing speed (m/sec): "))
    frac_of_nominal_wt = float(input("Enter required weight in terms of percentage of nominal weight required (%): ")) / 100
    frac_of_init_vol = 1 - float(input("Enter percentage of product lost during processing (%): ")) / 100
    time_gap = float(input("Enter time gap at finishing stage (seconds): "))

#    print(production_rate.production_rate())
    print(production_rate.production_rate(width, thickness, length, diameter, density, velocity, frac_of_nominal_wt, frac_of_init_vol, time_gap))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
