from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'', include('main.urls')),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
)
