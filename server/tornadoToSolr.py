'''
Tornado server handling requests from clients by fetching from Solr
'''

import tornado.ioloop
import tornado.web
import urllib
import urllib2
import urlparse

#TODO: make methods more abstract, write the constructor, and write the json parsing aspect
class SolrHandler(tornado.web.RequestHandler):
    #let's initialize these using a constructor in the future (read from config file?)
    solrFieldQuery="q"
    solrFieldTimestamp="timestampEpoch_i"
    solrFieldHeadline="title_t"
    solrFieldRows="rows"
    solrFieldFormat="wt"
    solrFieldSorting="sort"
    clientFieldTimestamp="lastUpdate"
    clientFieldHeadline="search"
    maxHits="10"
    responseFormat="json"
    sortingOrder=solrFieldTimestamp + " desc"
    #have these in a urlparse-friendly format
    solrScheme="http"
    solrNetloc="localhost:8983"
    solrPath="/solr/collection1/select"

    def parseClientQuery(self, clientQueryString):
        clientQuery=urlparse.parse_qs(clientQueryString)
        for clientField in (self.clientFieldTimestamp, self.clientFieldHeadline):
            if clientField not in clientQuery:
                clientQuery[clientField]=["*"]
        return clientQuery

    def createSolrQuery(self, clientQuery):
        solrQuery=dict()
        solrQuery[self.solrFieldQuery]=self.solrFieldTimestamp + ":[" + clientQuery[self.clientFieldTimestamp][0] + " TO *] AND " + self.solrFieldHeadline + ":" + clientQuery[self.clientFieldHeadline][0]
        solrQuery[self.solrFieldRows]=self.maxHits
        solrQuery[self.solrFieldFormat]=self.responseFormat
        solrQuery[self.solrFieldSorting]=self.sortingOrder
        return solrQuery

    def querySolr(self, solrQuery):
        solrQueryString=urllib.urlencode(solrQuery)
        solrURL = urlparse.urlunparse((self.solrScheme, self.solrNetloc, self.solrPath, '', solrQueryString, ''))
        solrResponse=urllib2.urlopen(solrURL)
        return solrResponse

    def formatResponse(self, response):
        return response.read()

    def get(self):
        clientQuery=self.parseClientQuery(self.request.query)

        solrQuery=self.createSolrQuery(clientQuery)

        solrResponse=self.querySolr(solrQuery)
        
        #send request back to client
        self.write(self.formatResponse(solrResponse))
        self.set_header('Content-type', 'application/json')

class AndroidTestHandler(tornado.web.RequestHandler):
    def get(self):
        static_response='{ "responseHeader": { "status": 0, "QTime": 4, "params": { "indent": "true", "q": "*:*", "_": "1384043579811", "wt": "json" } }, "response": { "numFound": 64, "start": 0, "docs": [ { "title_t": "Viral Facebook post says Obamacare fines to be seized from bank accounts", "type_s": "headline", "id": "Viral Facebook post says Obamacare fines to be seized from bank accounts", "timestampEpoch_i": 1383713083, "_version_": 1450928330229416000 }, { "title_t": "Asian shares frozen by Fed, ECB uncertainty", "type_s": "headline", "id": "Asian shares frozen by Fed, ECB uncertainty", "timestampEpoch_i": 1383713083, "_version_": 1450928330292330500 }, { "title_t": "Acer shares tumble by daily limit after CEO resigns, job cuts", "type_s": "headline", "id": "Acer shares tumble by daily limit after CEO resigns, job cuts", "timestampEpoch_i": 1383713083, "_version_": 1450928330298622000 }, { "title_t": "Office Depot closes deal to buy OfficeMax", "type_s": "headline", "id": "Office Depot closes deal to buy OfficeMax", "timestampEpoch_i": 1383713083, "_version_": 1450928330299670500 } ] } }'
        self.write(static_response)
        self.set_header('Content-type', 'application/json')
# instantiate a tornado web application with SolrHandler mapped to /update
application = tornado.web.Application([
    (r"/select", SolrHandler),
    (r"/shibboleet", AndroidTestHandler)
])


if __name__ == "__main__":
    #listen on port 3813
    #NOTE: Pebble -->  p. 38813 --> port 3813
    application.listen(3813)
    #run the IOLoop
    tornado.ioloop.IOLoop.instance().start()

