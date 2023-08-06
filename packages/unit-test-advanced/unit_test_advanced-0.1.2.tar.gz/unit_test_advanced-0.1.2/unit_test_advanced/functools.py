from unit_test_advanced.UnitTest import UnitTest

def initUT(func):
	def wrapper(*args, **kwargs):
		list_args = func.__code__.co_varnames
		
		if 'UT' not in kwargs and 'UT' in list_args:
			kwargs['UT'] = UnitTest()
			
		elif 'UT' in kwargs and 'UT' not in list_args:
			del kwargs['UT']
			
		return func(*args, **kwargs)
	return wrapper