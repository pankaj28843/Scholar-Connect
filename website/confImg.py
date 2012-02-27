
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
#from yos.crawl import rest

def search(pattern, text):
	
	if re.search(pattern,text,re.IGNORECASE)<>None:
		return True
	else:
		return False

## checking relevance of Name and filename
def checkRelevance(name,fname):
	
	## Check for punctuation characters
	punc= string.punctuation
	for i in range(len(punc)):
		if punc[i]<>'.' and punc[i]<>'_' and fname.find(punc[i])<>-1:
			return False	
		

	## Searching for Substring of Name,
	nmlst= name.split(" ")
	rel= False
	for n in nmlst:				
		if search(n,fname):	
			return True

	## Search for Initials,
	initial= ""
	for n in nmlst:		
		initial+= n[0]
	if search(initial,fname):	
		return True

	return False

## Does the Image search on Name of professor,
'''
def ImageSearch(name, domain):

	## Trucate the domain to remove www. leading
	dm= domain.split(".")			
	domainsplt= dm[1]
	for dstr in dm[2:]:		
		domainsplt+= "."+dstr
	domain= domainsplt
	
	imgData= ysearch.search(name + " site:"+domain, vertical="images",count= 10)
	#imgData= ysearch.search(name, vertical="images",count= 10)

	imgTb = db.create(name="img", data= imgData)
	#imgTb.describe()

	prof_parse= name
	tt=prof_parse.split()
	print tt
	prof_parse=tt[0]
	for i in range(len(tt)-1):
		prof_parse=prof_parse+"_"+tt[i+1]
		
	name= prof_parse
	
	cnt= 0	
	for r in imgTb.rows:

		fname= r["img$filename"]
		furl= r["img$url"]

		#console.write( "Format:%s\nTitle:%s\nURL:%s\nFilename:%s\n" % (r["img$format"],r["img$title"], r["img$url"],r["img$filename"]) )
		# Show Relevant Images
		if checkRelevance(name,fname):
			cnt+=1		
			format= r["img$format"] 		
			fp= open("images/"+name+str(cnt)+'.'+format,'w')
			fp.write(urllib.urlopen(furl).read())
			fp.close()
			
			console.write( "Format:%s\nTitle:%s\nURL:%s\nFilename:%s\n" % (r["img$format"],r["img$title"], r["img$url"],r["img$filename"]) )
	
'''

## Image Search,
## returns the name of file saved, in /images folder

def ImageSearch(name, domain):
	
	## Trucate the domain to remove www. leading
	dm= domain.split(".")			
	domainsplt= dm[1]
	for dstr in dm[2:]:		
		domainsplt+= "."+dstr
	domain= domainsplt

	#url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+ urllib.quote(name) +'+site:'+ domain)
	url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+ urllib.quote(name) )
	request = urllib2.Request(url, None, {'Referer': 'abc.com'})
	response = urllib2.urlopen(request)
	
	# Process the JSON string.
	results = (json.loads(response.read()))['responseData']['results']

	## Returns the Most relevant Image
	cnt= 0
	for i in results:	
			
		fname= i['url'].split("/")[-1]
		if checkRelevance(name,fname):
			cnt+=1
			#print fname 			
			fp= open("images/"+fname,'w')
			fp.write(urllib.urlopen(i['url']).read())
			fp.close()	
			return fname
	return None










