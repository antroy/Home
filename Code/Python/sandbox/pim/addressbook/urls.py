from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'pim.addressbook.views.index', ),
    (r'^(?P<contact_id>\d+)/$', 'pim.addressbook.views.detail', ),
)

