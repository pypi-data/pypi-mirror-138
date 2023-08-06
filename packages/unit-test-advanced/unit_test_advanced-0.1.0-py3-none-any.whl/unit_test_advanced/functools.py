from unit_test_advanced.UnitTest import UnitTest

def initUT(func):
	def wrapper(*args, **kwargs):
		if 'UT' in kwargs and type(kwargs['UT']) != type(UnitTest):
			pass
		else:
			kwargs['UT'] = UnitTest()
		return func(*args, **kwargs)
	return wrapper