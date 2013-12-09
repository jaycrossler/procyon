from django.conf.urls import patterns, include, url

from procyon.starsystemmaker.views import *
from procyon.starsystemmaker.space_helpers import *
from procyon.starsystemmaker.test_helpers import *

urlpatterns = patterns('',
    url(r'^test1/(?P<mean>.*)$', test_generate_rand_nums),
    url(r'^(?P<mean>.*)/test2.png$', test_generate_rand_nums_as_image),
    url(r'^(?P<weight>.*)/test3.png$', test_generate_rand_range_as_image),
    url(r'^task_colors/(?P<force>.*)$', create_some_star_colors),
    url(r'^rerandomize/(?P<pk>\d+)$', create_star_extended_data_rerandomize, name='maker-star-build-reset-rand' ),
    url(r'^initialize/(?P<pk>\d+)$', create_star_extended_data, name='maker-star-build' ),
    url(r'^star/(?P<pk>\d+)$', lookup_star_info_prime, name='maker-star-info' ),
    url(r'^star/created/(?P<pk>\d+)$', lookup_star_info, name='maker-star-info-createdid' ),
    url(r'^viewer/(?P<pk>\d+)$', star_viewer, name='maker-star-viewer' ),
    )