"""
Unit tests for Unit tester: 
Uses QUTest to test QUTest
"""
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
	L = [random.uniform(0, x) for i in xrange(x)]

	return mergesort(L)

def foo():
	assert False
	return 0

def fib(x):
	if x == 0: return 0
	
	return fib(x/2)

"""

test = Test(foo,[], output = 0, error = True,)
test2 = Test(test.run, [], (True, 0, None), name = "Test.run()")


s = Suite("QUTest", [test])

test3 = Test(s.addTest, [test2], error = False, name = "suite.addTest")

test4 = Test(s.addTest, [5], None, error = True, name = "Improper input to suite.addTest")


s.addTest(test3)
s.addTest(test4) 

test5 = Test(s.runTests, [], 0, error = False, name = "running tests")


"""
print calcTimeComplexity(testbinSearch, maximum = 1000, factor = 2)
