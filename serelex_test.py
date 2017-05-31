import requests

req = requests.get("http://www.serelex.org/find/en-patternsim-ukwac-wiki/scooter")
res = req.json()

try:
	print [rx[u'word'].encode('ascii', 'ignore') for rx in res[u'relations'][:5]]
	# print res[u'relations'][:5]
except:
	pass
