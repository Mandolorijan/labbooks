from django.conf.urls import patterns, url, include
from models import Measurement, JournalEntry, CurrentSetting
from django.views.generic import ListView
from django.http import HttpResponseRedirect

import clustof.views

urlpatterns = patterns('',
    url(r'^readsettings/$', 'clustof.views.readsettings'),
    url(r'^newmeasurement/$', 'clustof.views.newmeasurement'),
    url(r'^view/$', ListView.as_view(model = Measurement, template_name = 'clustof/measurement_list.html', paginate_by = 100)),
    url(r'^insight/(?P<parameter1>\w+)/(?P<parameter2>\w+)/$', 'clustof.views.plot_parameters'),
    url(r'^insight/$', lambda x: HttpResponseRedirect('extraction_1/extraction_2/')),
    url(r'^insight/(?P<parameter1>\w+)/$', 'clustof.views.plot_parameters'),
    url(r'^journal/$', ListView.as_view(model = JournalEntry, template_name = 'clustof/journalentry_list.html')),
    url(r'^$', 'django.contrib.flatpages.views.flatpage', {'url': '/clustof/'}, name='clustofhome'),
    url(r'^export/(\d+)/$', 'clustof.views.exportfile'),
)
