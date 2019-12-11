# Utility Functions

Functions to make life easier as a Python Developer. There was some adjustments in using Python when I have come from PHP for 10 years & Java before that. I put this in the Lib/site-packages folder so it could be imported in every single program/app I have made.

| Functions | Purpose |
| ------ | ------ |
| print_structure | Takes any Dictionary that is deeply deeply nested in LOTS of levels (whether it's 10 or 100 or unlimited), and just simply shows the hierarchy of keys + list Indexes at every node, and the value. GONE are the days of guessing and messing around on the console to find out the right keys to access one little value on that deeply nested div of 100 levels. |
| sanitize | only include ASCII characters for cases with messy unicode and you don't care about Unicode 
| get_item | get a value in a list, with the option of a default value if there's a key error. Just handle the responsiblity of this somewhere else for cleaner code |
| file_put_contents | Just a throwback and habit of my old PHP days, haha. Puts data in a file by the filename |
| file_get_contents | Vice Versa keeping up with PHP theme |
| get_html | Get the HTML but with Browser Cookies/User Agent to increase the chances of getting the desired HTML (generally for scraping) |
| dvkp | From an old project I did, it gets the value of a dictionary based on a substring of a key. With an option for default argument if there's nothing. |

# Very Deeply Nested Key/Value Data Structure into Neat Text to find the order of Keys & Lists to access value in Structure

![](images/xml_hierarchy.jpg)

# Utility "Helper" functions

```python
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
		req=urllib.request.Request(url, None, {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; G518Rco3Yp0uLV40Lcc9hAzC1BOROTJADjicLjOmlr4=) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'})
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

def dvkp(dict, key_part, default=''):
	try:
		return [value for key,value in dict.items() if key_part in key][0]
	except:
		return default
```