import math


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