"""
Will replicate Optimal Power Tracking Logic and return
"""
import numpy as np
from helpers import *


def calc_opt(igspeed: float, iglmims: float, wr: float, tr: float, gr: float):
    r"""
    Optimal Power Tracking Calculator

    :param igspeed:
    :param iglmims:
    :param wr:
    :param tr:
    :param gr:
    :return:
    """
    # Limit the p.u. range between (0.01,100.0)
    igspeed = range_limit(igspeed, 100.0, 0.01)

    # Limit the p.u. range between (0.01,100.0)
    iglmims1 = range_limit(iglmims, 100.0, 0.01)

    # Limit the p.u. range between (0.0,1.0)
    iglmims2 = range_limit(iglmims, 1.0, 0.0)

    x = ((np.power(igspeed*(1/wr), 3)*(tr/gr))/igspeed)*tr
    y = iglmims1+(-0.5*iglmims2)+0.5    # Add a LPF of 1.0/(1+0.024s) to y
    return x, y


def regulate_f(ig_speed: float, ig_lmims: float, wr: float, tr: float, gr: float,
               ref_f: float, sys_f: float, droop: float):
    r"""
    Optimal Power Tracking Calculator

    :param ig_speed:
    :param ig_lmims:
    :param wr:
    :param tr:
    :param gr:
    :param ref_f:
    :param sys_f:
    :param droop:
    :return:
    """
    # Limit the p.u. range between [0.01,100.0]
    ig_speed = range_limit(ig_speed, 100.0, 0.01)

    # Limit the p.u. range between [0.01,100.0]
    ig_lmims1 = range_limit(ig_lmims, 100.0, 0.01)

    # Limit the p.u. range between [0.0,1.0]
    ig_lmims2 = range_limit(ig_lmims, 1.0, 0.0)

    # Frequency regulation
    del_f = (float(ref_f) - float(sys_f))*float(droop)*1e-2

    x = ((np.power(ig_speed*(1/wr), 3)*(tr/gr))/ig_speed)*tr
    y = ig_lmims1+(-0.5*ig_lmims2)+0.5    # Add a LPF of 1.0/(1+0.024s) to y
    return x, y, del_f


def droop_ctrl(ref_f: float, sys_f: float, droop: float, droopAct:int):    
    r"""
    Droop control

    :param ref_f:
    :param sys_f:
    :param droop:
    "param droopAct:
    :return:
    """

    # Frequency regulation
    del_f = (float(ref_f) - float(sys_f))*float(droop)*1e-2*droopAct

    # Limit the del_f range between [0.0,3.0]
    return range_limit(del_f, 3.0, 0.0)

    
    
    
