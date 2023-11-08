#!/usr/bin/env python3
import json
from urllib.request import urlopen
import urllib.error 
import sys
import os

CVEADPPILOT_URL = 'https://cveawg-adp-test.mitre.org/api/cve/'

def check_ssvc(cve):
	url = CVEADPPILOT_URL + cve
	try:
		content = urlopen(url).read()
		data = json.loads(content)
		containers = data['containers']
		try:
			adp = containers['adp']
		except KeyError:
			adp = 'there is no adp content for CVE: %s' % cve# on the pilot (url:%s)' % (cve,url)
	except urllib.error.HTTPError:
		adp = 'HTTP ERROR: check that this ia a valid CVE'
	return adp

if __name__ == '__main__':
	if len(sys.argv) <2:
		sys.exit('usage: %s <cve>' % sys.argv[0])
	cve = sys.argv[1].upper()
	adp = check_ssvc(cve)
	print(json.dumps(adp,indent=2))



