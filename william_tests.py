import pandas as pd
import unittest
import sys
from datetime import datetime
import numpy as np
import ast

indi = pd.read_csv('indi.csv')
fam = pd.read_csv('fam.csv')
orderedP = []
datesM = []
datesD = []
datesDea = []

print(indi)
print(fam)

def to_format(lis, hus):
    if hus == True:
        name = 'Husband Name'
    else:
        name = 'Wife Name'
    for person in lis:
        orderedP.append(person)
        datesM.append(fam.loc[fam[name] == person]['Married'].tolist())
        datesD.append(fam.loc[fam[name] == person]['Divorced'].tolist())
        datesDea.append(indi.loc[indi['Name'] == person]['Death'].tolist())

child = indi['Child'].tolist()
spouse = indi['Spouse'].tolist()

to_format(fam['Husband Name'].tolist(), True)
to_format(fam['Wife Name'].tolist(), False)

def checkMarrNotDescOrSib(c, s):
    if not (isinstance(c, int) or isinstance(c, float) or isinstance(s, int) or isinstance(c, float)):
        raise ValueError("Error, wrong data format")
    if c == s:
        print("Error us17-18, married to sibling or child", str(c), str(s))
        return False
    else:
        return True

def dateBefore(mordd, deat_s):
    try:
        if mordd == 'nan':
            return True
        if deat_s == 'nan':
            return True
        else:
            marrdiv = datetime.strptime(mordd, "%d %b %Y").date()
            deat = datetime.strptime(deat_s, "%d %b %Y").date()
            if marrdiv >= deat:
                print("Error us05-06, marr/div before death",str(mordd), str(deat_s))
                return False
            if marrdiv < deat:
                return True
    except ValueError:
        raise ValueError("Error, incorrect data format, should be YYYY MM DD")

counter = 0

for person in orderedP:
    for date_ in datesD[counter]:
        print(dateBefore(str(date_),str(datesDea[counter][0])))
    for date_ in datesM[counter]:
        print(dateBefore(str(date_),str(datesDea[counter][0])))
    counter = counter + 1

for x in range(len(child)):
    checkMarrNotDescOrSib(child[x],spouse[x])

class Testing(unittest.TestCase):
    def test_success_date(self):
        result = dateBefore("5 JAN 2009","3 OCT 2010")
        self.assertTrue(result)
        result = dateBefore("3 AUG 1999","5 AUG 1999")
        self.assertTrue(result)

    def test_fail_date(self):
        result = dateBefore("3 OCT 2010","5 JAN 2009")
        self.assertFalse(result)
        result = dateBefore("5 AUG 1999","3 AUG 1999")
        self.assertFalse(result)

    def test_input_fail_date(self):
        with self.assertRaises(ValueError): dateBefore("Testing","444")

    def test_success_no_marr(self):
        result = checkMarrNotDescOrSib(5345234,42423)
        self.assertTrue(result)
        result = checkMarrNotDescOrSib(432234,42362)
        self.assertTrue(result)

    def test_fail_no_marr(self):
        result = checkMarrNotDescOrSib(432,432)
        self.assertFalse(result)
        result = checkMarrNotDescOrSib(5.3,5.3)
        self.assertFalse(result)

    def test_input_fail_no_marr(self):
        with self.assertRaises(ValueError): checkMarrNotDescOrSib("Testing","444")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )