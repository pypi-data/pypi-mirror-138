'''
	Author  : RoodRepo
	Git     : https://github.com/roodrepo/unit_test_advanced
	Contact : roodrepo@gmail.com
	
	Title       : Unit Test Advanced
	Version     : 0.x.x
	Description : Execute unit tests using the production code - Program multiple scenarios and inject custom data if needed
'''

from importlib import import_module as sys_import_module
import random

class UnitTest:
	
	memory          : dict = {}
	execution_plans : list = []
	loaded_plans    : list = []
	
	verbose                 : bool
	is_enabled              : bool
	parent_execution_plan   : str
	children_execution_plan : str
	script_counter          : dict  = {}
	pooltest                        = None
	
	count_limit_identify_infinite_loop : int
	
	'''
		is_enabled: If true, UnitTesting is activated, otherwise will execute the default function in all cases
		
		parent_execution_plan / children_execution_plan
			"all"       executes all paths possible
			"random"    executes ONE random path based on all the potential possibilities
			"main"      executes the first path of all tests
		
		count_limit_identify_infinite_loop: Count to prevent looping multiple time on the same class. If set to 2, one class in an execution plan cannot be executed more than twice
		
		verbose: display progress of the execution
	'''
	def __init__(self, is_enabled = False, parent_execution_plan = 'all', children_execution_plan = 'all', count_limit_identify_infinite_loop = 2, verbose = False):
		
		self.updateSettings(**{
			'verbose'                               : verbose,
			'is_enabled'                            : is_enabled,
			'parent_execution_plan'                 : parent_execution_plan,
			'children_execution_plan'               : children_execution_plan,
			'count_limit_identify_infinite_loop'    : count_limit_identify_infinite_loop,
		})
		
		
		
	'''
		Securing the settings to update to a define list. Multiple settings can be updated at once
	'''
	def updateSettings(self, **kwargs):
		updatable_settings = ['verbose', 'is_enabled', 'parent_execution_plan', 'children_execution_plan', 'count_limit_identify_infinite_loop']
		for kwarg, value in kwargs.items():
			if kwarg in updatable_settings:
				setattr(self, kwarg, value)
	
	
	
	'''
		Print out texts when verbose mode is enabled
	'''
	def print(self, *args, level = 0):
		if self.verbose == True:
			args = list(args)
			
			if level == 1:
				args.insert(0, f'{"":4}')
			elif level == 2:
				args.insert(0, f'{"":8}')
			elif level == 3:
				args.insert(0, f'{"":12}')
			elif level == 4:
				args.insert(0, f'{"":16}')
				
			print(*args)
	
	
	
	'''
		Dynamically import modules if a string is passed
	'''
	def import_module(self, module):
		if isinstance(module, str):
			_tmp = module.split('.')
			module_path = '.'.join(_tmp[:-1])
			class_name  = _tmp[-1]
			
			# Importing the object dynamically
			module = sys_import_module(module_path)
			return getattr(module, class_name)
		else:
			return module
	
	
	
	'''
		For each execution plan, resetting both the counter and memory
	'''
	def resetCounter(self):
		self.script_counter = {}
		
	def resetMemory(self):
		self.memory         = {}
	
	
	
	'''
		id: The function to execute within the class if that function exists
		function: The actual function to execute in case the function-id does not exists
		*args and **kwargs are the argument to pass to both the fake function and real function
	'''
	def inject(self, id, function, *args, **kwargs):
		
		if self.is_enabled == True and hasattr(self.pooltest, id):
			return getattr(self.pooltest, id)(*args, **kwargs)
		else:
			return function(*args, **kwargs)
	
	
	
	'''
		Simply return the passed value. Useful when just a value needs to be faked out during unit test
	'''
	def returnValue(self, value):
		return value
	
	
	
	'''
		Checks how many time a class is called and raise an error when the limit "count_limit_identify_infinite_loop" is reached
	'''
	def checkInfiniteLoop(self, module_name):
		if module_name  not in self.script_counter:
			self.script_counter[module_name] = 0
			
		self.script_counter[module_name] += 1
		
		if self.script_counter[module_name] >= self.count_limit_identify_infinite_loop:
			raise Exception(f'Possible infinite loop identified on {module_name}')
	
	
	
	'''
		Executing all the main functions of a class
		pooltest        : Storing the current class executed for the unit test. Passing memory to access previous stored data
		trigger_params  : Parameters (dict) to pass from the class to the triggered function
		trigger         : Action (function) to trigger for the unit test
		final_check     : Final check after the action is complete
	'''
	def run(self, module):
		
		if self.is_enabled == True:
			module = self.import_module(module)
			
			init_params = {}
			if hasattr(self.pooltest, 'init_params'):
				init_params = module.init_params
				
			self.pooltest = module(**init_params)
			module_has_memory = False
			
			if hasattr(self.pooltest, 'setMemory'):
				self.pooltest.setMemory(memory = self.memory)
				module_has_memory = True
				
			params = {}
			if hasattr(self.pooltest, 'trigger_params'):
				params = self.pooltest.trigger_params
				
			if hasattr(module, 'trigger'):
				module.trigger(UT= self, **params)
				
			if hasattr(self.pooltest, 'final_check'):
				self.pooltest.final_check()
				
			# Updating the memory attribute
			if module_has_memory == True:
				self.memory = self.pooltest.memory
	
	
	
	'''
		Running an execution plan
	'''
	def runExecutionPlan(self, execution_plan):
		if self.is_enabled == True:
			self.resetMemory()
			self.print('Running execution plan: ', execution_plan)
			for module in execution_plan:
				self.run(module)
	
	
	
	'''
		Preparing the plans according the the settings and list passed.
		This function also prepare the execution tree for parents and children possibilities
	'''
	def preparePlans(self, list_unit_tests):
		if self.is_enabled == True:
			for unit_test in list_unit_tests:
				self.resetCounter()
				if isinstance(unit_test, list):
					self.execution_plans.append(unit_test)
				else:
					self.createExecutionPlans(unit_test)
					
			self.preventExecutionPlansDuplicates()
	
	
	'''
		Return all the current execution plans
	'''
	def getExecutionPlans(self):
		return self.execution_plans
	
	
	
	'''
		Resetting the execution plan list
	'''
	def resetExecutionPlans(self):
		self.execution_plans    = []
		self.loaded_plans       = []
	
	
	
	'''
		Entry point to start the unit tests
		Either prepare a list and execute or pass the list as argument to perform both actions at once
	'''
	def execute(self, list_unit_tests = None):
		if self.is_enabled == True:
			
			if list_unit_tests != None:
				self.preparePlans(list_unit_tests)
				
			for ep in self.execution_plans:
				self.runExecutionPlan(ep)
				
			self.resetExecutionPlans()
			
			
			
	'''
		Removing duplicated plans
	'''
	def preventExecutionPlansDuplicates(self):
		final_plans = []
		for plan in self.execution_plans:
			_modules_in_plan = []
			for _module in plan:
				_modules_in_plan.append(_module.__name__)
				
			if _modules_in_plan not in self.loaded_plans:
				self.loaded_plans.append(_modules_in_plan)
				final_plans.append(plan)
				
		self.execution_plans = final_plans
		
	
	'''
		If verbose mode is enable, print out if the reversed relation is not found
	'''
	def checkRelationship(self, obj, attr, check_obj):
		if self.verbose == True:
			if (hasattr(obj, attr) == False):
				self.print(f'{obj} do not have {check_obj} in {attr}', level= 1)
			else:
				_imported_modules = []
				for _module in getattr(obj, attr):
					_imported_modules.append(self.import_module(_module))
					
				if check_obj not in _imported_modules:
					self.print(f'{obj} do not have {check_obj} in {attr}', level= 1)
	'''
		From a plan, create the parent tree
	'''
	def getParentPlans(self, plans):
		new_plans = []
		dependencies_found = False
		for plan in plans:
			if hasattr(plan[0], 'dependencies'):
				dependencies_found = True
				if self.parent_execution_plan == 'all':
					for dependency in plan[0].dependencies:
						dependency = self.import_module(dependency)
						new_plans.append([dependency] + plan.copy())
						
						# Relationship verification
						self.checkRelationship(dependency, 'children', plan[-1])
						
				else:
					idx = 0
					if self.parent_execution_plan == 'random':
						idx = random.randint(0, len(plan[0].dependencies) -1)
						
					dependency = self.import_module(plan[0].dependencies[idx])
					new_plans.append([dependency] + plan.copy())
					
					# Relationship verification
					self.checkRelationship(dependency, 'children', plan[-1])
					
			else:
				new_plans.append(plan.copy())
				
		if dependencies_found == True:
			plans = self.getParentPlans(new_plans)
			
		return plans
	
	
	
	'''
		From a plan, create the children tree
	'''
	def getChildrenPlans(self, plans):
		new_plans = []
		dependencies_found = False
		# print(plans)
		for plan in plans:
			
			if hasattr(plan[-1], 'children'):
				dependencies_found = True
				if self.children_execution_plan == 'all':
					for child in plan[-1].children:
						child = self.import_module(child)
						new_plans.append(plan.copy() + [child])
						
						# Relationship verification
						self.checkRelationship(child, 'dependencies', plan[-1])
						
						
				else:
					idx = 0
					if self.children_execution_plan == 'random':
						idx = random.randint(0, len(plan[-1].children) -1)
						
					child = self.import_module(plan[-1].children[idx])
					new_plans.append(plan.copy() + [child])
					
					# Relationship verification
					self.checkRelationship(child, 'dependencies', plan[-1])
			else:
				new_plans.append(plan.copy())
				
		if dependencies_found == True:
			plans = self.getChildrenPlans(new_plans)
			
		return plans
	
	
	
	'''
		Manage and put together the parent tree and children tree
	'''
	def createExecutionPlans(self, module):
		current_plans = [[module]]
		
		self.print('Checking relationships...')
		current_plans = self.getParentPlans(current_plans)
		current_plans = self.getChildrenPlans(current_plans)
		
		self.execution_plans += current_plans
	