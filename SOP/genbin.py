class CodeGen:
	def __init(self, config):
		if 'includes' in config.keys():
			self.includes = self.add_includes(config)


	def add_includes(self, setup):
		libraries = []
		for lib in setup['includes']:
			libraries.append(lib)
		return libraries





	def create(self):
		output = b''
		# add includes
		if len(self.includes):
			for lib in self.includes:
				output += f'#include {lib}\n' 
		# 
		# add functions 

		# add main
