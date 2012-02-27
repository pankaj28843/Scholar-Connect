#!/usr/bin/env python
# Corey Goldberg, April 2007 (corey@goldb.org)
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





proxies = {'http': 'http://10.3.100.211:8080'}


marker_size = 50
zoom_level = 14
height = '550px' 
width = '800px' 
center = 'Topeka, KS'  # city or zip
map_type = 'YAHOO_MAP_REG'  # YAHOO_MAP_REG, YAHOO_MAP_SAT, YAHOO_MAP_HYB 



fh = open('geo_output.html', 'w')

fh.write("""\
    <html>
    <head>
        <title>Geolocation Map</title>
        <script type="text/javascript" 
            src="http://api.maps.yahoo.com/ajaxymap?v=3.0&appid=YD-eQRpTl0_JX2E95l_xAFs5UwZUlNQhhn7lj1H">
        </script>
        <style type="text/css">
            body { padding: 0; margin: 0; }
            #mapContainer { height: %s; width: %s; }
        </style>
    </head>
    <body>
    <div id="mapContainer"></div>
        <script type="text/javascript">


            function createYahooMarker(rank,geopoint, size,prof_name, latitude, longitude,distance,marker_name,initial) { 
                    var myImage = new YImage();

            myImage.src = marker_name             
            myImage.size = new YSize(size, size);

            var marker = new YMarker(geopoint, myImage);    

            
            document.write("<p>"+rank+" <b>Prof. </b>"+prof_name+" ,  <b>Location </b>"+geopoint+" , "+distance+ "<b> kms</b></p>");

            
            marker.addAutoExpand("rank="+rank+" prof. name is "+prof_name+" and the distance of "+geopoint+" from "+initial+" is "+distance);
            var markerMarkup = "<b>You can add markup this</b>";
                markerMarkup += "<i> easy</i>";
            
            return marker; 
            }
            
            var map = new  YMap(document.getElementById('mapContainer'), %s);
            map.addPanControl(); 
            map.addZoomLong(); 
            map.drawZoomAndCenter("%s", %d);""" % (height, width, map_type, center, zoom_level))






place1=""
place2=""
distance=""
str2=""





class professor:
    def __init__(self, name, place, lat,longi,distance,parse_name,i_name,d_name):       #parse name "a dobr"=> "a_dobr"
        self.name = name
        self.place = place
        self.lat = lat
        self.longi=longi
        self.distance=distance
        self.parse_name=parse_name
        self.i_name=i_name
        self.d_name=d_name
    
    def __repr__(self):
        return repr((self.name, self.place, self.lat, self.longi,self.distance,self.parse_name,self.i_name,self.d_name))




li=[]
print li
initial=""
i=0
fd_in = open('./loc_output', 'r')

# construct the list

lines = fd_in.readlines()
proffs = []
univs = []
lats = []
longs = []
doms = []
imgs = []

for i in range(len(lines)):
    if i%6 == 0:
        proffs.append(lines[i])
    elif i%6 == 1:
        univs.append(lines[i])
    elif i%6 == 2:
        lats.append(lines[i])
    elif i%6 == 3:
        longs.append(lines[i])
    elif i%6==4:
        doms.append(lines[i])
    elif i%6==5:
        imgs.append(lines[i])



        
for ii in range(len(proffs)):
    prof_name=proffs[ii]
    univ=univs[ii]
    latitude=lats[ii]
    longitude=longs[ii]
    image_name=doms[ii]
    domain_name=imgs[ii]


    univ=univ.strip('\n')
    prof_name=prof_name.strip('\n')
    latitude=latitude.strip('\n')
    longitude=longitude.strip('\n')
    image_name=image_name.strip('\n')
    domain_name=domain_name.strip('\n')

    if ii==0:

        place1=univ
        place1=place1.split()                   #just splits the name of place into distinct words
        print place1
        place_x=place1[0]                   
        for  j in range(len(place1)-1):         #so place_x has the name of the university/place
            place_x=place_x+"+"+place1[j+1]
        place1=place_x
        distance="0"
        initial=univ
    else:
        place2=univ
        print "debg"+place2
        place2=place2.split()                   #just splits the name of place into distinct words
        place_x=place2[0]                       
        for  j in range(len(place2)-1):         #so place_x has the name of the university/place
            place_x=place_x+"+"+place2[j+1]
        place2=place_x
        print place2+"\n\n\n"


        #note find the distance from second node onwards, wrt the first node always.. which is source here
        req = "http://query.yahooapis.com/v1/public/yql?q=select%20kilometers%20from%20geo.distance%20where%20place1%3D%22"+place1+"%22%20and%20place2%3D%22"+place2+"%22&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"

        response = urllib.urlopen(req, proxies=proxies)
        page = response.read()
        page=page.decode('ascii', 'ignore')
        soup = BeautifulSoup(page)

        #distance=soup('kilometers')

        str2=soup('kilometers');  

        distance=(str2[0]).contents[0]
        print "distance"+distance

    prof_parse=prof_name
    tt=prof_parse.split()
    #print tt
    prof_parse=tt[0]
    for i in range(len(tt)-1):
        prof_parse=prof_parse+"_"+tt[i+1]

    image_name="images/"+image_name 



    dd=professor(prof_name, univ,latitude, longitude,int(distance),prof_parse,image_name, domain_name)
    #print dd 
    li.append(dd)       




li=sorted(li, key=lambda pr: pr.distance)



j=0


for x in li:
    j=j+1

    #get the name of the extension of the file f.format
    print x.parse_name
    cmd = 'ls images/ | grep '+x.parse_name.split('/')[-1]+' | cut -d . -f 2'
    #print cmd
    format=str(os.popen(cmd).read())
    #print 'Format: '+format
    x.parse_name=x.parse_name+'.'+format.strip()
    #print x.parse_name
    fh.write("map.addOverlay(new createYahooMarker('%s','%s', %s,'%s','%s','%s','%s','%s','%s'))\n" %(j,x.place, marker_size,x.name,x.lat, x.longi,x.distance,x.i_name, initial))

       
fh.write("""\
    </script>
    </body>
    </html>""")



