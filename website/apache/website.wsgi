import os, sys
sys.path.append('/home/pankaj/django_projects/confrence/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
