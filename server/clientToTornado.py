'''
mock-up of the pebblewire client, for testing purposes

'''

import urllib2
import time
import urllib

#form query
lastUpdate = int(time.time() - 200000)
query = "http://localhost:3813/update?q=" + urllib.quote('timestampEpoch_i:[{0} TO *]'.format(lastUpdate)) + "&wt=json"
print "My query is: " + query

#send request
request = urllib2.Request(url=query)
request.add_header('Content-type', 'application/json')
requestResponse = urllib2.urlopen(request)

print requestResponse.read()
