from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView

from procyon.starsystemmaker.views import *
from procyon.starsystemmaker.spacehelpers import *

urlpatterns = patterns('',
    url(r'^test/(?P<id>.*)$', generate_system),
    )