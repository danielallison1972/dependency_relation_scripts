from bs4 import BeautifulSoup
import requests
import sys
import re
import json

"""
scrapes www.npmjs.com for package data and builds json file
"""
BASE_URL = 'https://www.npmjs.com/package/'

def get_components(package,basejson):
	url = BASE_URL + package
	content = requests.get(url)
	soup = BeautifulSoup(content.content,'html5lib')
	scripts = soup.find_all('script')
	results = []
	for script in scripts:
		searches = re.search('dependencies',str(script.string))
		if searches:
			results.append(str(script.string))
	for result in results:
		searchstring = 'name":"%s",.*version":.*versions"' % package
		version = re.findall(searchstring,result)[0]
		packagenamelength = len(package)
		version = version[7+ packagenamelength + 29:7+packagenamelength + 34]
		basejson = {"name":package,"version":version,"components" :[]}
		#dep = re.findall('"dependencies.*}.*"devDep',result)
		dep = re.findall('"dependencies.*"devDep',result)
		try:	
			dstring = '{' + dep[0][:-8] + '}'
			djson = json.loads(dstring)
			for dependency in djson["dependencies"]:
				subname = dependency
				subversion = djson["dependencies"][dependency]
				subjson = {"name":subname,"version":subversion,"components":[]}
				subcomponents = get_components(dependency,subjson)
				basejson['components'].append(subcomponents)
		except IndexError:
			djson = {}
	return basejson


		
if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.exit('Usage: %s <package_name>' % sys.argv[0])
	package = sys.argv[1]
	x=get_components(package,{})
	print(json.dumps(x,indent=2))
