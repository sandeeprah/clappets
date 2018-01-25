from techclappets.thermochem.psychrometry import Pws, humidityratio

Piso = 101325
Tiso = 273+45
RHiso = 0

Psite = 101325
Tsite = 273 + 45
RHsite = 100

Xiso =  humidityratio(Tiso, Piso, RHiso)
print(Xiso)

Xsite =  humidityratio(Tsite, Psite, RHsite)
print(Xsite)


Pwiso =  Pws(Tiso)*(RHiso/100)
#print(Pwiso)

Pwsite =  Pws(Tsite)*(RHsite/100)
#print(Pwsite)


Runiversal = 8.314
MWair = 0.02897
MWwater = 0.018
Rair = Runiversal/MWair
Rwater = Runiversal/MWwater

Paiso = Piso - Pwiso
rhoda_iso = Paiso/(Rair*Tiso)
print(rhoda_iso)

Pasite = Psite - Pwsite
rhoda_site = Pasite/(Rair*Tsite)
print(rhoda_site)

print(rhoda_site/rhoda_iso)
print((Psite-Pwsite)/(Piso-Pwiso))
