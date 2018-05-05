
from techclappets.mechanical.utils.psychrometrics import Pw_sat
T = 100
Pws = Pw_sat(273.15+T)
print(Pws/1000)
