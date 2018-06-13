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



# Equations for Cylinder
# ======================
# ======================


def thicknessCylinderCircumStress(S, E, P, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    #check if thin cylinder equations are to be used or thick cylinders as per supplementary equations of ASME
    if (P <= 0.385*S*E):
        condn_P = True
        if (R is not None):
            t = (P*R)/(S*E-0.6*P)
            eqn_ref = "UG-27(1)"
        else:
            tc = (P*Ro)/(S*E+0.4*P)
            eqn_ref = "Appendix 1-1(1)"
    else:
        condn_P = False
        if (R is not None):
            t = R*(exp(P/(S*E))-1)
            eqn_ref = "Appendix 1-2(1)"
        else:
            t = Ro*(1-exp(-P/(S*E)))
            eqn_ref = "Appendix 1-2(1)"

    return t, condn_P, eqn_ref


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
        Ri = Ro - t

    if (t <= (Ri/2)):
        condn_t = True
        if (R is not None):
            P = (S*E*t)/(R+0.6*t)
            eqn_ref = "UG-27(1)"
        else:
            P = (S*E*t)/(Ro-0.4*t)
            eqn_ref = "Appendix 1-1(1)"
    else:
        condn_t = False
        if (R is not None):
            P = S*E*log((R+t)/R)
            eqn_ref = "Appendix 1-2(2)"
        else:
            P = S*E*log(Ro/(Ro-t))
            eqn_ref = "Appendix 1-2(2)"

    return P, condn_t, eqn_ref


def thicknessCylinderLongStress(S, E, P, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    #check if thin cylinder equations are to be used or thick cylinders as per supplementary equations of ASME
    if (P <= 1.25*S*E):
        condn_P = True
        if (R is not None):
            t = (P*R)/(2*S*E+0.4*P)
            eqn_ref = "UG-27(2)"
        else:
            t = (P*Ro)/(2*S*E+1.4*P)
            eqn_ref = "UG-27(2) [derived]"
    else:
        condn_P = False
        Z = (P/(S*E)) + 1
        if (R is not None):
            t = R*(sqrt(Z) - 1)
            eqn_ref = "Appendix 1-2(3)"
        else:
            t = Ro*(sqrt(Z)-1)/sqrt(Z)
            eqn_ref = "Appendix 1-2(3)"

    return t, condn_P, eqn_ref


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
        Ri = Ro - t

    if (t <= (Ri/2)):
        condn_t = True
        if (R is not None):
            P = (2*S*E*t)/(R-0.4*t)
            eqn_ref = "UG-27(2)"
        else:
            P = (2*S*E*t)/(Ro-1.4*t)
            eqn_ref = "UG-27(2) [derived]"
    else:
        condn_t = False
        if (R is not None):
            Z = ((R+t)/R)**2
        else:
            Z = (Ro/(Ro-t))**2

        P = S*E*(Z-1)
        eqn_ref = "Appendix 1-2(4)"

    return P, condn_t, eqn_ref

# Equations for Sphere
# ====================
# ====================

def thicknessSphere(S, E, P, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    #check if thin spherical equations are to be used or thick spherical  as per supplementary equations of ASME
    if (P <= 0.665*S*E):
        condn_Ps = True
        if (R is not None):
            ts = (P*R)/(2*S*E -0.2*P)
            eqn_ref = "UG-27(3)"
        else:
            ts = (P*Ro)/(2*S*E +0.8*P)
            eqn_ref = "Appendix 1-1(2)"
    else:
        condn_Ps = False
        if (R is not None):
            ts = R*(exp((0.5*P)/(S*E)) - 1)
            eqn_ref = "Appendix 1-3(1)"
        else:
            ts = Ro*(1 - exp((-0.5*P)/(S*E)))
            eqn_ref = "Appendix 1-3(1)"

    return ts, condn_Ps, eqn_ref

def pressureSphere(S, E, t, R=None, Ro=None):
    # check for invalid inputs for optional parameters R and Ro. Only one amongst these two must be provided
    if (R is None) and (Ro is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (R is not None) and (Ro is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    if (t <= 0.356*R):
        condn_ts = True
        if (R is not None):
            Ps = (2*S*E*t)/(R+0.2*t)
            eqn_ref = "UG-27(3)"
        else:
            Ps = (2*S*E*t)/(Ro-0.8*t)
            eqn_ref = "Appendix 1-1(2)"
    else:
        condn_ts = False

        if (R is not None):
            Ps = 2.0*S*E*log((R+t)/R)
            eqn_ref = "Appendix 1-3(2)"
        else:
            Ps = 2.0*S*E*log(Ro/(Ro-t))
            eqn_ref = "Appendix 1-3(2)"

    return Ps, condn_ts, eqn_ref


# Equations for Formed Head
# =========================
# =========================

def thicknessEllipsoidalHead(S, E, P, D=None, Do=None,  ar = 2):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    # evaluate the K factor
    K = (1/6)*(2 + ar**2)

    if (D is not None):
        t = (P*D*K)/(2*S*E - 0.2*P)
        eqn_ref = "Appendix 1-4(1)"
    else:
        t = (P*Do*K)/(2*S*E + 2*P*(K-0.1))
        eqn_ref = "Appendix 1-4(2)"

    return t, K, eqn_ref


def pressureEllipsoidalHead(S, E, t, D=None, Do=None, ar = 2):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    # evaluate the K factor
    K = (1/6)*(2 + ar**2)

    if (D is not None):
        P = (2*S*E*t)/(K*D + 0.2*t)
        eqn_ref = "Appendix 1-4(1)"
    else:
        P = (2*S*E*t)/(K*Do -2*t(K-0.1))
        eqn_ref = "Appendix 1-4(2)"

    return P, K, eqn_ref


def thicknessTorisphericalHead(S, E, P, Do, L, r):
    # check for validity of L and r
    if (L > Do):
        raise Exception("Inner crown radius (L) should not be greater than outer skirt diameter (Do)")
    if (r < 0.06*Do):
        raise Exception("Knuckle radius (r) should not be less than to 0.06Do")

    # evaluate the M factor
    M = (1/4)*(3 + sqrt(L/r))
    t = (P*L*M)/(2*S*E - 0.2*P)
    eqn_ref = "Appendix 1-4(3)"

    return t, M, eqn_ref


def pressureTorisphericalHead(S, E, t, Do, L, r ):
    # check for validity of L and r
    if (L > Do):
        raise Exception("Inner crown radius (L) should not be greater than outer skirt diameter (Do)")
    if (r < 0.06*Do):
        raise Exception("Knuckle radius (r) should not be less than to 0.06Do")

    # evaluate the M factor
    M = (1/4)*(3 + sqrt(L/r))
    P = (2*S*E*t)/(L*M + 0.2*t)
    eqn_ref = "Appendix 1-4(3)"

    return P, M, eqn_ref

def thicknessHemisphericalHead(S, E, P, D):
    R = D/2
    t, condn_P, eqn_ref = thicknessSphere(S, E, P, R)
    return t, condn_P, eqn_ref

def pressureHemisphericalHead(S, E, t, D):
    R = D/2
    MAWP, condn_t, eqn_ref = pressureSphere(S, E, t, R)
    return MAWP, condn_t, eqn_ref

def thicknessConicalHead(S, E, P, D=None, Do=None, alpha=30):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'R' or 'Ro' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'R' and 'Ro' should not be provided")

    #check the validity of alpha
    if (alpha > 30):
        raise Exception("Apex angle alpha exceeds 30 degrees")

    if (D is not None):
        t = (P*D)/(2*cos(alpha)*(S*E - 0.6*P))
        eqn_ref = "Appendix 1-4(5)"
    else:
        t = (P*Do)/(2*cos(alpha)*(S*E + 0.4*P))
        eqn_ref = "Appendix 1-4(5)"

    return t, eqn_ref

def pressureConicalHead(S, E, t, D=None, Do=None, alpha=30):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    if (D is None) and (Do is None):
        raise Exception("Invalid inputs. Either 'D' or 'Do' should be provided")
    if (D is not None) and (Do is not None):
        raise Exception("Invalid inputs. Both 'D' and 'Do' should not be provided")

    #check the validity of P
    if (alpha > 30):
        raise Exception("Apex angle alpha exceeds 30 degrees")

    if (D is not None):
        P = (2*S*E*t*cos(alpha))/(D + 1.2*t*cos(alpha))
        eqn_ref = "Appendix 1-4(5)"
    else:
        P = (2*S*E*t*cos(alpha))/(Do - 0.8*t*cos(alpha))
        eqn_ref = "Appendix 1-4(5)"

    return P, eqn_ref


def thicknessToriConicalHead(S, E, P, Do, tn, Di, r, alpha=30):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    # check for validity of L and r
    if (r < 0.06*Do):
        raise Exception("Knuckle radius (r) should not be less than  0.06Do")

    if (r < 3*tn):
        raise Exception("Knuckle radius (r) should not be less than three times knuckle thickness")

    #check the validity of alpha
    if (alpha > 30):
        raise Exception("Apex angle alpha exceeds 30 degrees")

    tcone, eqn_ref_cone = thicknessConicalHead(S, E, P, D=Di, alpha=alpha)
    L = Di/(2*cos(alpha))
    tknuckle,M, eqn_ref_knuckle = thicknessTorisphericalHead(S, E, P, Do, L, r)

    t = max([tcone,tknuckle])
    return t, tcone, eqn_ref_cone, tknuckle, L, M, eqn_ref_knuckle


def pressureToriConicalHead(S, E, t, Do, tn, Di, r, alpha=30):
    # check for invalid inputs for optional parameters D and Do. Only one amongst these two must be provided
    # check for validity of L and r
    if (r < 0.06*Do):
        raise Exception("Knuckle radius (r) should not be less than  0.06Do")

    if (r < 3*tn):
        raise Exception("Knuckle radius (r) should not be less than three times knuckle thickness")

    #check the validity of alpha
    if (alpha > 30):
        raise Exception("Apex angle alpha exceeds 30 degrees")

    Pcone, eqn_ref_cone = pressureConicalHead(S, E, t, D=Di, alpha=alpha)
    L = Di/(2*cos(alpha))
    Pknuckle, M, eqn_ref_knuckle = pressureTorisphericalHead(S, E, t, Do, L, r )
    P = min([Pcone,Pknuckle])

    return P, Pcone, eqn_ref_cone, Pknuckle, L, M, eqn_ref_knuckle
