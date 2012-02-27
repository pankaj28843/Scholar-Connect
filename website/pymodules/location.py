#given a input file, finds the latitude and longitude of the place
import urllib2
import urllib
import confImg 


proxies = {'http': 'http://10.3.100.211:8080'}

fd_in = open('./loc_input', 'r')
fd_out = open('./loc_output', 'w')

i=0;

for line in fd_in.readlines():
    line= line.strip()    
    info=line.split(',')
    print info

    t=info[1]

    place=t.split()	#just splits the name of place into distinct words

    print info[0]
    print info[2]

    place_x=place[0]
    for  j in range(len(place)-1):			#so place_x has the name of the university/place
	    place_x=place_x+"+"+place[j+1]

    req = "http://where.yahooapis.com/geocode?location="+place_x    #berekeley"
    response = urllib.urlopen(req, proxies=proxies)
    page = response.read()

    parsi=page.split('>')		            #start parsing

    fd_out.write(info[0]+"\n")				#print name of prof
    fd_out.write(place_x.replace("+"," ")+"\n")	#print the location

    ii=1
    for d in parsi:
        if 'lati' in d:
            ii=ii+1
            if ii==3:
	            m=d.rsplit('<')
	            fd_out.write(m[0]+"\n")		# print latitude first

    ii=1
    for d in parsi:
        if 'long' in d:
            ii=ii+1
            if ii==3:
	            m=d.rsplit('<')
	            fd_out.write(m[0]+"\n")		#print longitude then

    fd_out.write(info[3]+"\n")
    fd_out.write(info[2]+"\n")       

