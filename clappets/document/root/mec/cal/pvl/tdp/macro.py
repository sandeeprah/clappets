from math import *
from copy import deepcopy
from clappets.units import treeUnitConvert, SI_UNITS
from clappets.utils import parseFloat, roundit
from techclappets.mechanical.static import pressurevessel as pv

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    D = None
    R = None
    Ro = None
    Do = None

    tn = parseFloat(doc['input']['tn']['_val'])
    D_basis = doc['input']['D_basis']['_val']
    if (D_basis=='inner'):
        D = parseFloat(doc['input']['D']['_val'])
        R = D/2
        D_calc = D
        R_calc = R
        Do_calc = D+2*tn
        Ro_calc = Do_calc/2
    elif(D_basis=='outer'):
        Do = parseFloat(doc['input']['Do']['_val'])
        Ro = Do/2
        D_calc = Do - 2*tn
        R_calc = D_calc/2
        Do_calc = Do
        Ro_calc = Ro
    else:
        doc[errors].append('Invalid value for "Shell Diameter given as"')

    L = parseFloat(doc['input']['L']['_val'])
    Pi = parseFloat(doc['input']['Pi']['_val'])
    Ti = parseFloat(doc['input']['Ti']['_val'])
    ca = parseFloat(doc['input']['ca']['_val'])
    E = parseFloat(doc['input']['E']['_val'])
    MOC = doc['input']['MOC']['_val']
    #S = parseFloat(doc['input']['S']['_val'])

    # set the available thickness after deducting corrosion
    ta = tn - ca

    if (MOC=='Other'):
        S = parseFloat(doc['input']['S']['_val'])
    else:
        S = pv.getAllowableStress(MOC, Ti)


    # set the minimum required thickness as per UG-15
    tu = 1.5/1000

    # check whether the geometry is sphere or cylinder
    Shape = doc['input']['Shape']['_val']

    if (Shape=='cylindrical'):

        # Circumferential Stress Evaluation
        if (R is not None):
            tc, condn_Pc, eqn_reftc = pv.thicknessCylinderCircumStress(S, E, Pi, R)
            MAWPc, condn_tc, eqn_refpc = pv.pressureCylinderCircumStress(S, E, ta, R)
        else:
            tc, condn_Pc, eqn_reftc = pv.thicknessCylinderCircumStress(S, E, Pi, Ro)
            MAWPc, condn_tc, eqn_refpc = pv.pressureCylinderCircumStress(S, E, ta,Ro)

        # Longitudinal Stress Evaluation
        if (R is not None):
            tl, condn_Pl, eqn_reftl = pv.thicknessCylinderLongStress(S, E, Pi, R)
            MAWPl, condn_tl, eqn_refpl = pv.pressureCylinderLongStress(S, E, ta, R)
        else:
            tl, condn_Pl, eqn_reftl = pv.thicknessCylinderLongStress(S, E, Pi, Ro)
            MAWPl, condn_tl, eqn_refpl = pv.pressureCylinderLongStress(S, E, ta, Ro)

        doc['result'].update({'tc':{'_val' : str(roundit(tc)), '_dim':'length'}})
        doc['result'].update({'condn_Pc':{'_val' : condn_Pc}})
        doc['result'].update({'eqn_reftc':{'_val' : eqn_reftc}})

        doc['result'].update({'MAWPc':{'_val' : str(roundit(MAWPc)), '_dim':'pressure'}})
        doc['result'].update({'condn_tc'  :{'_val' : condn_tc}})
        doc['result'].update({'eqn_refpc':{'_val' : eqn_refpc}})

        doc['result'].update({'tl':{'_val' : str(roundit(tl)), '_dim':'length'}})
        doc['result'].update({'condn_Pl':{'_val' : condn_Pl}})
        doc['result'].update({'eqn_reftl':{'_val' : eqn_reftl}})

        doc['result'].update({'condn_tl'  :{'_val' : condn_tl}})
        doc['result'].update({'MAWPl':{'_val' : str(roundit(MAWPl)), '_dim':'pressure'}})
        doc['result'].update({'eqn_refpl':{'_val' : eqn_refpl}})

        # get the highest of the shell thickness determined as per circumferential analysis, longitudinal analysis and UG-15 requirement
        t = max([tu,tc,tl])
        # get the least of the MAWP from circumferential and longitudinal analysis to get governing MAWP
        MAWP = min([MAWPc,MAWPl])

        # carry out head evaluation
        Head1 = doc['input']['Head1']['_val']
        tn1 = parseFloat(doc['input']['tn1']['_val'])
        D1 = D_calc
        Do1 = D1 + 2*tn1
        R1 = D1/2
        Ro1 = Do1/2
        ta1 = tn1 - ca
        doc['result'].update({'D1':{'_val' : str(roundit(D1)), '_dim':'length'}})
        doc['result'].update({'Do1':{'_val' : str(roundit(Do1)), '_dim':'length'}})
        doc['result'].update({'ta1':{'_val' : str(roundit(ta1)), '_dim':'length'}})

        if (Head1=='ellipsoidal'):
            ar1 = parseFloat(doc['input']['ar1']['_val'])
            try:
                t1, K1, eqn_reft1 =  pv.thicknessEllipsoidalHead(S, E, P=Pi, D=D_calc, ar = ar1)
            except Exception as e:
                doc['errors'].append(str(e))

            try:
                MAWP1, K1, eqn_refp1 = pv.pressureEllipsoidalHead(S, E, t=ta1, D=D_calc, ar = ar1)
            except Exception as e:
                doc['errors'].append(str(e))

            doc['result'].update({'K1':{'_val' : str(roundit(K1))}})

        elif (Head1=='torispherical'):
            L1 = parseFloat(doc['input']['L1']['_val'])
            r1 = parseFloat(doc['input']['r1']['_val'])
            try:
                t1, M1, eqn_reft1 = pv.thicknessTorisphericalHead(S, E, P=Pi, Do=Do_calc, L=L1, r=r1)
            except Exception as e:
                doc['errors'].append(str(e))

            try:
                MAWP1, M1, eqn_refp1 = pv.pressureTorisphericalHead(S, E, t=ta1, Do=Do_calc, L=L1, r=r1)
            except Exception as e:
                doc['errors'].append(str(e))

            doc['result'].update({'M1':{'_val' : str(roundit(M1))}})

        elif (Head1=='hemispherical'):
            try:
                t1, condn_P1, eqn_reft1 =  pv.thicknessSphere(S, E, P=Pi, R=R1)
            except Exception as e:
                doc['errors'].append(str(e))

            try:
                MAWP1, condn_t1, eqn_refp1 = pv.pressureSphere(S, E, t=ta1, R=R1)
            except Exception as e:
                doc['errors'].append(str(e))

            doc['result'].update({'condn_P1':{'_val' : condn_P1}})
            doc['result'].update({'condn_t1':{'_val' : condn_t1}})

        elif (Head1=='conical'):
            alpha1 = parseFloat(doc['input']['alpha1']['_val'])

            try:
                t1, eqn_reft1 = pv.thicknessConicalHead(S, E,   P=Pi, D=D1, alpha=alpha1)
            except Exception as e:
                raise (e)
                doc['errors'].append(str(e))

            try:
                MAWP1, eqn_refp1 = pv.pressureConicalHead(S, E, t=ta1, D=D1, alpha=alpha1)
            except Exception as e:
                doc['errors'].append(str(e))

        elif (Head1=='toriconical'):
            r1 = parseFloat(doc['input']['r1']['_val'])
            alpha1 = parseFloat(doc['input']['alpha1']['_val'])
            Di1 = D1 - 2*r1*(1-cos(alpha1))
            t1, tcone1, eqn_ref_conet1, tknuckle1, L1, M1, eqn_ref_knucklet1 =  pv.thicknessToriConicalHead(S, E, P=Pi, Do=Do_calc, tn=tn1, Di=Di1, r=r1, alpha=alpha1)
            MAWP1, Pcone1, eqn_ref_coneP1, Pknuckle1, L1, M1, eqn_ref_knuckleP1 = pv.pressureToriConicalHead(S, E, t=ta1, Do=Do_calc, tn=tn1, Di=Di1, r=r1, alpha=alpha1)
            # L & M are common for both equations as they depend on common variables
            eqn_reft1 = ""
            eqn_refp1 = ""

            doc['result'].update({'Di1':{'_val' : str(roundit(Di1)), '_dim':'length'}})
            doc['result'].update({'L1':{'_val' : str(roundit(L1)), '_dim':'length'}})
            doc['result'].update({'M1':{'_val' : str(roundit(M1))}})

            doc['result'].update({'tcone1':{'_val' : str(roundit(tcone1)), '_dim':'length'}})
            doc['result'].update({'eqn_ref_conet1':{'_val' : eqn_ref_conet1}})
            doc['result'].update({'tknuckle1':{'_val' : str(roundit(tknuckle1)), '_dim':'length'}})
            doc['result'].update({'eqn_ref_knucklet1':{'_val' : eqn_ref_knucklet1}})

            doc['result'].update({'Pcone1':{'_val' : str(roundit(Pcone1)), '_dim':'pressure'}})
            doc['result'].update({'eqn_ref_coneP1':{'_val' : eqn_ref_coneP1}})
            doc['result'].update({'Pknuckle1':{'_val' : str(roundit(Pknuckle1)), '_dim':'pressure'}})
            doc['result'].update({'eqn_ref_knuckleP1':{'_val' : eqn_ref_knuckleP1}})

        else:
            doc['errors'].append('Invalid input for Head - Side 1')

        tr1 = t1 + ca
        if (tn1>=tr1):
            tn1_adequate = "Yes"
        else:
            tn1_adequate = "No"


        doc['result'].update({'t1':{'_val' : str(roundit(t1)), '_dim':'length'}})
        doc['result'].update({'eqn_reft1':{'_val' : eqn_reft1}})
        doc['result'].update({'tr1':{'_val' : str(roundit(tr1)), '_dim':'length'}})
        doc['result'].update({'tn1_adequate':{'_val' : tn1_adequate}})
        doc['result'].update({'MAWP1':{'_val' : str(roundit(MAWP1)), '_dim':'pressure'}})
        doc['result'].update({'eqn_refp1':{'_val' : eqn_refp1}})


        Head2 = doc['input']['Head2']['_val']
        tn2 = parseFloat(doc['input']['tn2']['_val'])
        D2 = D_calc
        Do2 = D2 + 2*tn2
        R2 = D2/2
        Ro2 = Do2/2
        ta2 = tn2 - ca
        doc['result'].update({'D2':{'_val' : str(roundit(D2)), '_dim':'length'}})
        doc['result'].update({'Do2':{'_val' : str(roundit(Do2)), '_dim':'length'}})
        doc['result'].update({'ta2':{'_val' : str(roundit(ta2)), '_dim':'length'}})

        t2 = nan
        K2 = nan
        L2 = nan
        M2 = nan
        Di2 = nan
        tcone2 = nan
        tknuckle2 = nan
        Pcone2 = nan
        Pknuckle2 = nan
        MAWP2 = nan
        condn_t2 = ""
        condn_P2 = ""
        eqn_reft2 = ""
        eqn_refp2 = ""
        eqn_ref_conet2 = ""
        eqn_ref_knucklet2 = ""
        eqn_ref_coneP2 = ""
        eqn_ref_knuckleP2 = ""



        if (Head2=='ellipsoidal'):
            ar2 = parseFloat(doc['input']['ar2']['_val'])
            try:
                t2, K2, eqn_reft2 =  pv.thicknessEllipsoidalHead(S, E, P=Pi, D=D2, ar = ar2)
            except Exception as e:
                doc['errors'].append(str(e))

            try:
                MAWP2, K2, eqn_refp2 = pv.pressureEllipsoidalHead(S, E, t=ta1, D=D2, ar = ar2)
            except Exception as e:
                doc['errors'].append(str(e))

            doc['result'].update({'K2':{'_val' : str(roundit(K2))}})

        elif (Head2=='torispherical'):
            L2 = parseFloat(doc['input']['L2']['_val'])
            r2 = parseFloat(doc['input']['r2']['_val'])
            try:
                t2, M2, eqn_reft2 = pv.thicknessTorisphericalHead(S, E, P=Pi, Do=Do2, L=L2, r=r2)
            except Exception as e:
                doc['errors'].append(str(e))

            try:
                MAWP2, M2, eqn_refp2 = pv.pressureTorisphericalHead(S, E, t=ta2, Do=Do2, L=L2, r=r2)
            except Exception as e:
                doc['errors'].append(str(e))

            doc['result'].update({'M2':{'_val' : str(roundit(M2))}})

        elif (Head2=='hemispherical'):
            try:
                t2, condn_P2, eqn_reft2 =  pv.thicknessSphere(S, E, P=Pi, R=R2)
            except Exception as e:
                doc['errors'].append(str(e))

            try:
                MAWP2, condn_t2, eqn_refp2 = pv.pressureSphere(S, E, t=ta2, R=R2)
            except Exception as e:
                doc['errors'].append(str(e))

            doc['result'].update({'condn_P2':{'_val' : condn_P2}})
            doc['result'].update({'condn_t2':{'_val' : condn_t2}})

        elif (Head2=='conical'):
            alpha2 = parseFloat(doc['input']['alpha2']['_val'])

            try:
                t2, eqn_reft2 = pv.thicknessConicalHead(S, E,   P=Pi, D=D2, alpha=alpha2)
            except Exception as e:
                doc['errors'].append(str(e))

            try:
                MAWP2, eqn_refp2 = pv.pressureConicalHead(S, E, t=ta2, D=D2, alpha=alpha2)
            except Exception as e:
                doc['errors'].append(str(e))

        elif (Head2=='toriconical'):
            r2 = parseFloat(doc['input']['r2']['_val'])
            alpha2 = parseFloat(doc['input']['alpha2']['_val'])
            Di2 = D2 - 2*r2*(1-cos(alpha2))

            try:
                t2, tcone2, eqn_ref_conet2, tknuckle2, L2, M2, eqn_ref_knucklet2 =  pv.thicknessToriConicalHead(S, E, P=Pi, Do=Do2, tn=tn2, Di=Di2, r=r2, alpha=alpha2)
            except Exception as e:
                doc['errors'].append(str(e))

            try:
                MAWP2, Pcone2, eqn_ref_coneP2, Pknuckle2, L2, M2, eqn_ref_knuckleP2 = pv.pressureToriConicalHead(S, E, t=ta2, Do=Do2, tn=tn2, Di=Di2, r=r2, alpha=alpha2)
            except Exception as e:
                doc['errors'].append(str(e))

            # L & M are common for both equations as they depend on common variables
            eqn_reft2 = ""
            eqn_refp2 = ""

            doc['result'].update({'Di2':{'_val' : str(roundit(Di2)), '_dim':'length'}})
            doc['result'].update({'L2':{'_val' : str(roundit(L2)), '_dim':'length'}})
            doc['result'].update({'M2':{'_val' : str(roundit(M2))}})

            doc['result'].update({'tcone2':{'_val' : str(roundit(tcone2)), '_dim':'length'}})
            doc['result'].update({'eqn_ref_conet2':{'_val' : eqn_ref_conet2}})
            doc['result'].update({'tknuckle2':{'_val' : str(roundit(tknuckle2)), '_dim':'length'}})
            doc['result'].update({'eqn_ref_knucklet2':{'_val' : eqn_ref_knucklet2}})

            doc['result'].update({'Pcone2':{'_val' : str(roundit(Pcone2)), '_dim':'pressure'}})
            doc['result'].update({'eqn_ref_coneP2':{'_val' : eqn_ref_coneP2}})
            doc['result'].update({'Pknuckle2':{'_val' : str(roundit(Pknuckle2)), '_dim':'pressure'}})
            doc['result'].update({'eqn_ref_knuckleP2':{'_val' : eqn_ref_knuckleP2}})

        else:
            doc['errors'].append('Invalid input for Head - Side 1')

        tr2 = t2 + ca
        if (tn2>=tr2):
            tn2_adequate = "Yes"
        else:
            tn2_adequate = "No"


        doc['result'].update({'t2':{'_val' : str(roundit(t2)), '_dim':'length'}})
        doc['result'].update({'eqn_reft2':{'_val' : eqn_reft2}})
        doc['result'].update({'tr2':{'_val' : str(roundit(tr2)), '_dim':'length'}})
        doc['result'].update({'tn2_adequate':{'_val' : tn2_adequate}})
        doc['result'].update({'MAWP2':{'_val' : str(roundit(MAWP2)), '_dim':'pressure'}})
        doc['result'].update({'eqn_refp2':{'_val' : eqn_refp2}})


    elif (Shape=='spherical'):
        # Spherical Stress Evaluation
        if (R is not None):
            ts, condn_Ps, eqn_refts = pv.thicknessSphere(S, E, Pi, R)
            MAWPs, condn_ts, eqn_refps = pv.pressureSphere(S, E, ta, R)
        else:
            ts, condn_Ps, eqn_refts = pv.thicknessSphere(S, E, Pi, Ro)
            MAWPs, condn_ts, eqn_refps = pv.pressureSphere(S, E, ta, Ro)

        # get the highest of the shell thickness determined as per circumferential analysis, longitudinal analysis and UG-15 requirement
        t = max([tu,ts])

        MAWP = MAWPs

        doc['result'].update({'ts':{'_val' : str(roundit(ts)), '_dim':'length'}})
        doc['result'].update({'condn_Ps':{'_val' : condn_Ps}})
        doc['result'].update({'eqn_refts':{'_val' : eqn_refts}})
        doc['result'].update({'MAWPs':{'_val' : str(roundit(MAWPs)), '_dim':'pressure'}})
        doc['result'].update({'condn_ts'  :{'_val' : condn_ts}})
        doc['result'].update({'eqn_refps':{'_val' : eqn_refps}})

    else:
        doc['errors'].append('Invalid Shape')



    # add the corrosion allowance to get minimum thickness requirement
    tr = t + ca
    if (tn >= tr):
        tn_adequate = "Yes"
    else:
        tn_adequate = "No"

    doc['result'].update({'D_calc':{'_val' : str(roundit(D_calc)), '_dim':'length'}})
    doc['result'].update({'R_calc':{'_val' : str(roundit(R_calc)), '_dim':'length'}})
    doc['result'].update({'Do_calc':{'_val' : str(roundit(Do_calc)), '_dim':'length'}})
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
