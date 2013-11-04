'''
Created on Sep 20, 2013

@author: aaronkrolik
'''
from Plugin import Plugin

import urllib2
from xml.dom import minidom
import time
import json
import urllib
import time
import collections
import itertools

class PluginRSS(Plugin):
    def __init__(self):
        self.listOfTargetURL = self.getRSSURLs()
    
    def getRSSURLs(self, filepath="../resources/RSSURL"):
        f = open(filepath, 'r')
        RSSTarget = collections.namedtuple("RSSTarget", "name, URL")
        listOfTargets = []
        for line in f:
            listOfTargets.append(RSSTarget._make(line.strip().split(",")))
        f.close()
        return listOfTargets
            
    #Taken from StackOverflow post
    def getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
    
    def retreiveData(self, targets=[]):
        rawXMLOutputList = map(lambda x: urllib2.build_opener(urllib2.HTTPCookieProcessor).open(x.URL).read(), targets)
        return rawXMLOutputList
    
    def formatHelper(self, rawXMLOutputElement):
        parsedDOM = minidom.parseString(rawXMLOutputElement)
        itemList = parsedDOM.getElementsByTagName("item")
        docList = []
        for item in itemList:
            tempDoc = {}
            title = item.getElementsByTagName("title")[0]
            tempDoc["title_s"] = self.getText(title.childNodes)
            tempDoc["timestampEpoch_i"] = self.getEpoch()
            tempDoc["type_s"] = "headline"
            tempDoc["id"] = self.getText(title.childNodes)
            docList.append(tempDoc)
        return docList
        
    def formatJSONStrForSolrIndexing(self, rawXMLOutputList):
        JSONList = map(self.formatHelper, rawXMLOutputList)
        concatJSONList = list(itertools.chain(*JSONList))
        JSONStr = json.dumps(concatJSONList)
        
        return JSONStr
    
    def submitToSolr(self, JSONStr):
        
        req = urllib2.Request(url='http://localhost:8983/solr/update/json?commit=true',
                              data=JSONStr)
        req.add_header('Content-type', 'application/json')
        f = urllib2.urlopen(req)
        # Begin using data like the following
        response = f.read()
        
        return response
        

if __name__ == "__main__":
    print time.gmtime()
    plugin = PluginRSS()
    print plugin.getRSSURLs()
    print "\n*\n*\n"
    while True:
        l = plugin.retreiveData(plugin.listOfTargetURL)
        x = plugin.formatJSONStrForSolrIndexing(l)
        print plugin.submitToSolr(x)
        time.sleep(300)