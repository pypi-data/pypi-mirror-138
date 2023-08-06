import os
from unit_test_advanced.UnitTest import UnitTest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

'''
	Injecting some data that will be different according from where the file is executed.
	If the file is run directly, the content of "myfile.txt" is "actual api call".
	However, when run from the unit test, the content is "fake api call". The function "fakeApiCall" from the class step2_InjectDataExample is actually executed instead of "imagineThisIsAnApiCall".
'''


def imagineThisIsAnApiCall(myParam):
	return 'actual api call'

# For each entry point, the function must accept the UT parameter and initialize it when Null
def run(UT = None):
	UT = UT if UT != None else UnitTest()
	
	f = open(f'{BASE_DIR}/myfile.txt', 'w+')
	
	is_injected = UT.inject(
		'inject_value',
		UT.returnValue,
		value= True
	)
	
	f.write(
		UT.inject(
			'fakeApiCall',
			imagineThisIsAnApiCall,
			myParam = 'value to pass'
		)
	)
	f.close()
	
	f = open(f'{BASE_DIR}/myfile.txt', 'r')
	print(f'File content after executing {os.path.basename(__file__)}: "{f.read()}"')
	f.close()
	
if __name__ == '__main__':
	run()
