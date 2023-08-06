from unit_test_advanced.UnitTest import UnitTest

def initUT(func):
	def wrapper(*args, **kwargs):
		
		if 'UT' not in kwargs:
			if 'UT' in func.__code__.co_varnames:
				kwargs['UT'] = UnitTest()
				
		return func(*args, **kwargs)
	return wrapper