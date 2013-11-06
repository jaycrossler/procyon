from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView

#from starcatalog.models import *
from starcatalog.forms import *
from starcatalog.views import *

urlpatterns = patterns('',
    url(r'^$', StarViewList.as_view(), name='star-list'),
    url(r'^star/$', StarViewList.as_view(), name='star-list-no-id'),
    )