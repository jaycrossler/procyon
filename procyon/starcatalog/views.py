from django.contrib import messages
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models.loading import get_model
import operator
from procyon.starcatalog.models import *
#from datetime import datetime
#import logging
#import json

# Get an instance of a logger
#logger = logging.getLogger(__name__)


class SearchView(object):
    search_fields = list()
    search_term = None
    search_type = 'icontains'
    search_term_parameter = 'q'

    def get_queryset(self):
        search_query = []
        search_term = self.request.GET.get(self.search_term_parameter, self.search_term)

        queryset = super(SearchView, self).get_queryset()

        for field in self.search_fields:
            search_query.append(Q(**{field+'__{search_type}'.format(search_type=self.search_type): search_term}))

        if search_query and search_term:
            queryset = queryset.filter(reduce(operator.or_, search_query))

        return queryset


class StarViewList(SearchView, ListView):
    model = Star
    paginate_by = 25
    template_name = 'star_list.html'
    context_object_name = 'items'
    search_fields = ['proper_name', 'gliese', 'HIP', 'HD', ]

    def get_context_data(self, **kwargs):
        cv = super(StarViewList, self).get_context_data(**kwargs)
        return cv
