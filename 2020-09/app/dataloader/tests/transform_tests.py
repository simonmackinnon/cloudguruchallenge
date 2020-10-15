import unittest
import sys
import pandas
sys.path.insert(0, '..')
from transform import (mergeCsvFiles)

testcasesvalid=[
	['test left and right ok', 'testData/00/left.csv', 'testData/00/right.csv', 'testData/00/expected.csv'],
	['test left and right one row overlap', 'testData/01/left.csv', 'testData/01/right.csv', 'testData/01/expected.csv'],
	['test left and right no overlap', 'testData/02/left.csv', 'testData/02/right.csv', 'testData/02/expected.csv']
]

class TestFunctions(unittest.TestCase):

	def test_mergeCsvFiles_LeftFilenameInvalid(self):
		with self.assertRaises(FileNotFoundError):
			mergedData = mergeCsvFiles('testData/02/dafdsfdsfds.csv', 'testData/02/right.csv')
			
	def test_mergeCsvFiles_RightFilenameInvalid(self):
		with self.assertRaises(FileNotFoundError):
			mergedData = mergeCsvFiles('testData/02/left.csv', 'testData/02/afdsjkfljs.csv')
	
	def test_mergeCsvFiles_NullFilenameCheck(self):
		with self.assertRaises(TypeError):
			mergedData = mergeCsvFiles(None, None)

def test_generator(usaCovidDataFilename, johnHopkinsDataFilename, expectedFilename):
	def test_mergeCsvData(self):
		expected = pandas.read_csv(expectedFilename) 
		mergedData = mergeCsvFiles(usaCovidDataFilename, johnHopkinsDataFilename)
		self.assertTrue(mergedData.empty or mergedData.equals(expected))
	return test_mergeCsvData 

if __name__ == '__main__':
	for case in testcasesvalid:
		test_name = 'test: %s' % case[0]
		test = test_generator(case[1], case[2], case[3])
		setattr(TestFunctions, test_name, test)
	unittest.main()