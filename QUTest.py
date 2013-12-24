"""
QUTest Testing Module version 1.0
(c) James Wu 2013

QUTest is a simple unit testing framework for python. 
See readme for details.

"""
import time, numpy, math, gc
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

	def onlytime(self):
		start = time.clock()
		try: 
			self.fn(*self.inputs)
		except Exception as e:
			print "Exception!"
			return False


		elapsed = time.clock() - start
		return elapsed

	def avgtime(self, tries):
		"""
		Gives the average time elapsed for a certain number of Runs
		"""
		total = 0
		for i in xrange(tries):
			elapsed = self.onlytime()
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

		except Exception as e:
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









def largeIntTests(fn, maximum = 1000000000000, factor = 10, start = 1): 
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
def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())

     return k[v.index(max(v))]


def calcTimeComplexity(fn, maximum = 10000000000, factor = 10):
	"""
	Generates a list of largeIntTests, and uses them to figure out time complexity by timing
	
	Currently only works on functions with one argument, which is an int or float

	NOT EXACT: Only estimates based on linear, quadratic, cubic, exponential and logarithmic regression data
	"""
	fn(maximum)

	testSuite = largeIntTests(fn, maximum, factor, start = 1)


	data = []
	#run average time elapsed on each test
	for test in testSuite.tests:

		assert len(test.inputs) == 1

		inputSize = test.inputs[0]

		#number of times we average it by

		testTime = test.avgtime(100) * 10000

		data.append((inputSize, testTime))


	del testSuite.tests[:]
	rvals = {}
	
	#linear?
	slope, _, lin_rval, _, _ = linregress(data)

	rvals['n'] = lin_rval**2


	#quadratic?
	sq_data = [(x, math.sqrt(y)) for (x,y) in data]
	_, _, sq_rval, _, _ = linregress(sq_data)
	rvals['n^2'] = sq_rval**2
	del sq_data[:]

	#nlogn?
	nlgn_data = [(x*math.log(x,2), y) for (x,y) in data]
	_, _, nlgn_rval, _, _ = linregress(nlgn_data)
	rvals['nlg(n)'] = nlgn_rval**2
	del nlgn_data[:]

	
	#exp?
	exp_data = [(x, math.log(y, 2)) for (x,y) in data]
	_, _, exp_rval, _, _ = linregress(exp_data)	
	rvals['2^n'] = exp_rval**2
	del exp_data[:]

	#log?
	log_data = [(math.log(x, 2), y) for (x,y) in data]
	_, _, log_rval, _, _ = linregress(log_data)	
	rvals['lg(n)'] = log_rval**2


	return "O(" + keywithmaxval(rvals) + ")"
	








class Suite(object):
	"""
	A suite is a group of tests meant to be run together
	"""
	tests = []
	def __init__(self, name = "", tests= []):
		self.tests = tests
		self.name = name

	def __add__(self, other):

		return Suite(self.name + " and " + other.name, self.tests + other.tests)


	def __repr__(self):
		return self.name + str(self.tests)


	def testList(self):
		return self.tests

	def addTests(self, tests):
		"adds a list of tests to the suite"
		assert type(tests) == list
		self.tests += tests

	def addTest(self, test):
		"adds a single test to the Suite"
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
				print "TEST on function", test.fn.__name__, "FAILED"
				print "Input:",  test.inputs
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

		if errorCount:
			print "Tests failed: ", errorCount
		return errorCount

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


	
		return errorCount










	





