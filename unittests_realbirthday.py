import unittest
import sys
from script import marriageAge

class TestAge(unittest.TestCase):
    def test1(self):
        #check_dateOrder(i.get('Birthday', None), i.get('Death', None)) == False
        result = childBirthday < wifeDeath
        self.assertTrue(result)

    def test2(self):
        result = '5 JAN 1950' < '19 AUG 1988'
        self.assertTrue(result)

    def test3(self):
        result = (childBirthday, wifeDeath)
        self.assertTrue(result)

    def test4(self):
        result = childBirthday > wifeDeath
        self.assertFalse(result)

    def test5(self):
        result = '5 JAN 1950' > '19 AUG 1988'
        self.assertFalse(result)

    def test6(self):
        result = (wifeDeath, childBirthday)
        self.assertTrue(result)

if __name__ == "__main__":
    # test_classes_to_run = [TestClassA, TestClassC]
    # loader = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
