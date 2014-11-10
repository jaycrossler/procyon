from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView

from views import *

urlpatterns = patterns('',
                       url(r'^$', generator_list, name='generators-list'),
                       url(r'item/?$', generator_item, name='item-generator'),
                       url(r'name/?$', generator_name, name='name-generator'),
                       url(r'trap/?$', generator_trap, name='trap-generator'),
                       url(r'junk/?$', generator_junk, name='junk-generator'),

                       url(r'solarsystem/?$', generator_solarsystem, name='solarsystem-generator'),
                       url(r'planet/?$', generator_item, name='plan-generator'),
                       url(r'person/?$', generator_item, name='person-generator'),
                       url(r'city/?$', generator_item, name='city-generator'),
                       )