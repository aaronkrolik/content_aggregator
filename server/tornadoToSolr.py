'''
Tornado server handling requests from clients by fetching from Solr
'''

import tornado.ioloop
import tornado.web
import urllib2

class SolrHandler(tornado.web.RequestHandler):
    def get(self):
        query = "http://localhost:8983/solr/collection1/select?" + self.request.query
        print "Tornado queries Solr: " + query

        #get request from Solr
        req = urllib2.Request(url=query)
        req.add_header('Content-type', 'application/json')
        f = urllib2.urlopen(req)
        
        #send request back to client
        self.write(f.read())
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Origin','*')
 

# instantiate a tornado web application with SolrHandler mapped to /update
application = tornado.web.Application([
    (r"/select", SolrHandler),
])


if __name__ == "__main__":
    #listen on port 3813
    #NOTE: Pebble -->  p. 38813 --> port 3813
    application.listen(3813)
    #run the IOLoop
    tornado.ioloop.IOLoop.instance().start()

