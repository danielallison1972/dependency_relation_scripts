import json
import jsonpath_ng as jp
import re
import sys
from json_ntv import Ntv

'''
creates 'markdown' from json for mermaid.live
'''

def load(pathfile):
	f = open(pathfile)
	data = json.load(f)
	return data

def ntv_mermaid(pathfile):
	data = load(pathfile)
	dat = {'title':data}
	prelim = []
	cleaned_up = []
	dict = Ntv.obj(data).to_mermaid(disp=False)
	mermaid_str = dict[':$mermaid']
	lines = mermaid_str.split('\n')
	for line in lines:
		prelim.append(line.lstrip().rstrip())
	for line in prelim:
		if line ==  '("<b>::</b>")':
			line = 'AAA("<b>::</b>")'
		elif line[:3] == '-->':
			line = 'AAA -->' + line[3:]
		cleaned_up.append(line)
	return cleaned_up

def dictmap(pathfile):
	#builds a single layer dictionary out of nested elements
	data = load(pathfile)
	d = {}
	expr = jp.parse('$..*')
	for m in expr.find(data):
		d[str(m.full_path)] = m.value
	return data,d

if __name__ in '__main__':
	if len(sys.argv) < 2:
		sys.exit('Usage %s path-to-sbom.json' % sys.argv[0])
	pathfile = sys.argv[1]
	lines = ntv_mermaid(pathfile)
	print('for use with live editor at https://mermaid.live')
	for entry in lines:
		print(entry)
