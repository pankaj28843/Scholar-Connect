import mechanize
import urllib
import cookielib
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urlparse
from html2text import html2text

MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
    ]

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


def search_for_month(string):
    for m in MONTHS:
        if m in string:
            return True
    return False

class GoogleScholarSearch:

    def __init__(self):
        """
        @brief Empty constructor.
        """
        self.SEARCH_HOST = "scholar.google.com"
        self.SEARCH_BASE_URL = "/scholar"

    def getACMPaperDetails(self, url):    
        br_1 = br
        br_1.open(url)
        html = br_1.response().read()
        html = html.decode('ascii', 'ignore')
        soup = BeautifulSoup(html)

        paper_details = {'authors':None,'title':None}
        paper_details['title'] = soup.find('div', {'class': 'large-text'}).first('h1').first('strong').contents[0]
        authors = []
        
        for record in soup('td', {'valign':'top'}):
            try:
                author = record.first('a',{'title':"Author Profile Page"}).contents[0]
                authors.append(html2text(author).strip())
            except:
                continue
        paper_details['authors'] = authors
        return paper_details

    def search(self, terms, limit=1000, since=1960, before=2011, cp=None ):   
        params = urllib.urlencode({'q': "+".join(terms), 'num': limit, 'as_ylo':since, 'as_yhi':before})
        url = "http://"+self.SEARCH_HOST+self.SEARCH_BASE_URL+"?"+params

        br_2 = br
        r = br_2.open(url)
        
        html = br.response().read()
        html = html.decode('ascii', 'ignore')
        soup = BeautifulSoup(html)
        citations = 0
        for record in soup('div', {'class': 'gs_r'}):
            pubURL = ''
            pubDetails = {'authors':None,'title':None}
            pubCitations = []
            pubReferences = []

            try:
                pubURL = record.first('a')['href']
                print pubURL
            except:
                continue

            
            if urlparse(record.first('a')['href']).netloc == 'portal.acm.org':              
                url_1 = record.first('a')['href']
                pubDetails = self.getACMPaperDetails(url_1)

                
                sp = pubURL.split('citation.cfm')
                url_1 = sp[0]+'tab_citings.cfm'+sp[1]+'&usebody=tabbody&_cf_containerId=citedby'
                br_1 = br
                
                br_1.open(url_1)
                html_1 = br_1.response().read()
                html_1 = html_1.decode('ascii', 'ignore')
                soup_1 = BeautifulSoup(html_1)
                
                for record in soup_1('td'):
                    try:
                        url_2 = BeautifulSoup(str(record.first('div'))).first('a')['href']
                        pubCitations.append(self.getACMPaperDetails(url_2))
                    except:
                        continue
                
                sp = pubURL.split('citation.cfm')
                url_1 = sp[0]+'tab_references.cfm'+sp[1]+'&usebody=tabbody&_cf_containerId=references&type='
                print url_1
                br_1 = br
                
                br_1.open(url_1)
                html_1 = br_1.response().read()
                html_1 = html_1.decode('ascii', 'ignore')
                soup_1 = BeautifulSoup(html_1)
                
                for record in soup_1('td'):
                    try:
                        url_2 = BeautifulSoup(str(record.first('div'))).first('a')['href']
                        pubReferences.append(self.getACMPaperDetails(url_2))
                    except:
                        continue
                        
                co_auth = ''
                cite_auth = ''
                ref_auth = ''
                
                co_auth = str(pubDetails['title']) + '|' + ','.join(pubDetails['authors'])
                co_auth = co_auth.encode('ascii', 'ignore')
                if co_auth != '':
                    if cp.co_authors == '':
                        cp.co_authors = co_auth
                        cp.save()
                    else:
                        cp.co_authors = cp.co_authors + ';' + co_auth
                        cp.save()

                cite_auth_set = []
                for c in pubCitations:
                    cite_auth_set.append(str(c['title'])+'|'+','.join(c['authors']))
                cite_auth = cite_auth + ';'.join(cite_auth_set)
                cite_auth = cite_auth.encode('ascii', 'ignore')
                if cite_auth != '':
                    if cp.cite_authors == '':
                        cp.cite_authors = cite_auth
                        cp.save()
                    else:
                        cp.cite_authors = cp.cite_authors + ';' + cite_auth
                        cp.save()
                
                ref_auth_set = []
                for r in pubReferences:
                    ref_auth_set.append(str(r['title'])+'|'+','.join(r['authors']))
                ref_auth = ref_auth + ';'.join(ref_auth_set)
                ref_auth = ref_auth.encode('ascii', 'ignore')
                
                if ref_auth != '':
                    if cp.ref_authors == '':
                        cp.ref_authors = ref_auth
                        cp.save()
                    else:
                        cp.ref_authors = cp.ref_authors + ';' + ref_auth
                        cp.save()

        return True
