"""Command for sending the newsletter"""
from django.core.management.base import NoArgsCommand

from main.models import *
from crawl_data import create_confrence_profile

class Command(NoArgsCommand):
    """Create confrence profile for a profesor if it\'s not there"""
    help = 'Create confrence profile for a professor if it\'s not there'

    def handle_noargs(self, **options):
        verbose = int(options['verbosity'])

        if verbose:
            print 'Starts'
        
        conf = Confrence.objects.get(pk=1)
        
        for p in Professor.objects.all():
            try:
                cp = ConfrenceProfile.objects.get(professor = p, confrence = conf)
            except:
                cp = ConfrenceProfile(professor = p, confrence = conf, co_authors = '', cite_authors = '', ref_authors = '')
                cp.save()
                create_confrence_profile(p, conf)
        if verbose:
            print 'Ends'
