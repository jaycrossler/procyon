from django.contrib import messages
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models.loading import get_model

from procyon.starcatalog.models import *
#from datetime import datetime
#import logging
#import json

# Get an instance of a logger
#logger = logging.getLogger(__name__)

class StarViewList(ListView):
    model = Star
    paginate_by = 25
    template_name = 'star_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        cv = super(StarViewList, self).get_context_data(**kwargs)
        return cv
