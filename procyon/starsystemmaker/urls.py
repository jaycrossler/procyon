from django.conf.urls import patterns, include, url

from procyon.starsystemmaker.views import *
from procyon.starsystemmaker.space_helpers import *
from procyon.starsystemmaker.test_helpers import *

urlpatterns = patterns('',
    url(r'^test1/(?P<mean>.*)$', test_generate_rand_nums),
    url(r'^(?P<mean>.*)/test2.png$', test_generate_rand_nums_as_image),
    url(r'^(?P<weight>.*)/test3.png$', test_generate_rand_range_as_image),
    url(r'^task_colors/(?P<force>.*)$', process_star_colors),
    )