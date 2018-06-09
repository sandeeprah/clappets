from math import *
from copy import deepcopy
from clappets.units import treeUnitConvert, SI_UNITS
from clappets.utils import parseFloat, roundit
from techclappets.mechanical.static import pressurevessel as pv

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    R = None
    Ro = None
    D_basis = doc['input']['D_basis']['_val']
    if (D_basis=='inner'):
        D = parseFloat(doc['input']['D']['_val'])
        R = D/2
    elif(D_basis=='outer'):
        Do = parseFloat(doc['input']['Do']['_val'])
        Ro = Do/2
    else:
        doc[errors].append('Invalid value for "Shell Diameter given as"')

    L = parseFloat(doc['input']['L']['_val'])
    Pi = parseFloat(doc['input']['Pi']['_val'])
    Ti = parseFloat(doc['input']['Ti']['_val'])
    ca = parseFloat(doc['input']['ca']['_val'])
    E = parseFloat(doc['input']['E']['_val'])
    MOC = doc['input']['MOC']['_val']
    #S = parseFloat(doc['input']['S']['_val'])
    tn = parseFloat(doc['input']['tn']['_val'])

    # set the available thickness after deducting corrosion
    ta = tn - ca

    if (MOC=='Other'):
        S = parseFloat(doc['input']['S']['_val'])
    else:
        S = pv.getAllowableStress(MOC, Ti)

    # calculate R or Ro for results if not provided
    if (R is not None):
        R_calc = R
        Ro_calc = R + tn
    else:
        R_calc = Ro - tn
        Ro_calc = Ro

    # set the minimum required thickness as per UG-15
    tu = 1.5/1000

    # check whether the geometry is sphere or cylinder
    Shape = doc['input']['Shape']['_val']

    if (Shape=='cylindrical'):

        # Circumferential Stress Evaluation
        if (R is not None):
            tc, condn_Pc = pv.thicknessCylinderCircumStress(S, E, Pi, R)
            MAWPc, condn_tc = pv.pressureCylinderCircumStress(S, E, ta, R)
        else:
            tc, condn_Pc = pv.thicknessCylinderCircumStress(S, E, Pi, Ro)
            MAWPc, condn_tc = pv.pressureCylinderCircumStress(S, E, ta,Ro)

        # Longitudinal Stress Evaluation
        if (R is not None):
            tl, condn_Pl = pv.thicknessCylinderLongStress(S, E, Pi, R)
            MAWPl, condn_tl = pv.pressureCylinderLongStress(S, E, ta, R)
        else:
            tl, condn_Pl = pv.thicknessCylinderLongStress(S, E, Pi, Ro)
            MAWPl, condn_tl = pv.pressureCylinderLongStress(S, E, ta, Ro)

        # get the highest of the shell thickness determined as per circumferential analysis, longitudinal analysis and UG-15 requirement
        t = max([tu,tc,tl])

        # get the least of the MAWP from circumferential and longitudinal analysis to get governing MAWP
        MAWP = min([MAWPc,MAWPl])

        doc['result'].update({'condn_Pc':{'_val' : condn_Pc}})
        doc['result'].update({'tc':{'_val' : str(roundit(tc)), '_dim':'length'}})
        doc['result'].update({'condn_tc'  :{'_val' : condn_tc}})
        doc['result'].update({'MAWPc':{'_val' : str(roundit(MAWPc)), '_dim':'pressure'}})

        doc['result'].update({'condn_Pl':{'_val' : condn_Pl}})
        doc['result'].update({'tl':{'_val' : str(roundit(tl)), '_dim':'length'}})
        doc['result'].update({'condn_tl'  :{'_val' : condn_tl}})
        doc['result'].update({'MAWPl':{'_val' : str(roundit(MAWPl)), '_dim':'pressure'}})

    elif (Shape=='spherical'):
        # Spherical Stress Evaluation
        if (R is not None):
            ts, condn_Ps = pv.thicknessSphere(S, E, Pi, R)
            MAWPs, condn_ts = pv.pressureSphere(S, E, ta, R)
        else:
            ts, condn_Ps = pv.thicknessSphere(S, E, Pi, Ro)
            MAWPs, condn_ts = pv.pressureSphere(S, E, ta, Ro)

        # get the highest of the shell thickness determined as per circumferential analysis, longitudinal analysis and UG-15 requirement
        t = max([tu,ts])

        MAWP = MAWPs

        doc['result'].update({'condn_Ps':{'_val' : condn_Ps}})
        doc['result'].update({'ts':{'_val' : str(roundit(ts)), '_dim':'length'}})
        doc['result'].update({'condn_ts'  :{'_val' : condn_ts}})
        doc['result'].update({'MAWPs':{'_val' : str(roundit(MAWPs)), '_dim':'pressure'}})

    else:
        doc['errors'].append('Invalid Shape')



    # add the corrosion allowance to get minimum thickness requirement
    tr = t + ca


    if (tn >= tr):
        tn_adequate = "Yes"
    else:
        tn_adequate = "No"


    doc['result'].update({'R_calc':{'_val' : str(roundit(R_calc)), '_dim':'length'}})
    doc['result'].update({'Ro_calc':{'_val' : str(roundit(Ro_calc)), '_dim':'length'}})
    doc['result'].update({'S':{'_val' : str(roundit(S)), '_dim':'pressure'}})

    doc['result'].update({'ta':{'_val' : str(roundit(ta)), '_dim':'length'}})


    doc['result'].update({'tu':{'_val' : str(roundit(tu)), '_dim':'length'}})
    doc['result'].update({'t' :{'_val' : str(roundit(t)),  '_dim':'length'}})
    doc['result'].update({'tr':{'_val' : str(roundit(tr)), '_dim':'length'}})
    doc['result'].update({'MAWP' :{'_val' : str(roundit(MAWP)),  '_dim':'pressure'}})
    doc['result'].update({'tn_adequate':{'_val' : tn_adequate}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
