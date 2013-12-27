"""
QUTest Testing Module version 1.0
(c) James Wu 2013

QUTest is a simple unit testing framework for python. 
This is the set of unit tests for the module.

As a demonstration of QUTest, QUTest tests itself!
"""

##################################
# Helper demonstration functions #
##################################

import random
from QUTest import *

def merge(L1, L2):
	newList = []
	while (L1 and L2):
		if L1[0] < L2[0]:
			newList.append(L1[0])
			L1.remove(L1[0])
		else:
			newList.append(L2[0])
			L2.remove(L2[0])

	return newList + L1 + L2

def binSearch(L, x):
	"Performs binary search *correctly*"
	lo = 0
	hi = len(L) - 1

	while lo < hi:
		#loop invariant: 0 <= low <= mid <= hi
		mid = lo + (hi - lo)/2
		if L[mid] == x:
			return mid
		elif x < L[mid]:
			hi = mid
		else:
			lo = mid + 1

	return False

L = {}
for x in xrange(1000):
	L[x] = [random.uniform(0, x) for i in xrange(x)]

def testbinSearch(x):
	return binSearch(L[x], x/2)


def mergesort(L):
	if not L:
		return []
	if len(L) == 1:
		return L

	half = len(L)/2

	return merge(mergesort(L[:half]), mergesort(L[half:]))


def testmerge(x):
	return mergesort([random.uniform(0,x) for i in xrange(x)])

def foo(x):
	assert False
	return 0

def foo2(x):
	return 0

def fib(x):
	if x == 0: return 0
	
	return fib(x/2)





#################
#  Test Cases	#
#################





#Test the Test class
test1 = Test(foo, [1], error = True)
test2 = Test(mergesort, [[1,2,5,3,2]], [1,2,2,3,5], error = False, name = "mergesort test")
test3 = Test(test1.run, [], (True, 0, None), name = "run() test" )
test4 = Test(test2.run, [], (True, 0, None), name = "run() test 2")
test5 = Test(test1.time, [], Unknown, name = "timetest")

suite1 = Suite("test Tests", [test1, test2, test3, test4, test5])

#Test the Suite class
test5 = Test(suite1.runTestsSilent, [], 0, name = "runTestSilent() test")
test6 = Test(suite1.runTests, [], 0, name = "runTest() test")
test7 = Test(suite1.__add__, [suite1], Unknown, name = "Suite add test")
test8 = Test(suite1.__repr__, [], suite1.name + str(suite1.tests), name = "Suite repr test")
test9 = Test(suite1.testList, [], suite1.tests, name = "testList")
suite2 = Suite("Suite tests", [test5, test6, test7, test8, test9])


#Test calcTimeComplexity
fibtest = Test(calcTimeComplexity, [fib], output = "O(lg(n))")
footest = Test(calcTimeComplexity, [foo], error = True)
mergetest = Test(calcTimeComplexity, [testmerge, 300, 2], output = "O(nlg(n))")
bintest = Test(calcTimeComplexity, [testbinSearch, 300, 2], output = "O(lg(n))")

timecomplexitySuite = Suite("calcTimeComplexity", [fibtest,footest, mergetest, bintest])



#genTests test
test10 = Test(genTests, [foo2, [1],10, None], error = False, name = "foo2 generate testss")
test11 = Test(genTests, [mergesort,  [[1.0,4,5,4,3]], 15, sorted])


genTests(mergesort, [[1.0, 4,5,4,3]], 15, sorted)

fullSuite = Suite("Full Testing")
fullSuite += suite1
fullSuite += suite2
fullSuite += timecomplexitySuite

fullSuite.addTest(test10)
fullSuite.addTest(test11)

fullSuite.runTests()

