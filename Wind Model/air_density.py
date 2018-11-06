"""
Will calculate the air density based on temperature, pressure, and humidity
"""
import numpy as np


def calc(t: float, p: float, rh: float):
    r"""
    This function will return the air density using atmospheric conditional parameters

    :param t: Air temperature in deg. C
    :param p: Barometric Pressure in millibar
    :param rh: Relative Humidity in %
    :return rho: Air pressure in kg/m3
    """
    # Calculate Saturation Vapor Pressure (SVP)
    svp = 0.61121*np.exp((17.67*t)/(t+243.5))

    # Calculate Vapor Pressure (VP)
    vp = rh*svp*1e-2

    # Calculate mixing ratio (XM)
    xm = (0.622*vp)/((0.1*p) - vp)

    # Calculate air pressure (rho)
    return ((0.1*p)*(1 + xm))/(0.28703*(t+273.15)*(1+(1.16078*xm)))


'''
a = calc(-25, 1015, 30)
print('rho', a)
'''