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
# import logging
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


class StoryComponentViewList(SearchView, ListView):
    model = Component
    paginate_by = 100
    template_name = 'component_list.html'
    context_object_name = 'components'
    search_fields = ['id', 'name', 'anthology', 'tags', 'type']

    def get_queryset(self):
        components = Component.objects.filter(active=True)
        if 'anthology' in self.kwargs:
            anthology = str(self.kwargs['anthology']) or ""
            if len(anthology) > 0:
                anthology_list = anthology.split(",")
                components = components.filter(anthology__in=anthology_list)
        return components

    def get_context_data(self, **kwargs):
        cv = super(StoryComponentViewList, self).get_context_data(**kwargs)
        if 'anthology' in self.kwargs:
            anthology = str(self.kwargs['anthology']) or ""
            if len(anthology) > 0:
                anthology_list = anthology.split(",")
                cv['anthologies'] = ", ".join(anthology_list)
        return cv


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


class StoryComponentDetailView(DetailView):
    http_method_names = ['post', 'get']
    model = Component
    template_name = 'component_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StoryComponentDetailView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        component = get_object_or_404(Component, id=self.kwargs.get('pk'))

        try:
            if request.POST.get('effects'):
                effects = json.dumps(request.POST.get('effects'))
            else:
                effects = None

            if request.POST.get('requirements'):
                requirements = json.dumps(request.POST.get('requirements'))
            else:
                requirements = None

            if request.POST.get('properties'):
                properties = json.dumps(request.POST.get('properties'))
            else:
                properties = None

            anthology = request.POST.get('anthology')
            name = request.POST.get('name')
            type = request.POST.get('type')
            tags = request.POST.get('tags')
            active = True

            phrase_list = []
            list_of_phrases = request.POST.get('list_of_phrases')
            if isinstance(list_of_phrases, basestring) and len(list_of_phrases) and list_of_phrases.startswith('['):
                #It's likely a JSON array of strings
                phrases = json.loads(list_of_phrases)
                if isinstance(phrases, list):
                    phrase_list = phrases
            elif isinstance(list_of_phrases, basestring) and len(list_of_phrases) and '\n' in list_of_phrases:
                phrases = list_of_phrases.split('\n')
                if isinstance(phrases, list):
                    phrase_list = phrases

            elif isinstance(list_of_phrases, basestring) and len(list_of_phrases):
                phrases = list_of_phrases.split(",")
                if isinstance(phrases, list):
                    phrase_list = phrases

            if len(phrase_list) < 1:
                phrase_list.append(name)

            ids_of_added = []
            for phrase in phrase_list:
                name = phrase.strip()
                if len(phrase_list) == 1:

                    if name and not name == 'tags-update':
                        component.name = name

                    if effects:
                        component.effects = effects
                    if requirements:
                        component.requirements = requirements
                    if properties:
                        component.properties = properties

                    if anthology:
                        component.anthology = anthology
                    if type:
                        component.type = type
                    if tags:
                        component.tags = tags
                    if active:
                        component.active = True

                    component.save()
                    ids_of_added.append(component.id)
                else:
                    # Multiple were added. Instead of updating, add new ones
                    component = Component(name=name, anthology=anthology, type=type, tags=tags, active=active,
                                          effects=effects, requirements=requirements, properties=properties)
                    component.save()
                    ids_of_added.append(component.id)

            result = {"status": "OK", "message": "updated", "ids": ids_of_added, "input_count": len(phrase_list),
                      "added_count": len(ids_of_added)}
        except Exception, e:
            import traceback

            result = dict(status="Error!", error=500, message='Generic Exception',
                          details=traceback.format_exc(), exception=str(e))

        return HttpResponse(json.dumps(result, ensure_ascii=True), mimetype="application/json")


def create_new_story_post(request):
    story_body = request.body
    try:
        story_data = json.loads(story_body)

        anthology = story_data.get('anthology')
        name = 'New Story'
        stype = story_data.get('type')
        tags = story_data.get('tags')
        active = True
        force_usage = 0
        year_min = int(story_data.get('year_min'))
        year_max = int(story_data.get('year_max'))

        story = Story(name=name, anthology=anthology, type=stype, tags=tags, active=active, force_usage=force_usage,
                      year_min=year_min, year_max=year_max)
        story.save()

        result = {"status": "OK", "message": "updated", "id": story.id}
    except Exception, e:
        import traceback

        result = dict(status="Error!", error=500, message='Generic Exception',
                      details=traceback.format_exc(), exception=str(e))

    return HttpResponse(json.dumps(result, ensure_ascii=True), mimetype="application/json")


def create_new_components_post(request):
    story_body = request.body
    try:
        component_data = json.loads(story_body)

        anthology = component_data.get('anthology')
        name = 'New Component'
        ctype = component_data.get('type')
        tags = component_data.get('tags')
        active = True

        component = Component(name=name, anthology=anthology, type=ctype, tags=tags, active=active)
        component.save()

        result = {"status": "OK", "message": "updated", "id": component.id}
    except Exception, e:
        import traceback

        result = dict(status="Error!", error=500, message='Generic Exception',
                      details=traceback.format_exc(), exception=str(e))

    return HttpResponse(json.dumps(result, ensure_ascii=True), mimetype="application/json")
