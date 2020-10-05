import pandas as pd
import unittest
import sys
from datetime import datetime
import numpy as np

indi = pd.read_csv('indi.csv')
fam = pd.read_csv('fam.csv')

print(fam)
print(indi)

orderedP = []
datesM = []
datesD = []
datesDea = []

for person in fam['Husband Name'].tolist():
    orderedP.append(person)
    datesM.append(fam.loc[fam['Husband Name'] == person]['Married'].tolist())
    datesD.append(fam.loc[fam['Husband Name'] == person]['Divorced'].tolist())
    datesDea.append(indi.loc[indi['Name'] == person]['Death'].tolist())

for person in fam['Wife Name'].tolist():
    orderedP.append(person)
    datesM.append(fam.loc[fam['Wife Name'] == person]['Married'].tolist())
    datesD.append(fam.loc[fam['Wife Name'] == person]['Divorced'].tolist())
    datesDea.append(indi.loc[indi['Name'] == person]['Death'].tolist())

print(orderedP)
print(datesM)
print(datesD)
print(datesDea[0][0])

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
                return False
            if marrdiv < deat:
                return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY MM DD")

counter = 0

for person in orderedP:
    for date_ in datesD[counter]:
        print(dateBefore(str(date_),str(datesDea[counter][0])))
    for date_ in datesM[counter]:
        print(dateBefore(str(date_),str(datesDea[counter][0])))
    counter = counter + 1

class TestDeathAfterMarriageorDiv(unittest.TestCase):
    def test_success(self):
        result = dateBefore("5 JAN 2009","3 OCT 2010")
        self.assertTrue(result)
        result = dateBefore("3 AUG 1999","5 AUG 1999")
        self.assertTrue(result)

    def test_fail(self):
        result = dateBefore("3 OCT 2010","5 JAN 2009")
        self.assertFalse(result)
        result = dateBefore("5 AUG 1999","3 AUG 1999")
        self.assertFalse(result)


    def test_input_fail(self):
        with self.assertRaises(ValueError): dateBefore("Testing","444")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
