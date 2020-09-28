import unittest
import sys
from script import validDate
from script import maleLastNames


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



if __name__ == "__main__":
    # test_classes_to_run = [TestClassA, TestClassC]
    # loader = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
