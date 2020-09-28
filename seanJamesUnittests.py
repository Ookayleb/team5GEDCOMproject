import unittest
import sys
import pandas
from script import validDate
from script import maleLastNames, generateInitialData

# xDF = pd.read_csv("indiDF_badlastname.csv")

gedcomeStructuredData = generateInitialData("gedFiles/badLastName.ged")


indiDF = 	gedcomeStructuredData['indiDF']
famDF = 	gedcomeStructuredData['famDF']
indiList = 	gedcomeStructuredData['indiList']
famList = 	gedcomeStructuredData['famList']

class TestDates(unittest.TestCase):
    def test_success(self):
        result = validDate("15 OCT 2019")
        self.assertTrue(result)
        result = validDate("27 SEP 2020")
        self.assertTrue(result)

    def test_fail(self):
        result = validDate("15 OCT 2020")
        self.assertFalse(result)
        result = validDate("28 SEP 2020")
        self.assertFalse(result)


    def test_input_fail(self):
        with self.assertRaises(ValueError): validDate("15")

class TestMaleLastNames(unittest.TestCase):
    def test_fail(self):
        result = maleLastNames(indiDF, famList, '1')
        self.assertFalse(result)
        result = maleLastNames.child
        self.assertFalse(result)

    def test_success(self):
        result = maleLastNames(indiDF, famList, 'Smith')
        self.assertTrue(result)
        result = maleLastNames(indiDF, famList, 'Terrace Smith')
        self.assertTrue(result)



if __name__ == "__main__":
    # test_classes_to_run = [TestClassA, TestClassC]
    # loader = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
