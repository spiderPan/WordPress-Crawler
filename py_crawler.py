#!/usr/bin/env python

import argparse
import re
import requests
import StringIO
from bs4 import BeautifulSoup
import os


def _main():
    argParser = argparse.ArgumentParser(
        description='Scan any wordpress powered website and identify plugins installed')
    argParser.add_argument('-s', '--scan', metavar='<website url>', dest='url',
                           help='scan website at <website url> to see how many plugins installed(untested)')
    argParser.add_argument('-u', '--update', type=int, metavar='<page number>', dest='pageN',
                           help='update the list of plugins from wordpress.org up to <page number>')
    argParser.add_argument('-a', '--all', metavar='<plugin name>', dest='pluginName',
                           help='scaning all preset sites to look for <plugin name>')
    args = argParser.parse_args()
    try:
        if args.url == args.pageN == args.pluginName is None:
            argParser.print_help()
        elif args.pluginName is not None:
            scanSites(args.pluginName)
        elif args.url is not None:
            scanPlugins(args.url)
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


def _parseHrefs(html):
    doc = BeautifulSoup(html)
    pattern = re.compile('/plugins/([\w\d\-]+)/')
    pluginsList = []
    links = doc.find_all('a', class_='plugin-icon')
    for link in links:
        plugin = pattern.search(link.get('href')).group(1)
        pluginsList.append(plugin)
        print plugin + '[+]'
    return pluginsList


def _requestURL(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36"}

    request = requests.get(url, headers=headers)
    return request


def _getRequestStatusCode(url):
    response = _requestURL(url)
    return response.status_code


def _readURL(url):
    response = _requestURL(url)
    return response.text


def _writePlugins(pluginsList):
    currentDir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
    pluginsFile = open(currentDir + 'plugins.txt', 'w')
    pluginsFile.write('\n'.join(pluginsList))
    pluginsFile.close()


def scanSites(pluginName):
    headerContent = 'Scanning all sites for {0}...'.format(pluginName)
    resultFile = open('./results.txt', 'w+')
    print headerContent
    resultFile.write(headerContent + '\n')
    urlList = [line.rstrip() for line in open('./sites.txt')]
    for url in urlList:
        pluginURL = 'http://' + url + '/wp-content/plugins/' + pluginName
        code = _getRequestStatusCode(pluginURL)
        if code in (403, 304, 200):
            lineResultsText = url + '[+]'
            resultFile.write(lineResultsText + '\n')
            print lineResultsText
    f.close()
    print "Scanning Complete!"


def scanPlugins(url):
    if _isUrl(url) != True:
        print 'The url you entered should match this pattern ^https?://[\w\d\-\.]+/(([\w\d\-]+/)+)?$'
        return
    print 'Scanning...'
    currentDir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
    pluginsFile = open(currentDir + 'plugins.txt', 'r')
    for line in pluginsFile.read().split('\n'):
        if line:
            code = _requestURL(url + 'wp-content/plugins/' + line + '/')
            if code is False:
                continue
            if code != 404:
                print line + '[+]'
    print "Scanning Complete!"


def update(pageN):
    pluginsList = []
    if pageN == 1:
        html = _readURL('https://wordpress.org/extend/plugins/browse/popular/')
        pluginsList = _parseHrefs(html)
    elif pageN == 2:
        html = _readURL('https://wordpress.org/extend/plugins/browse/popular/')
        pluginsList = _parseHrefs(html)
        html = _readURL(
            'https://wordpress.org/extend/plugins/browse/popular/page/2/')
        pluginsList = pluginsList + _parseHrefs(html)
    else:
        for page in range(2, pageN):
            html = _readURL(
                'https://wordpress.org/extend/plugins/browse/popular/page/' + str(page) + '/')
            pluginsList = pluginsList + _parseHrefs(html)
    _writePlugins(pluginsList)


if __name__ == "__main__":
    _main()
