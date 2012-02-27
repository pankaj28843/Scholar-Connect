from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('main.views',
                       (r'^$', 'index'),
                       (r'^dictionary/(?P<query>.*)/$', 'dictionary'),
                       (r'^add-new-professor/$', 'add_new_prof'),
                       (r'^professor-details/(?P<prof_id>\d+)/$', 'show_prof_details'),
                       (r'^map/(?P<cp_id>\d+)/$', 'show_map'),
                       (r'^map/(?P<cp_id>\d+)/(?P<count>\d+)/$', 'show_map'),
                       (r'^co-authors/(?P<cp_id>\d+)/$', 'show_co_authors'),
                       (r'^cite-authors/(?P<cp_id>\d+)/$', 'show_cite_authors'),
                       (r'^ref-authors/(?P<cp_id>\d+)/$', 'show_ref_authors'),
                       )
