import unittest
import sys
from script import validDate
from script import birthBeforeMarriage, reset, generateInitialData

class TestDates(unittest.TestCase):
    def test_success(self):
        result = validDate("15 OCT 2019")
        self.assertTrue(result)
        result = validDate("27 SEP 2020")
        self.assertTrue(result)

    def test_fail(self):
        result = validDate("15 OCT 2020")
        self.assertFalse(result)
        result = validDate("28 SEP 2021")
        self.assertFalse(result)

    def test_input_fail(self):
        with self.assertRaises(ValueError): validDate("15")

class TestBirthBeforeMarriage(unittest.TestCase):
    def test_success(self):
        reset()
        gedcomStructuredData    = generateInitialData("gedFiles/0BirthAfterDeath.ged") #store the tables and lists into gedcomStructuredData
        famList_0warnings		= gedcomStructuredData['famList']
        result = birthBeforeMarriage(famList_0warnings)
        self.assertTrue(result)

    def test_fail(self):
        reset()
        gedcomStructuredData    = generateInitialData("gedFiles/2BirthAfterMarriage.ged") #store the tables and lists into gedcomStructuredData
        famList_2warnings		= gedcomStructuredData['famList']
        result = birthBeforeMarriage(famList_2warnings)
        self.assertFalse(result)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
