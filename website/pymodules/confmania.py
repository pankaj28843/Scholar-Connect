

import sys
import re
import urllib
import urllib2
import urlparse
#import yahoo.yql
import pickle

from util import console, text
from yos.yql import db
from yos.boss import ysearch
from yos.crawl import rest

import confyql
import confImg

fp= open('UnivDatabase.db','r')
DATABASE= pickle.load(fp)
fp.close()

CONFERENCE= "WWW International Conference 2011"

## Write to the Database file,
def writeUnivtoDatabase(dbfile,domain,name,addr):

        fp= open(dbfile,'r')
        univ_dict= pickle.load(fp)
        fp.close()      

        univ_dict[domain] = {'name':name, 'addr':addr}          
                
        f = file(dbfile,'w')    
        pickle.dump(univ_dict, f)
        f.close()
        sys.exit()      

## checks whether Key has the keyword or not
def checkKeyExist( dbfile , keyword):

        fp= open(dbfile,'r')
        univ_dict= pickle.load(fp)
        fp.close()      
        
        for k in univ_dict:
                if keyword in k:
                        print k 
                        return True             
                                        
        return False    

def reportPubsYrs(url,odic):

        pub= rest.download(url)         
        yrs= ['2005','2006','2007','2008','2009','2010','2011']
        dic= {}
        for y in yrs:           
                dic[y]= max(int(pub.count(y)), odic[y] )
        return dic


# returns whether 'name' is co-author in prof's publications,
def whetherCoauthor(url, name):
        
        pub= rest.download(url)
        cnt= 0

        ## Use Regular expr- concept,
        cnt+= pub.count(name)           
        return 

def PubSearch(name,domain):
        
        pub= ysearch.search(name + " publications site:" + domain, count= 2, more={'type':'html','abstract':'long'})
        pub = db.create(name="pub", data= pub)
        
        ## for publication page extracted,
        yrs= ['2005','2006','2007','2008','2009','2010','2011']
        dic= {}
        for y in yrs:   
                dic[y]= 0

        for r in pub.rows:
                url = r["pub$url"]
                print 
                dic= reportPubsYrs(url,dic)
        
        return dic

## to get the Home Page of prof given his name and site:domain
def getHomePage(name,domain):

        ## Trucate the domain to remove www. leading
        dm= domain.split(".")                   
        domainsplt= dm[1]
        for dstr in dm[2:]:             
                domainsplt+= "."+dstr
        domain= domainsplt

        hm= ysearch.search("professor " + name + " site:"+domain, count= 1, more={'type':'html'})
        hm = db.create(name="hm", data= hm)
        
        ## assume single home-page 
        for r in hm.rows:       
                url = r["hm$url"]
                return url

        return None                     

# return the key with Max value
def findMax(hitdic):

        inverse = [(v,k) for k,v in hitdic.items()]
        return max(inverse)[1]          

def profData(name):

        dm_data = ysearch.search("Professor " + name, count= 3 )
        dmTb = db.create(name="prof", data= dm_data)


        ## Select the proper Domain Name from the Given Database Keys(), the Most HIT URL
        hitdic= {}
        for k in DATABASE.keys():
                hitdic[k]= 0
        
        #print "\nURL's returned: "
        for r in dmTb.rows:
                url= r["prof$url"]
                #print url

                ## for every domain saved,
                for k in DATABASE.keys():               
                        lt= k.split(".")
                        urllt= url.split(".") 

                        for e in lt[1:2]:
                                if e in urllt:
                                        hitdic[k]+=1
        
        ## Report the Domain with Maximum Hits  
        domain= findMax(hitdic) 

        return [name,domain]

## Render Details 
def renderDetails(name, univ , domain, img_name,f):
        
        f.write(name+","+univ+","+domain+","+img_name+"\n")


## Input Conf. Page and then, choose set of People concerned
def selectResearcher():

        conf_url = confyql.getConfAuthorPage("www.www2011india.com")
        #conf_url = confyql.getConfAuthorPage("http://nips.cc")

        print "Accepted Papers URL:"
        print conf_url
        
        '''

        ## Loading Author List, Dump into Authors.db
        
        query= "select content from html where url=\"http://www.www2011india.com/accepted_papers.html\" and xpath= \'//p\' "
        # query= "select content from html where url=\"" + conf_url + "\" and xpath= \'//p\' "
        confyql.getAuthors(query)
        
        f= open('Authors.db','r')
        athrLst= pickle.load(f)
        f.close()       

        '''     

###########################################################
## Calling Functions
'''
writeUnivtoDatabase('UnivDatabase.db','www.ust.hk','Hong Kong University','Hong Kong')

print checkKeyExist('UnivDatabase.db', 'ust')
sys.exit()

'''

#researchers= ['Saptarshi Ghosh ', 'Sudeshna Sarkar', 'Shivakant Mishra', 'Sanjeev Arora', 'Sui Huang']
#researchers= ['Shivakant Mishra', 'Kristina Lerman', 'Paolo Boldi', 'Mauro Passacant']
#researchers= [ 'Thomas Huang' ]

def collectData(name):

        tup= profData(name)
        name= tup[0]
        domain= tup[1]

        print name, domain
        hmpage = getHomePage(name,domain)
        #print "HomePage: "+ hmpage

        print hmpage
        #places= confyql.getPlaces( hmpage )
        #print "Places: "+ str(places)

        img_name= confImg.ImageSearch(name,domain)

        ## Write Details for Display purpose,
        #renderDetails(name, DATABASE[domain]['name'] , domain, str(img_name), f )
        
        ## Save the Details in data file
        univ_name= DATABASE[domain]['addr']     
        univ_addr= DATABASE[domain]['name']     

        if img_name<>None and hmpage<>None:     
                data= { 'image':str(img_name), 'domain':domain, 'hmpage':hmpage, 'university':univ_name, 'location':univ_addr, 'address': univ_addr }
                print data 
                return data
        else:
                return None


## Dump all Authors Data into Single file,
'''
f= open('Authors.db','r')
athrLst= pickle.load(f)
f.close()       


authdic= {}
## for every author name in Lst:
for name in athrLst:
        try:
                dt= collectData(name)
        except:
                continue

        if dt<>None:
                print str(athrLst.index(name)) + name + ": Data Added"
                authdic[name]= dt
                f= open('AuthorsData.db','w')
                pickle.dump(authdic,f)
                f.close()

'''

'''
## Update Database
def updateDB(name):
                
        f= open('AuthorsDataUpdated.db','r')
        curDic= pickle.load(f)
        f.close()
        
        if name in curDic.keys():
                print name+": already present"
                return

        dt= collectData(name)
        curDic[name]= dt

        print "Data Added for "+ name

        f= open('AuthorsDataUpdated.db','w')
        pickle.dump(curDic,f)
        f.close()

def deleteDB(name):

        f= open('AuthorsDataUpdated.db','r')
        curDic= pickle.load(f)
        f.close()
        
        if name not in curDic.keys():
                print name+": not present"              
        
        curDic.pop(name)
        
        print "Data Deleted for "+ name

        f= open('AuthorsDataUpdated.db','w')
        pickle.dump(curDic,f)
        f.close()

#updateDB( "Fernando Peruani" )
updateDB( "Bivas Mitra" )
updateDB( "Jie Yang" )
updateDB( "Scott Shenker" )
'''

collectData("Niloy ganguly")

