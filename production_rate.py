import math


def production_rate(width=0.1, thickness=0.1, length=6, diameter=0.008, density=7.85, velocity=22,
                    frac_of_nominal_wt=0.96, frac_of_init_vol=0.97, time_gap=5):
    """

    :param width: width of the billet in metres
    :param thickness: thickness of the billet in metres
    :param length: length of the billet in metres
    :param diameter: diameter of the finished product in metres
    :param density: density of the steel in tons per cubic metre
    :param velocity: Finishing bar speed in m/s
    :param frac_of_nominal_wt: Fraction of nominal weight to be retained
    :param frac_of_init_vol: Fraction of initial volume retained
    :param time_gap: Time gap between two bars at finishing stage in seconds
    :return: Production rate in tons per hour
    """
    init_vol = width * thickness * length
    final_vol = frac_of_init_vol * init_vol
    # Area of cross-section of the finished product
    area = math.pi * ((diameter / 2) ** 2)
    final_length = final_vol / (frac_of_nominal_wt * area)
    # Time for one bar is calculated in hours
    time_for_one_bar = (time_gap + (final_length / velocity)) / 3600
    # Density is tons per cubic metre so prod_rate will be in tons per hour.
    wt_of_bar = frac_of_init_vol * density * width * thickness * length
    prod_rate = wt_of_bar / time_for_one_bar
    return prod_rate
"""
    return frac_of_init_vol * frac_of_nominal_wt * 3600 * density * width * thickness * length / (frac_of_init_vol * width * thickness * length + time_gap * math.pi * diameter * diameter * velocity * frac_of_nominal_wt)
"""