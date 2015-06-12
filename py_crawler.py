import urllib2
import urllib
import re


SITE_URL = 'https://csaps.ca/'
PLUGIN_PATTERN = re.compile(r'<script .+?src=[\'"](.+?)[\'"]')


def GetPage(url, pattern):
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
		html = req.read()
		encoding=req.headers['content-type'].split('charset=')[-1]
		ucontent = unicode(html, encoding)
	except Exception, e:
		print u'**ERROR**: {0} : {1}\t--IGNORE--' .format(url, e)
	
	print ucontent.encode('utf-8')
	values = pattern.findall(ucontent)
	if values:
		print values
       
            
			
GetPage(SITE_URL, PLUGIN_PATTERN)