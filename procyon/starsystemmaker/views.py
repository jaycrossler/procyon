from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
import json

from procyon.starcatalog.models import *
from procyon.starsystemmaker.test_helpers import *


@timeit
def process_star_colors(request, force):

    for s in Star.objects.filter(pk__lt=1000):
        s.create_star_model(force)
    result_info = "Done"

    return HttpResponse(result_info, content_type="text/html")


