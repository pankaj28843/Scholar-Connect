#!/usr/bin/env python
import math
import urllib2
import urllib
import mechanize
import urllib
import cookielib
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urlparse
import os
from operator import itemgetter, attrgetter

#proxies = {'http': 'http://10.3.100.211:8080'}

def calculate_distance(place1, place2):
    place2=place2.split()					#just splits the name of place into distinct words
    place_x=place2[0]						
    for  j in range(len(place2)-1):			#so place_x has the name of the university/place
        place_x=place_x+"+"+place2[j+1]
    place2=place_x
    print place2+"\n\n\n"

    place1=place1.split()					#just splits the name of place into distinct words
    place_x=place1[0]						
    for  j in range(len(place1)-1):			#so place_x has the name of the university/place
        place_x=place_x+"+"+place1[j+1]
    place1=place_x
    print place1+"\n\n\n"

    #note find the distance from second node onwards, wrt the first node always.. which is source here
    req = "http://query.yahooapis.com/v1/public/yql?q=select%20kilometers%20from%20geo.distance%20where%20place1%3D%22"+place1+"%22%20and%20place2%3D%22"+place2+"%22&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"

    #response = urllib.urlopen(req, proxies=proxies)
    response = urllib.urlopen(req,)
    page = response.read()
    page=page.decode('ascii', 'ignore')
    soup = BeautifulSoup(page)

    #distance=soup('kilometers')

    str2=soup('kilometers');  

    distance=(str2[0]).contents[0]
    print distance

    return float(distance)
