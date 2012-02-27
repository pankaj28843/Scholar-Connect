from main.models import *
import urllib2
import urllib
import settings

def get_lat_lon(location):
    latlon = {}

    try:
        proxies = settings.PROXIES
    except:
        proxies = {'http': 'http://10.3.100.211:8080'}
        
    url = "http://where.yahooapis.com/geocode?location=" + location

    try:
        response = urllib.urlopen(url)
    except:
        response = urllib.urlopen(url, proxies=proxies)

    page = response.read()
    parsi = page.split('>')#start parsing

    ii=1
    for d in parsi:
        if 'lati' in d:
            ii=ii+1
            if ii==3:
                m=d.rsplit('<')
                latlon['lattitude'] = m[0]

    ii=1
    for d in parsi:
        if 'long' in d:
            ii=ii+1
            if ii==3:
                m=d.rsplit('<')
                latlon['longitude'] = m[0]
    return latlon


def create_person(name, location):
    latlon = get_lat_lon(location)
    p = Person(name=name, location=location, lattitude=latlon['lattitude'], longitude=latlon['longitude'])
    p.save()
