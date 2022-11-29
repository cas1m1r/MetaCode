import utils
import json
import sys  
import os


class Program:
	def __init__(self, filepath):
		if not os.path.isfile(filepath):
			print(f'[!] Cannot find {filepath}')
			return
		else:
			self.binary = self.load_binary(filepath)
		# read the program data line by line 
		self.data, self.functions = self.parse()


	def load_binary(self, filename):
		return open(filename, 'rb').read()


	def parse(self):
		data = {}
		functions = {}
		lc = 1
		for line in self.binary.split(b'\n'):
			# each line of code is a dict{}
			data[lc] = {'code': '', 'comment': '', 'include':'', 'definition':''}
			# look for a comment
			if line.find(b'/*') >=0:
				# TODO: What about multiline comments?
				data[lc]['comment'] = str(line[line.find(b'/*'):])
				hasComment = True
			if line.find(b'//')>=0:
				# this is a single line comment 
				data[lc]['comment'] = str(line[line.find(b'//'):])
				hasComment = True 
			# look for definitions 
			if line.find(b'#define')>=0:
				data[lc]['definition'] = str(line[line.find(b'#define')+8:])
			# look for includes
			if line.find(b'#include') >= 0:
				data[lc]['include'] = str(line[line.find(b'#include')+9:])
			# look for function signatures
			if line.find(b'(')>0 and line.find(b')')>0 and line.find(b'//')<0 and line.find(b'/*')<0: 
				data[lc]['code'] = str(line)
				# print(f'SIGNATURE:\t{line}')
				#TODO: Make function signatures a separate thing to track
				if line.find(b';') < 0 :
					elmts = line.split(b' ')
					return_type = elmts[0]
					fcn_name = elmts[1].split(b'(')[0]
					fcn_args = line[line.find(b'('):line.find(b')')].split(b',')
					functions[fcn_name] = {'returns': return_type, 'args': fcn_args}
				# TODO: Track the start of this and look for the end
			# look for code 
			if line.find(b';')>=0: # ending of code
				data[lc]['code'] = str(line[:line.find(b';')].decode('utf-8'))
			elif line.find(b'}')>=0: # ending of structs or functions
				data[lc]['code'] = str(line[line.find(b'}'):].decode('utf-8'))
				# This will always be end of something important!

			# LOOK FOR DECLS

			# increment linecount 
			lc += 1
		return data, functions

	def __str__(self):
		output = ''
		for line in self.data.keys():
			# check whats filled
			if len(self.data[line]['code']):
				output += str(self.data[line]['code'])
			if len(self.data[line]['definition']):
				output += f'#define {str(self.data[line]["definition"])}'
			if len(self.data[line]['include']):
				output += f'#include {str(self.data[line]["include"])}'
			if len(self.data[line]['comment']):
				output += str(self.data[line]['comment'])
			
			output += '\n'
		return output

	def __repr__(self):
		return str(json.dumps(self.data,indent=2))