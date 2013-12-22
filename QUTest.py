"""
QUTest- Unit Tests made easy
"""



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

	def __init__(self, fn, inputs = [], output = None, error = False, name = ""):
		"""
		fn: function in question
		inputs: required inputs for the function
		output: expected output
		error: whether or not this function should trigger an error
		name: name of function
		"""
		self.name = name
		self.inputs = inputs
		self.error = error
		if error:
			self.output = "Assertion Error"
		else:
			self.output = output
		self.fn = fn

	
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
		"""
		
		try:
			testOutput = self.fn(*self.inputs)
		except AssertionError, e:
			if self.error:
				return (True, 0, None)

			return (False, 1 ,e)


		if self.error:
			return (False, 2, testOutput)

		if testOutput == self.output:
			return (True, 0, None)

		else:
			return (False, 3, testOutput)



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
		


	def runTests(self):
		print "Running unit tests on suite", self.name
		print "--------------------------"
		errorCount = 0
		passed = 0

		for test in self.tests:
			print "Running", test.name
			print "Input: ", test.inputs

			print "Expect:", test.output

			result = test.run()
			if result[0]:
				passed += 1
				print "test successful"
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


		return errorCount











	





