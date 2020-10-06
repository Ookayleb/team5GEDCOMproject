import unittest
import sys
from caleb_unittest 	import *
from jared_unnitest 	import *
from william_tests 		import *
from seanJamesUnittests 	import *
from unittests 		import *
# from noe_unit_test 	import *

if __name__ == "__main__":
	# test_classes_to_run = [TestClassA, TestClassC]
	# loader = unittest.TestLoader()
	suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
	unittest.TextTestRunner(verbosity=3).run( suite )
