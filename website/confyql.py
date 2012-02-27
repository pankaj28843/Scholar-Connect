import sys
import re
import urllib
import urllib2
import urlparse
import simplejson
import json
import string

from util import console, text
from yos.yql import db
from yos.boss import ysearch
from yos.crawl import rest

import confImg


# Yahoo! YQL API
PUBLIC_API_URL  = 'http://query.yahooapis.com/v1/public/yql'
OAUTH_API_URL   = 'http://query.yahooapis.com/v1/yql'
DATATABLES_URL  = 'store://datatables.org/'

'''
YQL queries:
----------------------------------------------
WWW conference Page: 
	select content from html where url="http://www.www2011india.com/accepted_papers.html" and xpath='//p'

'''

def getConfAuthorPage(conf_page):

	url= ('https://ajax.googleapis.com/ajax/services/search/web?' + 'v=1.0&q='+ urllib.quote("Accepted papers")+ '+site:'+ conf_page)
	#print url

	request = urllib2.Request(url, None, {'Referer': 'abc.com'})
	response = urllib2.urlopen(request)
	
	# Process the JSON string.
	results = (json.loads(response.read()))['responseData']['results']
	for i in results:			
		url= i['url']
		if confImg.search("accepted",url) and confImg.search("paper",url):
			return url				

## Get AuthorsList from Conference web-page
def getAuthors(query):

	qurl= PUBLIC_API_URL + '?' + urllib.urlencode({ 'q': query, 'format': 'json', 'env': DATATABLES_URL })	
	qdata= rest.load(qurl)
	authors= []

	for ele in qdata['query']['results']['p']:
		try:
			ele= ele.strip()		
			ele= ele.split(",")
			if len(ele)> 1:
				lst= ele.pop(-1)
				lst= lst.split("and")
				ele.extend(lst)
				authors.extend(ele)
		except:
			continue

	f = file('Authors.db','w')
	pickle.dump(authors, f)
	f.close()


## Get List of Places associated with a prof. from his home-page
def getPlaces(hmpage):

	query= "SELECT match.place.name FROM geo.placemaker WHERE documentURL = \"" + hmpage + "\" AND documentType=\"text/plain\" "
	placeurl= PUBLIC_API_URL + '?' + urllib.urlencode({ 'q': query, 'format': 'json', 'env': DATATABLES_URL })	
	placedata= rest.load(placeurl)	

	places= []		
	try:
		
		for p in placedata["query"]["results"]["matches"]:
			#print p["match"]["place"]["name"]
			places.append(p["match"]["place"]["name"])
		return places	
	except:
		return places


	
		
	











