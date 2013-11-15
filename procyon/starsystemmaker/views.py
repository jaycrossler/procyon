from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
import json

from procyon.starcatalog.models import *


def process_star_colors(request, force):

    result_info = "Results:<br/>"
    for s in Star.objects.filter(pk__lt=1000):
        result = s.create_star_model(force)
        result_info += str(s.id) + ":" + result + "<br/>"

    return HttpResponse(result_info, content_type="text/html")


