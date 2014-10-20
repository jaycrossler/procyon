from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView

from views import *

urlpatterns = patterns('',
    url(r'^$', StoryViewList.as_view(), name='story-list'),
    url(r'^(?P<pk>\d+)/?$', StoryDetailView.as_view(), name='story-detail'),
    )