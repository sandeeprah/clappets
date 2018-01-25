from math import pow, log10
import os
import pandas as pd
from clappets.units import unitConvert

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def pump_types():
    pass

def pump_sizes(pump_type):
    pass

def pump_dimensions(pump_size):
    pass


def viscCorr(Qbep, Hbep, nu, N, Qratio):
    _Qbep = Qbep*3600
    _Hbep = Hbep
    _nu = unitConvert(nu,'kinViscosity', 'm2/s','cSt')
    _N = N

    B = 16.5*(pow(_nu,0.5)*pow(_Hbep, 0.0625))/(pow(_Qbep, 0.375)*pow(_N,0.25))

    if (B <= 1):
        Cq = 1
        Ch = 1
        Ceta = 1
    elif(B> 1 and B < 40):
        f = log10(B)
        k = -0.165*pow(f, 3.15)
        Cq = pow(2.71, k)
        Cbep_h = Cq
        Ch = 1 - (1-Cbep_h)*pow(Qratio, 0.75)
        a = -0.0547*pow(B, 0.69)
        Ceta = pow(B,a)
    else:
        raise Exception('Outside Correction Range')

    return Cq, Ch, Ceta


def viscSel(Qvis, Hvis, nu):
    _Qvis = Qvis*3600
    _Hvis = Hvis
    _nu = unitConvert(nu,'kinViscosity', 'm2/s','cSt')

    B = 2.80*(pow(_nu,0.5)/(pow(_Qvis, 0.25)*pow(_Hvis, 0.125)))
    print('B')
    print(B)

    if (B <= 1):
        Cq = 1
        Ch = 1
        Ceta = 1
    elif(B> 1 and B < 40):
        f = log10(B)
        k = -0.165*pow(f, 3.15)
        Cq = pow(2.71, k)
        Ch = Cq

        a = -0.0547*pow(B, 0.69)
        Ceta = pow(B,a)
    else:
        raise Exception('Outside Correction Range')

    return Cq, Ch, Ceta
