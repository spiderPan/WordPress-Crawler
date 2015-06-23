#!/usr/bin/env python

import argparse
import sys
import re
import urllib
import urllib2
import lxml.html
import os

def _main():
	argParser = argparse.ArgumentParser(description='Scan any wordpress powered website and identify plugins installed')
	argParser.add_argument('-s', '--scan', metavar='<website url>', dest='url', help='scan website at <website url>')
	argParser.add_argument('-u', '--update', type=int, metavar='<page number>', dest='pageN', help='update the list of plugins from wordpress.org up to <page number>')
	args = argParser.parse_args()
	try:
		if args.url == args.pageN == None:
			argParser.print_help()
		elif args.url != None:
			scan(args.url)
		else:
			update(args.pageN)
	except IOError as e:
		print e

def _isUrl(url):
	pattern = re.compile('^https?://[\w\d\-\.]+/(([\w\d\-]+/)+)?$')
	if pattern.match(url):
		return True
	else:
		return False

# def _isWebsiteAlive(url):
	
	# if readURL(url).c == 200:
		# return True
	# else:
		# return False

def _parseHrefs(html):
	doc = lxml.html.document_fromstring(html)
	pattern = re.compile('/plugins/([\w\d\-]+)/')
	pluginsList = []
	links = doc.cssselect('div.plugin-block h3 a')
	for link in links:
		plugin = pattern.search(link.get('href')).group(1)
		pluginsList.append(plugin)
		print plugin + '[+]'
	return pluginsList

def _writePlugins(pluginsList):
	currentDir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
	pluginsFile = open(currentDir + 'plugins.txt', 'w')
	pluginsFile.write('\n'.join(pluginsList))
	pluginsFile.close()

def scan(url):
	if _isUrl(url) != True:
		print 'The url you entered should match this pattern ^https?://[\w\d\-\.]+/(([\w\d\-]+/)+)?$'
		return
	# elif _isWebsiteAlive(url) != True:
		# print 'the url {0} is not live'.format(url)
		# return
	print 'Scanning...'
	currentDir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
	pluginsFile = open(currentDir + 'plugins.txt', 'r')
	for line in pluginsFile.read().split('\n'):
		if line:
			code = readURL(url + 'wp-content/plugins/' + line + '/')
			if code != 404:
				print line + '[+]'

def update(pageN):
	pluginsList = []
	if pageN == 1:
		html = readURL('http://wordpress.org/extend/plugins/browse/popular/').read()
		pluginsList = _parseHrefs(html)
	elif pageN == 2:
		html = readURL('http://wordpress.org/extend/plugins/browse/popular/').read()
		pluginsList = _parseHrefs(html)
		html = readURL('http://wordpress.org/extend/plugins/browse/popular/page/2/').read()
		pluginsList = pluginsList + _parseHrefs(html)
	else:
		for page in range(2, pageN):
			html = readURL('http://wordpress.org/extend/plugins/browse/popular/page/' + str(page) + '/').read()
			pluginsList = pluginsList + _parseHrefs(html)
	_writePlugins(pluginsList)
	
def readURL(url):
	headers = {"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
				"Accept-Encoding":"gzip, deflate, sdch",
				"Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
				"Cache-Control":"no-cache",
				"Connection":"keep-alive",
				"Pragma":"no-cache",
				"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36"}
	
	request = urllib2.Request(url, headers = headers)
	try:
		req = urllib2.urlopen(request)
		return req
	except urllib2.HTTPError as e:
		if e.code == 403:
			return 403
		elif e.code == 404:
			return 404
		else:
			print u'**ERROR**: {0} : {1}\t--IGNORE--' .format(url, e)     

if __name__ == "__main__": _main()