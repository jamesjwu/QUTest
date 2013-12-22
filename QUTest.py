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
		self.output = output
		self.error = error
		self.fn = fn

	
	def run(self):
		"""
		Returns a triplet, True means passed, False means failed. 
		Error codes:
		0: Test Passed
		1: Unexpected AssertionError
		2: Expected AssertionError, code ran to completion
		3: Incorrect Output
		4: No Output Specified: Prints output
		"""
		
		try:
			testOutput = self.fn(*self.inputs)
		except AssertionError, e:
			if self.error:
				return (True, 0, None)

			return (False, 1 ,e)

		if self.output != None:
			if self.error:
				return (False, 2, None)

			if testOutput == self.output:
				return (True, 0, None)

			else:
				return (False, 3, testOutput)

		#Return the output
		return (True, 4, testOutput)





class QUTests(object):
	tests = []
	"""
	Main testing suite. Use to add Tests and run them accordingly
	"""

	





