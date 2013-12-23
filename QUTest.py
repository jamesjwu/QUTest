"""
QUTest- Unit Tests made easy
"""
import time, numpy, math
from scipy.stats import linregress

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
			self.output = "Give assertion error"
		else:
			self.output = output
		self.fn = fn


	def time(self):
		start = time.clock()
		result = self.run()
		elapsed = time.clock() - start
		return (result, elapsed)


	def avgtime(self, tries):
		"""
		Gives the average time elapsed for a certain number of Runs
		"""
		total = 0
		for i in xrange(tries):
			_, elapsed = self.time()
			total += elapsed

		return total / tries



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









def largeIntTests(fn, maximum = 1000000000000, factor = 10, start = 1000): 
	"""
	Creates a suite of large integer input tests.
	Maximum: Maximum size input
	factor: Ratio of input sizes. If set to 1, inputs will increment by 1 each time
	"""
	i = start
	suite = Suite("{0} Large Integer tests".format(fn.__name__))
	while i <= maximum:
		suite.addTest(Test(fn, [i], name = "{0}({1})".format(fn.__name__, i)))
		if(factor == 1):
			i += 1
		else:
			i *= factor

	return suite

##from stackoverflow
def keywithminval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())

     return k[v.index(min(v))]


def calcTimeComplexity(fn, maximum = 10000000000, factor = 10):
	"""
	Generates a list of largeIntTests, and uses them to figure out time complexity by timing
	
	Currently only works on functions with one argument, which is an int or float

	NOT EXACT: Only estimates based on linear, quadratic, cubic, exponential and logarithmic regression data
	"""
	testSuite = largeIntTests(fn, maximum, factor)
	inputs = []
	times = []
	#run average time elapsed on each test
	for test in testSuite.tests:
		assert len(test.inputs) == 1

		inputSize = test.inputs[0]
		inputs.append(inputSize)
		#number of times we average it by
		testTime = test.avgtime(100)
		times.append(testTime)
		print inputSize, ":", testTime


		assert len(inputs) == len(times)

	
	#Now we have our data. Let's calculate regressions

	##For Polynomial times
	stderrs = {}




	##linear
	#y = x
	
	slope, _, _, _, lin_stderr = linregress(inputs, times)
	
	if slope < .0000001:
		stderrs['constant'] = lin_stderr
	else:
		stderrs['lin'] = lin_stderr

	##squared
	#x = sqrt(y)
	sqrt_times = [math.sqrt(i) for i in times]
	_, _, _, _, sq_stderr = linregress(inputs, sqrt_times)
	stderrs['x^2'] = sq_stderr

	##logarithmic
	#y = log(x)
	log_inputs = [math.log(i, 2) for i in inputs]
	_, _, _, _, log_stderr = linregress(log_inputs, times)
	stderrs['log'] = log_stderr

	##exponential
	#log (y) = x
	log_times = [math.log(i, 2) for i in times]
	_, _, _, _, exp_stderr = linregress(inputs, log_times)
	stderrs['exp'] = exp_stderr

	print stderrs

	return keywithminval(stderrs)








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


	











	





