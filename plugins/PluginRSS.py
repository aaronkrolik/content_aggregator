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
    
    def getRSSURLs(self, filepath="./resources/RSSURL"):
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
        return unicode(''.join(rc))
    
    def retreiveData(self, targets=[]):
        rawXMLOutputList = map(lambda x: urllib2.build_opener(urllib2.HTTPCookieProcessor).open(x.URL).read(), targets)
        return zip(rawXMLOutputList, [x.name for x in targets])
    
    def formatHelper(self, rawXMLOutputElementTup):
        rawXMLOutputElement = rawXMLOutputElementTup[0]
        parsedDOM = minidom.parseString(rawXMLOutputElement)
        itemList = parsedDOM.getElementsByTagName("item")
        docList = []
        for item in itemList:
            try:
                tempDoc = {}
                title = item.getElementsByTagName("title")[0]
                link  = item.getElementsByTagName("link")[0]
                pubDate = item.getElementsByTagName("pubDate")[0]
                tempDoc["link_t"] = self.getText(link.childNodes)
                tempDoc["pubDate_s"] = self.getText(pubDate.childNodes)
                tempDoc["title_t"] = self.getText(title.childNodes)
                tempDoc["source_s"]=rawXMLOutputElementTup[1]
                tempDoc["timestampEpoch_i"] = self.getEpoch()
                tempDoc["type_s"] = "headline"
                tempDoc["id"] = self.getText(title.childNodes)
                docList.append(tempDoc)
            except:
                print "Failed in format helper loop"
                
        return docList
        
    def formatJSONStrForSolrIndexing(self, rawXMLOutputList):
        JSONList = map(self.formatHelper, rawXMLOutputList)
        concatJSONList = list(itertools.chain(*JSONList))
        JSONStr = json.dumps(concatJSONList)
        
        return JSONStr
    
    def submitToSolr(self, JSONStr):
        
        req = urllib2.Request(url='http://54.201.40.213:8983/solr/update/json?commit=true',
                              data=JSONStr)
        req.add_header('Content-type', 'application/json')
        f = urllib2.urlopen(req)
        # Begin using data like the following
        response = f.read()
        
        return response
    
    def run(self):
        while True:
            l = self.retreiveData(self.listOfTargetURL)
            x = self.formatJSONStrForSolrIndexing(l)
            print self.submitToSolr(x)
            time.sleep(300)
        

if __name__ == "__main__":
    plugin = PluginRSS()
    plugin.getRSSURLs()
    while True:
        l = plugin.retreiveData(plugin.listOfTargetURL)
        x = plugin.formatJSONStrForSolrIndexing(l)
        print plugin.submitToSolr(x)
        time.sleep(300)
