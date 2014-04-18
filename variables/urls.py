from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
from portal.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('variables.views',
    # Examples:
    url(r'^test_json$','test_json'),
urlpatterns += staticfiles_urlpatterns()


)

