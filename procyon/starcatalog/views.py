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
        search_term = self.request.GET.get(self.search_term_parameter, self.search_term)

        queryset = super(SearchView, self).get_queryset()

        if search_term:
            search_query = []
            for field in self.search_fields:
                if field == 'id':
                    search_query.append(Q(**{field+'__{search_type}'.format(search_type='exact'): search_term}))
                else:
                    search_query.append(Q(**{field+'__{search_type}'.format(search_type=self.search_type): search_term}))

            if search_query:
                queryset = queryset.filter(reduce(operator.or_, search_query))

        return queryset


class StarViewList(SearchView, ListView):
    model = Star
    paginate_by = 100
    template_name = 'star_list.html'
    context_object_name = 'items'
    search_fields = ['id', 'HD', 'proper_name', 'gliese', 'HIP', 'HR', ]

    def get_context_data(self, **kwargs):
        cv = super(StarViewList, self).get_context_data(**kwargs)
        return cv

@csrf_exempt
def StarTypeView(request):
    callback = request.GET.get('callback')
    dumps = []
    for star in StarType.objects.all():
        dumps.append(star.get_params())
    if callback:
        output = '{0}({1});'.format(callback, json.dumps(dumps))
    else:
        output = json.dumps(dumps)

    return HttpResponse(output, content_type="application/json")


def lookup_star_info(request, pk):
    callback = request.GET.get('callback')

    try:
        star = get_object_or_404(Star, id=pk)
        dumps = star.get_params()

    except Exception as e:
        dumps = {'status': 'error', 'details': str(e)}

    output = json.dumps(dumps)
    if callback:
        output = '{0}({1});'.format(callback, output)

    return HttpResponse(output, content_type="application/json")
