import pickle, datetime
from main.models import *
import settings

from pymodules.google_scholar_search import GoogleScholarSearch

def create_confrence_profile(prof, confrence, papers_count=1000, start_year=1960):
    prof = prof    
    co_auth = ''
    cite_auth = ''
    ref_auth = ''

    try:
        cp = ConfrenceProfile.objects.get(professor = prof, confrence = confrence)
        cp.co_authors = co_auth
        cp.cite_authors = cite_auth
        cp.ref_authors = ref_auth
        cp.save()
    except:
        cp = ConfrenceProfile(professor = prof, confrence = confrence, co_authors = co_auth, cite_authors = cite_auth, ref_authors = ref_auth)
        cp.save()

    search = GoogleScholarSearch()
    search.search([prof.name], papers_count, start_year, datetime.datetime.now().year, cp)
    
    return True
