QUTest
======

A Simple Python Unit Testing Tool by James Wu

Version 1.0

Why QUTest?
-----------
I created QUTest as a practice project, in order to better understand unit testing and writing modules. QUTest also serves the purpose to the average python beginner as a very simple method of creating tests for code. The syntax of QUTest is simple to use, and may be a very simple alternative to the unittest module or pytest, if one is looking for an easy to use solution. Be aware that, at the cost of simplicity, the features in QUTest are much more limited than their professionally made counterparts.

What does QUTest stand for?
--------------------------
Despite sounding like "cutest", it actually is supposed to stand for "Quality Unit Tests". I'm not really picky either way.

Installation
------------
Simply download or clone QUTest.py, and then import QUTest. Change and run at your own will and risk(see license for more information). 


Creating Tests
--------------
A Test object is very simple to make:

```python
def __init__(self, fn, inputs = [], output = Unknown, error = False, name = ""):
		"""
		fn: function in question
		inputs: required inputs for the function
		output: expected output of the function
		error: whether or not this function should trigger an error
		name: name of function
		"""
```
If you do not specify an output, QUTest will assume the output is unknown(creating its own Unknown type as a filler), and simply print out the output upon running the test. 


An example usage would be:
```python
def foo(x):
	pass

mytest = Test(foo, [], output = None, error = False, name = "")
```


Running individual tests
------------------------
To run any individual test, simply call test.run(). The return value will be a tuple, with information as follows:
```python
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
```
For example, running a test on a function that returns the correct output will return:
```python
>>> workingfunctiontest.run()
(True, 0, None)
```
And running a test with an unknown output will return:
```python
>>> workingfunctiontest.run()
(True, 4, testOutput)
```

This information can be hard to parse, so if you want to simply print out testing results, the next section, suites, are for you.



Suites
------

Suites are collections of tests, as well as the way to print out test results. To create a Suite, simply call its constructor:
```
suite = Suite(name = "Suite name", tests = [])
```
calling Suite without a tests field will simply create an empty Suite. Then use Suite.addtest(test) to add any test to the suite.

Then, running the test suite is as simple as calling suite.runTests()

For example, the current version of testTest.py, which uses QUTest to test QUTest code itself, prints:

```
Running unit tests on suite QUTest
--------------------------
Running foo
Input:  []
Expect: Assertion Error
TEST PASSED
--------------------------
Running suite.addTest
Input:  [<QUTest.Test object at 0x105808450>]
Output: None
TEST PASSED
--------------------------
Running Improper input to suite.addTest
Input:  [5]
Expect: Assertion Error
TEST PASSED
--------------------------
Running Test.run()
Input:  []
Expect: (True, 0, None)
TEST PASSED
--------------------------
Tests passed:  4
Tests failed:  0
```

Other features
--------------

###Timing tests
Running Suite.timeTests() instead of runTests() will do performance testing, allowing you to see the time elapsed on your functions.

###Large Integer Tests
LargeIntTests is a simple method that creates a suite of tests that tests a function on larger and larger inputs.
```python
def largeIntTests(fn, maximum = 1000000000000, factor = 10): 
"""
Creates a suite of large integer input tests.
Maximum: Maximum size input
factor: Ratio of input sizes. If set to 1, inputs will increment by 1 each time
"""
```
Running largeIntTests to time an unmemoized fibonacci function, for example:

```python
def fib(x):
	if x == 0: return 1
	if x == 1: return 1
	return fib(x-1) + fib(x-2) 


t = largeIntTests(fib, maximum = 5, factor = 1)
t.timeTests()
```

Output:
```
Running unit tests on suite fib Large Integer tests
--------------------------
Running fib(1)
Input:  [1]
Output: 1
TEST PASSED
Time Elapsed: 4e-06
--------------------------
Running fib(2)
Input:  [2]
Output: 2
TEST PASSED
Time Elapsed: 2e-06
--------------------------
Running fib(3)
Input:  [3]
Output: 3
TEST PASSED
Time Elapsed: 4e-06
--------------------------
Running fib(4)
Input:  [4]
Output: 5
TEST PASSED
Time Elapsed: 7e-06
--------------------------
Running fib(5)
Input:  [5]
Output: 8
TEST PASSED
Time Elapsed: 9e-06
--------------------------
Tests passed:  5
Tests failed:  0
[Finished in 0.1s]
```

###Estimating Time Complexities 

QUTest can benchmark the big O time complexities of simple functions. For now, this means only functions with single integer inputs, but work is being done to facilitate list and other inputs. To run it, simply call
```python
def calcTimeComplexity(fn, maximum = 10000000000, factor = 10):
	"""
	Generates a list of largeIntTests, and uses them to figure out time complexity by timing
	
	Currently only works on functions with one argument, which is an int or float

	Maximum and factor are the same as arguments for largeIntTests

	"""
```

For example, running calcTimeComplexity of on a simple mergesort function(which has been altered to be tested with integer inputs representing length):
```python
def mergesort(L):
	if not L:
		return []
	if len(L) == 1:
		return L

	half = len(L)/2

	return merge(mergesort(L[:half]), mergesort(L[half:]))


def testmerge(x):
	L = [random.uniform(0, x) for i in xrange(x)] #does not effect bigO, since is only O(n)
	return mergesort(L)
```

yields:
```python
>>> print calcTimeComplexity(testmerge, maximum = 100, factor = 2)
O(nlg(n))
```

Note that currently, the build supports O(n), O(n^2), O(nlg(n)), O(lg(n)) and O(2^n) as estimates. A more robust format for calculating any time efficiency is in development.



Still in Progress
------------------

This module is still in development! I'm in the process of adding some of these features:

* Time complexity analyzer- more robust calculations
* Multitests - Running tests multiple times to check for consistency
* More robust suite test features - Things like concurrency tests, data structure invariants, etc should be handled sometime in the near future.

