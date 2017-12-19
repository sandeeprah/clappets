# import the run_tests from relevant test module
from clappets.document.root.pro.cal.tch.flu.test  import run_tests
from clappets.units import roundit


a = 100000.2346789567
b = roundit(a)
print(b)


if __name__ == '__main__':
    pass
    #run_tests ()
