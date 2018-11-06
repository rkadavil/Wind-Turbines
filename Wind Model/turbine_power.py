"""
Will compute the maximum available wind power in Watts, kW, or MW
"""
import numpy as np
from helpers import km_hr_to_m_s


def calc(d: float, rho: float, cp: float, v: float, scale: str=None):
    r"""

    :param d: Blade diameter in m
    :param rho: Air pressure in kg/m3
    :param cp: Coefficient of power
    :param v: Wind speed in km/hr
    :param scale: Power output units. String accepts w|W or kw|kW|KW or mw|MW
    :return pm_out: Mechanical power output of the wind turbine. Default unit is Watts
    """

    pm_out = (1/8)*(0.01*cp)*rho*np.pi*np.power(d, 2)*np.power((km_hr_to_m_s*v), 3)
    if scale in ['kw', 'kW', 'KW']:
        pm_out = pm_out*1e-3
    elif scale in ['mw', 'MW']:
        pm_out = pm_out*1e-6
    else:
        pass
    return pm_out


'''
a = calc(82, 1.19, 1, 12.6)
print(a)
'''
