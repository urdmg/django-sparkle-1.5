#from django.conf.urls.defaults import *
from django.conf.urls import *

urlpatterns = patterns('sparkle.views',
    url(r'^(?P<application_slug>[\w-]+)/appcast.xml$', 'appcast', name='sparkle_application_appcast'),
)
