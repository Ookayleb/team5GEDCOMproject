import pandas as pd
import unittest
import sys
from datetime import datetime
import numpy as np
import ast
from operator import itemgetter
import time

indi = pd.read_csv('indi.csv')
fam = pd.read_csv('fam.csv')
orderedP = []
datesM = []
datesD = []
datesDea = []
bdaysGroup = ['15 MAY','12 MAR','14 JAN']
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

def divTrue(al):
    if al == True:
        return True
    else:
        return False

def findDiv():
    rowDiv = []
    c = 0
    idCheck = []
    alDiv = []
    for x in fam['Divorced'].tolist():
        if str(x) == 'nan':
            pass
        else:
            rowDiv.append(c)
        c = c+1
    for x in rowDiv:
        idCheck.append(fam.loc[fam['Unnamed: 0'] == x]['Husband ID'])
        idCheck.append(fam.loc[fam['Unnamed: 0'] == x]['Wife ID'])
    for x in idCheck:
        if divTrue(indi.loc[indi['ID'] == x]['Alive']):
            alDiv.append(indi.loc[indi['ID'] == x]['Name'])
        
findDiv()

def same_bda(indi_in, grp_in):
    if grp_in == indi_in[:-4].strip():
        return True
    if grp_in != indi_in[:-4].strip():
        return False

def bdayGroupCh(b):
    ch_bd = indi['Birthday'].tolist()
    grab = []
    counter2 = 0
    for x in ch_bd:
        for y in b:
            if same_bda(x,y):
                grab.append(counter2)
        counter2 = counter2 + 1 
    print(grab)
    for x in grab: 
        print(indi.loc[indi['Unnamed: 0'] == x]['Name'])

bdayGroupCh(bdaysGroup)


def orderByAge(c):
    bdays = indi['Birthday'].tolist()
    names = indi['Name'].tolist()
    bday_timestamp = []
    for x in bdays:
        bday_timestamp.append(time.mktime(time.strptime(x, "%d %b %Y")))
    res = {names[i]: bday_timestamp[i] for i in range(len(names))}
    sort_orders = sorted(res.items(), key=lambda x: x[1], reverse=True)
    for i in sort_orders:
        if indi.loc[indi['Name'] == i[0]]['Child'].any():
	        print(i[0], indi.loc[indi['Name'] == i[0]]['Child'])

print("\nThe children with tags printed in order (US28): ")
orderByAge(child)

def listOrphans(c):
    res = []
    [res.append(x) for x in c if x not in res]
    tempCheck = []
    for x in res:
        tempCheck.append(indi.loc[indi['Spouse'] == x]['Alive'].tolist())
    print("\nOrphans (US33): ")
    checker = []
    counter = 0
    for x in tempCheck:
        if not x or True in x:
            checker.append(counter)
        counter = counter + 1
    for i in range(counter):
        if i not in checker:
            print(indi.loc[indi['Child'] == res[i]]['Name'].tolist(), '\n')


listOrphans(child)

#print(indi.loc[indi['Child'] == 515745826.0]['Birthday'].tolist())
#print(indi.loc[indi['Child'] == 515745826.0]['Name'].tolist())

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

    def test_success_born_same(self):
        result = same_bda('15 JAN 1931', '15 JAN')
        self.assertTrue(result)
        result = same_bda('1 APR 2000','1 APR')
        self.assertTrue(result)

    def test_fail_born_same(self):
        result = same_bda('5 JAN 1931', '15 JAN')
        self.assertFalse(result)
        result = same_bda('1 APR 2000','13 APR')
        self.assertFalse(result)

    def test_success_divTrue(self):
        result = divTrue(True)
        self.assertTrue(result)
    
    def test_fail_divTrue(self):
        result = divTrue(False)
        self.assertFalse(result)
        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )