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