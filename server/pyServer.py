'''
Created on Sep 20, 2013

@author: aaronkrolik
'''

import tornado.ioloop
import urllib2
import time
import urllib



class pyServer():
    
    
    def pollSolr(self, queryString):
        #query = "http://localhost:8983/solr/collection1/select?q=" + urllib.quote('timestampEpoch_i:[{0} TO *]'.format(num)) + "&wt=json"
        query = "http://localhost:8983/solr/collection1/select?q=" + urllib.quote(queryString) + "&wt=json"
        
        print query
        req = urllib2.Request(url=query)
        req.add_header('Content-type', 'application/json')
        f = urllib2.urlopen(req)
        return f
        
x = pyServer()
foo = int(time.time() - 2000)
print x.pollSolr(foo).read()
1314630302