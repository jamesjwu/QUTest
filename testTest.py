"""
Unit tests for Unit tester: 
Uses QUTest to test QUTest
"""
from QUTest import *

def foo():
	assert False
	return 0

def fib(x):
	y = 0
	for i in xrange(x**2):
		y += 1
	return y



test = Test(foo,[], output = 0, error = True,)
test2 = Test(test.run, [], (True, 0, None), name = "Test.run()")


s = Suite("QUTest", [test])

test3 = Test(s.addTest, [test2], error = False, name = "suite.addTest")

test4 = Test(s.addTest, [5], None, error = True, name = "Improper input to suite.addTest")


s.addTest(test3)
s.addTest(test4) 

test5 = Test(s.runTests, [], 0, error = False, name = "running tests")



print calcTimeComplexity(fib, maximum = 10000, factor = 10)
