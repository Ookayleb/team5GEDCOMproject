import pandas as pd
import unittest
import sys
from datetime import datetime

def marr_b4_deat(marr_s, deat_s):
    try:
        marr = datetime.strptime(marr_s, "%d %b %Y").date()
        deat = datetime.strptime(deat_s, "%d %b %Y").date()
        if marr >= deat:
            return False
        if marr < deat:
            return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


class TestDeathAfterMarriage(unittest.TestCase):
    def test_success(self):
        result = marr_b4_deat("5 JAN 2009","3 OCT 2010")
        self.assertTrue(result)
        result = marr_b4_deat("3 AUG 1999","5 AUG 1999")
        self.assertTrue(result)

    def test_fail(self):
        result = marr_b4_deat("3 OCT 2010","5 JAN 2009")
        self.assertFalse(result)
        result = marr_b4_deat("5 AUG 1999","3 AUG 1999")
        self.assertFalse(result)


    def test_input_fail(self):
        with self.assertRaises(ValueError): marr_b4_deat("Testing","444")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
