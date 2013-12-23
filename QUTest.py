"""
QUTest- Unit Tests made easy
"""
import time

#used for when the output is unknown
class Unknown(object):
	pass


"""Runs a single test"""
class Test(object):
	name = ""
	#expected inputs and outputs
	inputs = []
	output = None
	#the function itself
	fn = None
	#do we expect an assertion error?
	error = False

	def __init__(self, fn, inputs = [], output = Unknown, error = False, name = ""):
		"""
		fn: function in question
		inputs: required inputs for the function
		output: expected output
		error: whether or not this function should trigger an error
		name: name of function
		"""

		self.name = name
		if not self.name:
			self.name = fn.__name__
		self.inputs = inputs
		self.error = error
		if error:
			self.output = "Assertion Error"
		else:
			self.output = output
		self.fn = fn

	def time(self):
		start = time.clock()
		result = self.run()
		elapsed = time.clock() - start
		return (result, elapsed)

	def run(self):
		"""
		Returns a triplet, of type
		(bool, int, Object)
		True means passed, False means failed. 
		Error codes:
		0: Test Passed
		1: Unexpected AssertionError
		2: Expected AssertionError, code ran to completion
		3: Incorrect Output
		4: Unknown output, prints out
		"""
		
		try:
			testOutput = self.fn(*self.inputs)
		except AssertionError, e:
			if self.error:
				return (True, 0, None)

			return (False, 1 ,e)


		if self.error:
			return (False, 2, testOutput)

		if self.output is Unknown:
			return (True, 4, testOutput)

		if testOutput == self.output:
			return (True, 0, None)

		else:
			return (False, 3, testOutput)


"""
Creates a suite of large integer input tests.

"""
def largeIntTests(fn, maximum = 1000000000000, factor = 10): 

	i = 1
	suite = Suite("{0} Large Integer tests".format(fn.__name__))
	while i < maximum:
		suite.addTest(Test(fn, [i], name = "{0}({1})".format(fn.__name__, i)))
		if(factor == 1):
			i += 1
		else:
			i *= factor

	return suite


class Suite(object):
	"""
	A suite is a group of tests meant to be run together
	"""
	tests = []
	def __init__(self, name = "", tests= []):
		self.tests = tests
		self.name = name



	def addTest(self, test):
		assert type(test) == Test
		self.tests.append(test)
	

	def removeTest(self, test):
		self.tests.remove(test)


	def timeTests(self):
		self.runTests(timed = True)

	def runTestsSilent(self):
		"""
		Runs tests quietly, unless an error occurs
		"""
		errorCount = 0
		passed = 0

		for test in self.tests:
			result = test.run()
			if result[0]:
				passed += 1
			else:
				errorCount += 1
				#otherwise there's an error
				print "TEST FAILED"
				print "Expected ", test.output

				#assertion error
				if result[1] == 1:
					print "An assertion error occurred unexpectedly:"
					print result[2]

				#expected an assertion error	
				elif result[1] == 2:
					print "Expected an assertion to fail, but ran to completion"
					print "Output: ", result[2]

				else:
					assert result[1] == 3
					print "Incorrect output:", result[2]

				print "--------------------------"
		print "Tests passed: ", passed
		print "Tests failed: ", errorCount

	def runTests(self, timed= False):
		print "Running unit tests on suite", self.name
		print "--------------------------"
		errorCount = 0
		passed = 0

		for test in self.tests:
			print "Running", test.name
			print "Input: ", test.inputs
			if test.output is not Unknown:
				print "Expect:", test.output

			if timed:
				result, elapsed = test.time()
			else:
				result = test.run()
			if result[0]:
				passed += 1

				if result[1] == 4:
					print "Output:", result[2]

				print "TEST PASSED"

				if timed:
					print "Time Elapsed:", elapsed
				print "--------------------------"

			else:
				errorCount += 1
				#otherwise there's an error
				print "TEST FAILED"
				print "Expected ", test.output

				#assertion error
				if result[1] == 1:
					print "An assertion error occurred unexpectedly:"
					print result[2]

				#expected an assertion error	
				elif result[1] == 2:
					print "Expected an assertion to fail, but ran to completion"
					print "Output: ", result[2]

				else:
					assert result[1] == 3
					print "Incorrect output:", result[2]

				print "--------------------------"
		print "Tests passed: ", passed
		print "Tests failed: ", errorCount


	











	





