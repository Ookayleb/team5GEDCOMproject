import unittest
import sys
import pandas
from script import maleLastNames, generateInitialData, reset, SiblingSpacing

#Choy_familyTree.ged
#All last names ==
gedcomeStructuredData0 = generateInitialData("gedFiles/Choy_familyTree.ged")
indiDF = 	gedcomeStructuredData0['indiDF']
famDF = 	gedcomeStructuredData0['famDF']
indiList = 	gedcomeStructuredData0['indiList']
famList = 	gedcomeStructuredData0['famList']

reset()

#badLastName.ged
#one male child different last name
gedcomeStructuredData1 = generateInitialData("gedFiles/badLastName.ged")
indiDF_badLastName = 	gedcomeStructuredData1['indiDF']
famDF_badLastName = 	gedcomeStructuredData1['famDF']
indiList_badLastName = 	gedcomeStructuredData1['indiList']
famList_badLastName = 	gedcomeStructuredData1['famList']

reset()


#maleLastNamesEqFemaleDiff.ged
#all males == one female !=
gedcomeStructuredData2 = generateInitialData("gedFiles/maleLastNamesEqFemaleDiff.ged")
indiDF_maleLastNamesEqFemaleDiff = 	gedcomeStructuredData2['indiDF']
famDF_maleLastNamesEqFemaleDiff = 	gedcomeStructuredData2['famDF']
indiList_maleLastNamesEqFemaleDiff = 	gedcomeStructuredData2['indiList']
famList_maleLastNamesEqFemaleDiff = 	gedcomeStructuredData2['famList']

reset()
#allFemaleLastNamesEq
#all the females have the same last name
gedcomeStructuredData3 = generateInitialData("gedFiles/allFemaleLastNamesEq.ged")
indiDF_allFemaleLastNamesEq = 	gedcomeStructuredData3['indiDF']
famDF_allFemaleLastNamesEq = 	gedcomeStructuredData3['famDF']
indiList_allFemaleLastNamesEq = 	gedcomeStructuredData3['indiList']
famList_allFemaleLastNamesEq = 	gedcomeStructuredData3['famList']

reset()

#maleLastNamesDiffFamsEq.ged
# for different families there are different last names
gedcomeStructuredData4 = generateInitialData("gedFiles/maleLastNamesDiffFamsEq.ged")
indiDF_maleLastNamesDiffFamsEq = 	gedcomeStructuredData4['indiDF']
famDF_maleLastNamesDiffFamsEq = 	gedcomeStructuredData4['famDF']
indiList_maleLastNamesDiffFamsEq = 	gedcomeStructuredData4['indiList']
famList_maleLastNamesDiffFamsEq = 	gedcomeStructuredData4['famList']

reset()

#LessThan8Months.ged
# contains a birthday of siblings less than 8 months apart
gedcomeStructuredData5 = generateInitialData("gedFiles/lessThan8Months.ged")
indiDF_lessThan8Months = 	gedcomeStructuredData5['indiDF']
famDF_lessThan8Months = 	gedcomeStructuredData5['famDF']
indiList_lessThan8Months = 	gedcomeStructuredData5['indiList']
famList_lessThan8Months = 	gedcomeStructuredData5['famList']

reset()

#LessThan2Days.ged
# contains a birthday of siblings less than 2 days apart
gedcomeStructuredData6 = generateInitialData("gedFiles/lessThan2Days.ged")
indiDF_lessThan2Days = 	gedcomeStructuredData6['indiDF']
famDF_lessThan2Days = 	gedcomeStructuredData6['famDF']
indiList_lessThan2Days = 	gedcomeStructuredData6['indiList']
famList_lessThan2Days = 	gedcomeStructuredData6['famList']

reset()

class TestMaleLastNames(unittest.TestCase):

    def test_Pass_femaleLastNameDiff(self):
        result = maleLastNames(indiDF_maleLastNamesEqFemaleDiff, famList_maleLastNamesEqFemaleDiff)
        self.assertTrue(result)

    def test_Pass_femaleLastNameEq(self):
        result = maleLastNames(indiDF_allFemaleLastNamesEq, famList_allFemaleLastNamesEq)
        self.assertTrue(result)

    def test_Fail_MaleLastNameDiff(self):
        result = maleLastNames(indiDF_badLastName, famList_badLastName)
        self.assertFalse(result)

    def test_Pass_DiffFamNameEq(self):
        result = maleLastNames(indiDF_maleLastNamesDiffFamsEq, famList_maleLastNamesDiffFamsEq)
        self.assertTrue(result)

    def test_Pass_MaleLastNameEq(self):
        result = maleLastNames(indiDF, famList)
        self.assertTrue(result)

class TestSiblingSpacing(unittest.TestCase):

    def test_Pass_DiffYearMore8Months(self):
        result = SiblingSpacing(indiDF, famList, indiList)
        self.assertTrue(result)
        self.assertIsNot(result, False)

    def test_Fail_SameYearLess8Months(self):
        result = SiblingSpacing(indiDF_lessThan8Months, famList_lessThan8Months, indiList_lessThan8Months)
        self.assertFalse(result)

    def test_Pass_SameYearMore8Months(self):
        result = SiblingSpacing(indiDF_maleLastNamesDiffFamsEq, famList_maleLastNamesDiffFamsEq, indiList_maleLastNamesDiffFamsEq)
        self.assertTrue(result)
        self.assertIs(result, True)

    def test_Pass_LessThan2Days(self):
        result = SiblingSpacing(indiDF_lessThan2Days, famList_lessThan2Days, indiList_lessThan2Days)
        self.assertTrue(result)






if __name__ == "__main__":
    # test_classes_to_run = [TestClassA, TestClassC]
    # loader = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
