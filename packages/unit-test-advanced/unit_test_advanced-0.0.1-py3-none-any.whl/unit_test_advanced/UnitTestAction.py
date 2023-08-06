class UnitTestAction(object):
	
	# Attribute to pass data from one class to another in the execution plan
	memory = {}
	
	def setMemory(self, memory):
		self.memory = memory