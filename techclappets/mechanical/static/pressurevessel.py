import json
import os
from math import *
import pandas as pd
from techclappets.utils import linarray_interp
from collections import OrderedDict

def getAllowableStress(materialSpec, T):
    data_file = "ASME_VIII_table_5A.csv"

    try:
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(THIS_FOLDER, data_file)
        stress_df = pd.read_csv(data_file_path)
        stress_df = stress_df.set_index('MatlSpec')
        matl_stress = stress_df.loc[materialSpec]
        matl_stress = matl_stress.drop(['St', 'Sy', 'Tmax', 'Chart'])
        temperature_values = matl_stress.index.tolist()
        stress_values = matl_stress.values

        for index, val  in enumerate(temperature_values):
            temperature_values[index] = float(val)

        # convert K to F
        T_C = T - 273.15
        S_MPa = linarray_interp(temperature_values,stress_values,T_C)
        S = S_MPa*1e6

    except Exception as e:
#        raise e
        raise Exception('S could not be determined')


    return S


def thicknessCylinderCircumStress(S, E, P, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    #check if thin cylinder equations are to be used or thick cylinders as per supplementary equations of ASME
    if (P <= 0.385*S*E):
        condn_Pc = True
        if (R is not None):
            tc = (P*R)/(S*E-0.6*P)
        else:
            tc = (P*Ro)/(S*E+0.4*P)
    else:
        condn_Pc = False
        if (R is not None):
            tc = R*(exp(P/(S*E))-1)
        else:
            tc = Ro*(1-exp(-P/(S*E)))


    return tc, condn_Pc


def pressureCylinderCircumStress(S, E, t, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    # Get the inner radius
    if (R is not None):
        Ri = R
    else:
        Ri = R - t

    if (t <= (Ri/2)):
        condn_tc = True
        if (R is not None):
            Pc = (S*E*t)/(R+0.6*t)
        else:
            Pc = (S*E*t)/(Ro-0.4*t)
    else:
        condn_tc = False
        if (R is not None):
            Pc = S*E*log((R+t)/R)
        else:
            Pc = S*E*log(Ro/(Ro-t))

    return Pc, condn_tc


def thicknessCylinderLongStress(S, E, P, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    #check if thin cylinder equations are to be used or thick cylinders as per supplementary equations of ASME
    if (P <= 1.25*S*E):
        condn_Pl = True
        if (R is not None):
            tl = (P*R)/(2*S*E+0.4*P)
        else:
            tl = (P*Ro)/(2*S*E+1.4*P)
    else:
        condn_Pl = False
        Z = (P/(S*E)) + 1
        if (R is not None):
            tl = R*(sqrt(Z) - 1)
        else:
            tl = Ro*(sqrt(Z)-1)/sqrt(Z)

    return tl, condn_Pl


def pressureCylinderLongStress(S, E, t, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    # Get the inner radius
    if (R is not None):
        Ri = R
    else:
        Ri = R - t

    if (t <= (Ri/2)):
        condn_tl = True
        if (R is not None):
            Pl = (2*S*E*t)/(R-0.4*t)
        else:
            Pl = (2*S*E*t)/(Ro-1.4*t)
    else:
        condn_tl = False

        if (R is not None):
            Z = ((R+t)/R)**2
        else:
            Z = (Ro/(Ro-t))**2

        Pl = S*E*(Z-1)

    return Pl, condn_tl
