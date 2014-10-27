from django.contrib.auth.decorators import login_required
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
from models import *
# from datetime import datetime
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
                    search_query.append(Q(**{field + '__{search_type}'.format(search_type='iexact'): search_term}))
                else:
                    search_query.append(
                        Q(**{field + '__{search_type}'.format(search_type=self.search_type): search_term}))

            if search_query:
                queryset = queryset.filter(reduce(operator.or_, search_query))

        return queryset


class StoryViewList(SearchView, ListView):
    model = Story
    paginate_by = 100
    template_name = 'story_list.html'
    context_object_name = 'stories'
    search_fields = ['id', 'name', 'anthology', 'tags', 'type']

    def get_queryset(self):
        stories = Story.objects.filter(active=True)
        if 'anthology' in self.kwargs:
            anthology = str(self.kwargs['anthology']) or ""
            if len(anthology) > 0:
                anthology_list = anthology.split(",")
                stories = stories.filter(anthology__in=anthology_list)
        return stories

    def get_context_data(self, **kwargs):
        cv = super(StoryViewList, self).get_context_data(**kwargs)
        if 'anthology' in self.kwargs:
            anthology = str(self.kwargs['anthology']) or ""
            if len(anthology) > 0:
                anthology_list = anthology.split(",")
                cv['anthologies'] = ", ".join(anthology_list)
        return cv


class StoryDetailView(DetailView):
    http_method_names = ['post', 'get']
    model = Story
    template_name = 'story_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StoryDetailView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        story = get_object_or_404(Story, id=self.kwargs.get('pk'))

        story_body = request.body
        try:
            story_data = json.loads(story_body)

            story.choices = json.dumps(story_data.get('choices'))
            story.requirements = json.dumps(story_data.get('requirements'))
            story.story = json.dumps(story_data.get('story'))
            story.variables = json.dumps(story_data.get('variables'))
            #story.images = json.dumps(story_data.get('images'))

            story.description = story_data.get('description')
            story.anthology = story_data.get('anthology')
            story.name = story_data.get('name')
            story.type = story_data.get('type')
            story.tags = story_data.get('tags')
            story.active = bool(story_data.get('active'))
            story.force_usage = int(story_data.get('force_usage'))
            story.max_times_usable = int(story_data.get('max_times_usable'))
            story.times_used = int(story_data.get('times_used'))
            story.year_min = int(story_data.get('year_min'))
            story.year_max = int(story_data.get('year_max'))

            story.save()
            result = {"status": "OK", "message": "updated"}
        except Exception, e:
            import traceback

            result = dict(status="Error!", error=500, message='Generic Exception',
                          details=traceback.format_exc(), exception=str(e))

        return HttpResponse(json.dumps(result, ensure_ascii=True), mimetype="application/json")

