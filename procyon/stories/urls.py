from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView

from views import *

urlpatterns = patterns('',
                       url(r'^$', StoryViewList.as_view(), name='story-list'),
                       url(r'^(?P<pk>\d+)/?$', StoryDetailView.as_view(), name='story-detail'),
                       url(r'new/?$', create_new_story_post, name='story-detail-new'),
                       url(r'anthology/(?P<anthology>[a-zA-Z_,]+)?/?$', StoryViewList.as_view(), name='story-list-anthology'),

                       url(r'components/?$', StoryComponentViewList.as_view(), name='components-list'),
                       url(r'components/(?P<pk>\d+)/?$', StoryComponentDetailView.as_view(), name='component-detail'),
                       url(r'components/anthology/(?P<anthology>[a-zA-Z_,]+)?/?$', StoryComponentViewList.as_view(), name='components-list-anthology'),
                       url(r'components/new/?$', create_new_components_post, name='component-detail-new'),
                       )