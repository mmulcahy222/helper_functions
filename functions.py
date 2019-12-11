from collections import OrderedDict
from http.cookiejar import CookieJar
import urllib


# def print_value(value):
# 	'''
# 	print out the value column for the structure (either string )
# 	'''
# 	if isinstance(value, str) or isinstance(value, int):
# 		#if it is string or int, send it. You have reached a "leaf" in the structure
# 		return str(value).replace("\n"," ").strip()
# 	else:
# 		#Just print the type of class, instead of a whole entire tree. It's useless for us.
# 		return type(value).__name__

def print_structure(structure):
	depth = 0
	path = []
	def recurse(structure):
		nonlocal depth
		nonlocal path
		text = ''
		if isinstance(structure, dict) or isinstance(structure, OrderedDict):
			for k, value in structure.items():
				depth += 1
				path.append(str(k))
				recurse(value)
				path.pop()
				depth -= 1
		elif isinstance(structure, list):
			for i, value in enumerate(structure):
				depth += 1
				path.append(str(i))
				recurse(value)
				path.pop()
				depth -= 1
		else:
			#You Are now in a leaf of the structure, which can be an INT or a STRING
			keys = "|".join(path)
			value_string = str(structure).replace("\n"," ").strip()
			text = "{:2} {:80} {:20}\n".format(str(depth), keys,value_string)
			print(text.strip())
	recurse(structure)
	return structure


def sanitize(word):
	return ''.join([x for x in str(word) if ord(x) < 128])

def get_item(iterable, index, default=''):
	try:
		return operator.getitem(iterable, index)
	except:
		return default



def file_put_contents(filename,data):
	f = open(filename, 'w')
	data = sanitize(data)
	w = f.write(data)
	f.close()
	return w

def file_add_contents(filename,data):
	f = open(filename, 'a')
	data = sanitize(data)
	w = f.write(data)
	f.close()
	return w

def file_put_image(image_link,file_name):
	f = open(file_name, 'wb')
	w = f.write(requests.get(image_link, timeout=10).content)
	f.close()
	return w

def file_get_contents(filename):
	f = open(filename, 'r', errors='ignore')
	r = f.read()
	r = sanitize(r)
	f.close()
	return r

def get_html(url):
	try:
		req=urllib.request.Request(url, None, {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; =) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'})
		cj = CookieJar()
		opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
		response = opener.open(req)
		raw_response = response.read().decode('utf8', errors='ignore')
		response.close()
		raw_response = ''.join([x for x in str(raw_response) if ord(x) < 128])
		raw_response = raw_response.replace("<!DOCTYPE html>","").replace("\n","")
		return(raw_response)
	except urllib.request.HTTPError as inst:
		output = format(inst)
		print(output)
