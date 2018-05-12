from techclappets.electrical.ups.utils import getTd, getKt, readDischargeRate
from math import *

time = 1
cell_range = "M"
temperature = 0
Td = getTd(temperature, time, cell_range)
deration = (1/Td)
print("deration is {}".format(deration))

'''
AH_Rating = 460
time = 800
cell_range = "L"
Veod = 1.5
Kt = getKt(AH_Rating, time, cell_range, Veod)
print("Kt is {}".format(Kt))


data_file = 'L_Cell_1000mV_EOD.csv'
AH_Rating = 23
time = 350

A = readDischargeRate(data_file, AH_Rating, time)


try:
    A = readDischargeRate(data_file, AH_Rating, time)
except KeyError:
    raise Exception('Error occured while reading cell discharge rates. Ah rating not found in cell range selected.')
except TypeError:
    raise Exception('Error occured while reading cell discharge rates. Time used to obtain cell discharge rate outside defined range for the cell.')
except FileNotFoundError:
    raise Exception('Error occured while reading cell discharge rates. File for cell range selected could not be found. Check if correct cell range and cell End of Discharge values are used.')
except Exception as e:
    raise Exception('Error occured while reading cell discharge rates. ' + str(e))

print("A is {}".format(A))
'''
