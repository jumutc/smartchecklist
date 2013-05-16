from django.conf.urls.defaults import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^get_simple_checklist', 'SmartChecklist.views.get_simple_checklist', name='get_simple_checklist'),
    url(r'^create_checklist', 'SmartChecklist.views.create_checklist', name='create_checklist'),
    url(r'^get_delimited', 'SmartChecklist.views.get_delimited', name='get_delimited'),
    url(r'^send_checklist', 'SmartChecklist.views.send_checklist', name='send_checklist'),
    url(r'^checklist', 'SmartChecklist.views.checklist', name='checklist'),
    url(r'^activate_user', 'SmartChecklist.views.activate_user'),
    url(r'^contact_us', 'SmartChecklist.views.contact_us'),
    url(r'^check_done', 'SmartChecklist.views.check_done'),
    url(r'^statistics', 'SmartChecklist.views.statistics'),
    url(r'^last_page', 'SmartChecklist.views.last_page'),
    url(r'^join_now', 'SmartChecklist.views.join_now'),
    url(r'^my_desk', 'SmartChecklist.views.my_desk'),
    url(r'^history', 'SmartChecklist.views.history'),
    url(r'^details', 'SmartChecklist.views.details'),
    url(r'^offers', 'SmartChecklist.views.offers'),
    url(r'^stores', 'SmartChecklist.views.stores'),
    url(r'^index', 'SmartChecklist.views.index'),
    url(r'^$', 'SmartChecklist.views.first_page'),

    url(r'^store_admin', 'SmartChecklist.views.store_admin'),

    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': 'last_page.html'}),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)