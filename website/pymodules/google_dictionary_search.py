import mechanize
import urllib
import cookielib
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urlparse
from html2text import html2text

def dictionary_search(word):
    # Browserstripogram
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)


    #br.set_proxies({"http": "10.3.100.212:8080",})
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    url = "http://www.google.com/dictionary?aq=f&langpair=en|en&q=" + word + "&hl=en"
    r = br.open(url)
    html = br.response().read()
    html = html.decode('ascii', 'ignore')
    soup = BeautifulSoup(html)

    return html2text(str(soup('div', {'class':'dct-srch-rslt',})[0]))

if __name__ == '__main__':
    print search("hello")
