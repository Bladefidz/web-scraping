'''
Controlling TOR via stem. TOR Controller on port 9051.
Bypassing request data to Proxify which is HTTP proxy server on port 8118.
Then, proxify sending the request data to TOR network which is SOCK5 server.
'''

import stem
import stem.connection
import time
import urllib.request as req
from stem import Signal
from stem.control import Controller

# initialize some HTTP headers
# for later usage in URL requests
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent':user_agent}

# initialize some holding variables
oldIP = "0.0.0.0"
newIP = "0.0.0.0"

# Number of IP addresses to iterate
numIP = 3

# Time in second needed between IP address checks
timeIPCheck = 2

# Send request
def request(url):
	def _setUrlProxy():
		proxySupport = req.ProxyHandler({"http": "127.0.0.1:8118"})
		opener = req.build_opener(proxySupport)
		req.install_opener(opener)
	_setUrlProxy()
	request = req.Request(url, None, headers)  # Request via proxy
	return req.urlopen(request).read()

# Send new connection signal to TOR
def renewConnection():
	with Controller.from_port(port = 9051) as controller:
		controller.authenticate(password = "h0l4hupp")
		controller.signal(Signal.NEWNYM)
		controller.close()


# Rotating IP addresses
renewConnection()
newIP = request("http://icanhazip.com/").decode().rstrip()
for i in range(numIP):
	oldIP = newIP
	renewConnection()
	newIP = request("http://icanhazip.com/").decode().rstrip()

s = 0  # Time elapsed to check IP addresses
# Do loop until we get new IP address which is different with oldIP value
while oldIP == newIP:
	time.sleep(timeIPCheck)
	s += timeIPCheck
	newIP = request("http://icanhazip.com/").decode().rstrip()
	print("%d seconds elapsed awaiting a different IP address." % s)
print("")
print("newIP: %s" % newIP)