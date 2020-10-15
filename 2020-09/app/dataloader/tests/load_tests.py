import unittest
import sys
sys.path.insert(0, '..')
from load import (validateDate, validateNumber)

testcases_datevalidate=[
	['validDate', '2020-2-13', True],
	['invalidDate', '2020-13-10', False],
	['invalidString', 'asdsdfgd', False],
	['noneInput', None, False]
]

testcases_numbervalidate=[
	['validNumber', '22222', True],
	['invalidDate', 22222, True],
	['invalidString', 'asdsdfgd', False],
	['noneInput', None, False]
]

class TestFunctionsDateValidate(unittest.TestCase):
	pass

class TestFunctionsNumberValidate(unittest.TestCase):
	pass

def test_generator_datevalidate(inputDate, expected):
	def test_validateDate(self):
		state = validateDate(inputDate)
		self.assertEqual(state, expected)
	return test_validateDate 
	
def test_generator_numbervalidate(inputNumber, expected):
	def test_validateNumber(self):
		state = validateNumber(inputNumber)
		self.assertEqual(state, expected)
	return test_validateNumber 

if __name__ == '__main__':
	for case in testcases_datevalidate:
		test_name = 'test: %s' % case[0]
		test = test_generator_datevalidate(case[1], case[2])
		setattr(TestFunctionsDateValidate, test_name, test)
		
	for case in testcases_numbervalidate:
		test_name = 'test: %s' % case[0]
		test = test_generator_numbervalidate(case[1], case[2])
		setattr(TestFunctionsNumberValidate, test_name, test)
		
	unittest.main()