#!/usr/bin/python
# 
# JSON pretty printer, you can pass URL, string or file
# and it will output nicely printed json

import json, sys, urllib2

# JSON data providers
def jsonFromURL(url):
	response = urllib2.urlopen(url)
	html = response.read()
	if html != None:
		return json.loads(html)
	else:
		error('cannot open URL: %s' % url)

def jsonFromFile(file):
	with open(file) as f:
		return json.load(f)

	error('cannot open file: %s' % file)

def jsonFromString(string):
	return json.loads(string)

# Help & Error
def error(msg):
	print 'Error: %s' % msg
	exit(1)

def printHelpAndExit():
	print 'Usage: %s --file/--url/--string <data>' % sys.argv[0]
	exit()

# Main
if len(sys.argv) != 3:
	printHelpAndExit()

option = sys.argv[1]
data = None
if option == '--file':
	data = jsonFromFile(sys.argv[2])
elif option == '--url':
	data = jsonFromURL(sys.argv[2])
elif option == '--string':
	data = jsonFromString(sys.argv[2])
else:
	printHelpAndExit()

if data != None:
	print json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '))
else:
	error('something wrong with getting JSON!')