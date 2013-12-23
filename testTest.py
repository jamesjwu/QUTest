"""
Unit tests for Unit tester: 
Uses QUTest to test QUTest
"""
from QUTest import *

def foo():
	assert False
	return 0

def mathFunc(x):
	if x == 0: return 1
	if x == 1: return 1
	if x == 2: return 2
	return mathFunc(x-1) + mathFunc(x-2) + mathFunc(x-3)

test = Test(foo,[], output = 0, error = True,)
test2 = Test(test.run, [], (True, 0, None), name = "Test.run()")


s = Suite("QUTest", [test])

test3 = Test(s.addTest, [test2], error = False, name = "suite.addTest")

test4 = Test(s.addTest, [5], None, error = True, name = "Improper input to suite.addTest")


s.addTest(test3)
s.addTest(test4)

test5 = Test(s.runTests, [], 0, error = False, name = "running tests")

t = largeIntTests(mathFunc, maximum = 20, factor = 10)


t.timeTests()
