from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^addressbook/', include('pim.addressbook.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
)

