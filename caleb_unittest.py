import unittest
import sys
from script import validDate, calculateAge

class TestDateOrder(unittest.TestCase):
    def test_birthBeforeDeath(self):
        result = check_dateOrder("15 OCT 2020", "15 OCT 2021")
        self.assertTrue(result)

    def test_deathBeforeBirth(self):
        result = check_dateOrder("15 OCT 2020", "15 OCT 2019")
        self.assertFalse(result, "Earlier year failed")
        result = check_dateOrder("15 OCT 2020", "15 SEP 2020")
        self.assertFalse(result, "Earlier month failed")
        result = check_dateOrder("15 OCT 2020", "14 OCT 2020")
        self.assertFalse(result, "Earlier day failed")
        result = check_dateOrder("15 OCT 2020", "14 SEP 2019")
        self.assertFalse(result, "Earlier year, month, and day failed")


    def test_birthWithNoDeath(self):
        result = check_dateOrder("15 OCT 2020", "")
        self.assertTrue(result)

    def test_birthEqualsDeath(self):
        result = check_dateOrder("15 OCT 2020", "15 OCT 2020")
        self.assertTrue(result)

    def test_deathWithNoBirth(self):
        result = check_dateOrder("", "15 OCT 2021")
        self.assertFalse(result)



if __name__ == "__main__":
    # test_classes_to_run = [TestClassA, TestClassC]
    # loader = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
