import json
import re
import sys
from json_ntv import Ntv
import os

'''
creates a dot file based on json, then uses graphviz to create an svg graphic from the dot file
'''

def load(pathfile):
	f = open(pathfile)
	data = json.load(f)
	return data

def ntv_mermaid(pathfile):
	data = load(pathfile)
	prelim = []
	cleaned_up = []
	dict = Ntv.obj(data).to_mermaid(disp=False)
	mermaid_str = dict[':$mermaid']
	mermaid_str = mermaid_str.replace('\n<i>','<i>')
	mermaid_str = mermaid_str.replace('</b><i>',': ')
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

def mermaid_dot(pathfile):
	cleaned_up = ntv_mermaid(pathfile)
	altered = ['digraph test {']
	for line in cleaned_up[1:]:
		if '-->' in line:
			#default behavior for ntv_mermaid conversion is /
			newline = re.sub('/','8',line)
			parts = newline.split(' --> ')
			replaced = []
			for part in parts:
				replaced.append('"' + part + '"')
			new=' -> '.join(replaced)
			altered.append(new)
		else:	
			#default behavior for ntv_mermaid conversion is /
			leftsplit = line.split(' ')[0]
			newline = re.sub('/','8',leftsplit) + ' '.join(line.split(' ')[1:])
			newline = newline.replace('("<b>',' [label="')
			newline = newline.replace('("<b>',' [label="')
			newline = newline.replace('["<b>',' [label="')
			newline = newline.replace('<8i>"]',' "]')
			newline = newline.replace('<8b>")',' "]')
			newline = newline.replace('<8i>")',' "]')
			newline = newline.replace('<8b>"]',' "]')
			newline = newline.replace('</i>"]',' "]')
			altered.append(newline)	
		
	
	altered.append('}')
	return altered

def write_dot(pathfile):
	altered = mermaid_dot(pathfile)
	path,file = os.path.split(pathfile)
	filename,ext = file.split('.')
	dotfile = filename + '.dot'
	f = open(dotfile,'w+')
	for line in altered:
		f.write(line + '\n')
	f.close()

	svgfile = filename + '.svg'
	os.system('dot -Tsvg %s > %s' % (dotfile,svgfile))	


if __name__ in '__main__':
	if len(sys.argv) < 2:
		sys.exit('Usage %s path-to-sbom.json' % sys.argv[0])
	pathfile = sys.argv[1]
	lines = mermaid_dot(pathfile)
	write_dot(pathfile)
