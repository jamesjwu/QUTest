from Test import *

def foo():
	assert False
	return 0

test = Test(foo,[], output = 0, error = True)
print test.run()





test2 = Test(test.run, [], (True, 0, None), name = "")

print test2.run()