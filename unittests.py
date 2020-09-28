import unittest
import sys
from script import validDate
<<<<<<< HEAD

=======
>>>>>>> Changed date on TestDates fail test case. Generated .gitignore file from gitignore.io

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

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
