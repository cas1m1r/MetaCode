import sys  
import os 


def crawl_dir(path:str, data:{}):
	if path not in data.keys():
		data[path] = []
	for item in os.listdir(path):
		f = os.path.join(path, item)
		if os.path.isfile(f):
			data[path].append(f)
		else:
			data = crawl_dir(f, data)
	return data