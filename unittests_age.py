import unittest
import sys
from script import validAge

class TestAge(unittest.TestCase):
    def test1(self):
        result = validAge(0)
        self.assertTrue(result)

    def test2(self):
        result = validAge(27)
        self.assertTrue(result)

    def test3(self):
        result = validAge(82)
        self.assertTrue(result)

    def test4(self):
        result = validAge(150)
        self.assertFalse(result)

    def test5(self):
        result = validAge(184)
        self.assertFalse(result)

    def test6(self):
        result = validAge(21345)
        self.assertFalse(result)

if __name__ == "__main__":
    # test_classes_to_run = [TestClassA, TestClassC]
    # loader = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
