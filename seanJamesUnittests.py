import unittest
import sys
import pandas
from script import maleLastNames, generateInitialData, reset, SiblingSpacing, uniqueID, uniqueNameAndBirthday, listRecentBirths, listUpcomingBirthdays


class TestMaleLastNames(unittest.TestCase):

    def test_Pass_femaleLastNameDiff(self):
        reset()

        #maleLastNamesEqFemaleDiff.ged
        #all males == one female !=
        gedcomeStructuredData2 = generateInitialData("gedFiles/maleLastNamesEqFemaleDiff.ged")
        indiDF_maleLastNamesEqFemaleDiff = 	gedcomeStructuredData2['indiDF']
        famList_maleLastNamesEqFemaleDiff = 	gedcomeStructuredData2['famList']

        result = maleLastNames(indiDF_maleLastNamesEqFemaleDiff, famList_maleLastNamesEqFemaleDiff)
        self.assertTrue(result)

    def test_Pass_femaleLastNameEq(self):
        reset()
        #allFemaleLastNamesEq
        #all the females have the same last name
        gedcomeStructuredData3 = generateInitialData("gedFiles/allFemaleLastNamesEq.ged")
        indiDF_allFemaleLastNamesEq = 	gedcomeStructuredData3['indiDF']
        famList_allFemaleLastNamesEq = 	gedcomeStructuredData3['famList']

        result = maleLastNames(indiDF_allFemaleLastNamesEq, famList_allFemaleLastNamesEq)
        self.assertTrue(result)

    def test_Fail_MaleLastNameDiff(self):
        reset()

        #badLastName.ged
        #one male child different last name
        gedcomeStructuredData1 = generateInitialData("gedFiles/badLastName.ged")
        indiDF_badLastName = 	gedcomeStructuredData1['indiDF']
        famList_badLastName = 	gedcomeStructuredData1['famList']

        result = maleLastNames(indiDF_badLastName, famList_badLastName)
        self.assertFalse(result)

    def test_Pass_DiffFamNameEq(self):
        reset()

        #maleLastNamesDiffFamsEq.ged
        # for different families there are different last names
        gedcomeStructuredData4 = generateInitialData("gedFiles/maleLastNamesDiffFamsEq.ged")
        indiDF_maleLastNamesDiffFamsEq = 	gedcomeStructuredData4['indiDF']
        famList_maleLastNamesDiffFamsEq = 	gedcomeStructuredData4['famList']


        result = maleLastNames(indiDF_maleLastNamesDiffFamsEq, famList_maleLastNamesDiffFamsEq)
        self.assertTrue(result)

    def test_Pass_MaleLastNameEq(self):
        reset()
        #Choy_familyTree.ged
        #All last names ==
        gedcomeStructuredData0 = generateInitialData("gedFiles/Choy_familyTree.ged")
        indiDF = 	gedcomeStructuredData0['indiDF']
        famList = 	gedcomeStructuredData0['famList']

        result = maleLastNames(indiDF, famList)
        self.assertTrue(result)

class TestSiblingSpacing(unittest.TestCase):

    def test_Pass_DiffYearMore8Months(self):
        reset()

        #diffYearMore8Months.ged
        # 3 kids in family with similiar birthdays
        gedcomeStructuredData6 = generateInitialData("gedFiles/diffYearMore8Months.ged")
        indiDF_diffYearMore8Months = 	gedcomeStructuredData6['indiDF']
        famList_diffYearMore8Months = 	gedcomeStructuredData6['famList']

        result = SiblingSpacing(indiDF_diffYearMore8Months, famList_diffYearMore8Months)
        self.assertTrue(result)
        self.assertIsNot(result, False)

    #below test should fail 
    def test_Pass_SameYearLess8Months(self):
        reset()

        #birthdaysnot8month3kids.ged
        # 3 kids in family with similiar birthdays
        gedcomeStructuredData5 = generateInitialData("gedFiles/birthdaysnot8month3kids.ged")
        indiDF_birthdaysnot8month3kids = 	gedcomeStructuredData5['indiDF']
        famList_birthdaysnot8month3kids = 	gedcomeStructuredData5['famList']

        result = SiblingSpacing(indiDF_birthdaysnot8month3kids, famList_birthdaysnot8month3kids)
        self.assertFalse(result)
    
    def test_Pass_SameYearMore8Months(self):
        reset()
        #Choy_familyTree.ged
        #All last names ==
        gedcomeStructuredData0 = generateInitialData("gedFiles/Choy_familyTree.ged")
        indiDF = 	gedcomeStructuredData0['indiDF']
        famList = 	gedcomeStructuredData0['famList']

        result = SiblingSpacing(indiDF, famList)
        self.assertTrue(result)
        self.assertIs(result, True)

    #below should be false
    def test_Pass_MoreThan2Kids(self):
        reset()

        #birthdaysnot8month3kids.ged
        # 3 kids in family with similiar birthdays
        gedcomeStructuredData5 = generateInitialData("gedFiles/birthdaysnot8month3kids.ged")
        indiDF_birthdaysnot8month3kids = 	gedcomeStructuredData5['indiDF']
        famList_birthdaysnot8month3kids = 	gedcomeStructuredData5['famList']

        result = SiblingSpacing(indiDF_birthdaysnot8month3kids,famList_birthdaysnot8month3kids )
        self.assertFalse(result)

class TestUniqueID(unittest.TestCase):
    def test_Pass_AllIDSUnique(self):
        reset()
        #Choy_familyTree.ged
        gedcomeStructuredData0 = generateInitialData("gedFiles/Choy_familyTree.ged")
        indiList = 	gedcomeStructuredData0['indiList']

        result = uniqueID(indiList)
        self.assertTrue(result)
        self.assertIs(result, True)
    
    def test_Fail_AllIDSUnique(self):
        reset()
        #Choy_familyTree.ged
        gedcomeStructuredData0 = generateInitialData("gedFiles/nonUniqueID.ged")
        indiList = 	gedcomeStructuredData0['indiList']

        result = uniqueID(indiList)
        self.assertFalse(result)
        self.assertIs(result, False)


class TestUniqueNameAndBday(unittest.TestCase):
    def test_Pass_AllNameAndBdaysUnique(self):
        reset()
        #Choy_familyTree.ged
        gedcomeStructuredData0 = generateInitialData("gedFiles/Choy_familyTree.ged")
        indiList = 	gedcomeStructuredData0['indiList']

        result = uniqueNameAndBirthday(indiList)
        self.assertTrue(result)
        self.assertIs(result, True)

    def test_Fail_AllNameAndBdaysUnique(self):
        reset()
        #Choy_familyTree.ged
        gedcomeStructuredData0 = generateInitialData("gedFiles/RepeatedNameAndBirthday.ged")
        indiList = 	gedcomeStructuredData0['indiList']

        result = uniqueNameAndBirthday(indiList)
        self.assertFalse(result)
        self.assertIs(result, False)    

class TestlistRecentBirths(unittest.TestCase):
    def test_Pass_listRecentBirths(self):
        reset()
        #birthdayOct27.ged
        gedcomeStructuredData0 = generateInitialData("gedFiles/birthdayOct27.ged")
        indiList = 	gedcomeStructuredData0['indiList']

        result = listRecentBirths(indiList)
        self.assertTrue(result)
        self.assertIs(result, True)

    def test_Fail_listRecentBirths(self):
        reset()
        #RepeatedNameAndBirthday.ged
        gedcomeStructuredData0 = generateInitialData("gedFiles/RepeatedNameAndBirthday.ged")
        indiList = 	gedcomeStructuredData0['indiList']

        result = listRecentBirths(indiList)
        self.assertFalse(result)
        self.assertIs(result, False) 

class TestlistUpcomingBirthdays(unittest.TestCase):
    def test_Pass_listUpcomingBirthdays(self):
        reset()
        #birthdayOct31.ged
        gedcomeStructuredData0 = generateInitialData("gedFiles/birthdayOct31.ged")
        indiList = 	gedcomeStructuredData0['indiList']

        result = listUpcomingBirthdays(indiList)
        self.assertTrue(result)
        self.assertIs(result, True)

    def test_Fail_listUpcomingBirthdays(self):
        reset()
        #RepeatedNameAndBirthday.ged
        gedcomeStructuredData0 = generateInitialData("gedFiles/RepeatedNameAndBirthday.ged")
        indiList = 	gedcomeStructuredData0['indiList']

        result = listUpcomingBirthdays(indiList)
        self.assertFalse(result)
        self.assertIs(result, False) 


if __name__ == "__main__":
    # test_classes_to_run = [TestClassA, TestClassC]
    # loader = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )

