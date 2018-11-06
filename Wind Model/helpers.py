"""
Constants used for conversion are defined here
"""


km_per_hr_to_mph = 0.6213

km_hr_to_m_s = 0.2778

rpm_to_rad_per_sec = 0.104719755


def range_limit(val: float, up: float, low: float):
    r"""

    :param val:
    :param up:
    :param low:
    :return:
    """
    if val > up:
        val = up
    elif val < low:
        val = low
    else:
        pass

    return val

def rate_limit(newVal: float, oldVal: float, rateLim: float, timestep: float=9e-4):
    r"""

    :param newVal:
    :param oldVal:
    :param timestep:
    :param rateLim:
    :return:
    """
    if (newVal - oldVal)/timestep > rateLim:
        newVal = oldVal + (rateLim*timestep)
        
    elif (newVal - oldVal)/timestep < rateLim:
        newVal = oldVal - (rateLim*timestep)        
    else:
        pass
    
'''
a = range_limit(-1, 100.0, 0.01)
print(a)
'''
