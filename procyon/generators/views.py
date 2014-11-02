from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render_to_response
from django.core import exceptions
import json
import story_helpers
from django.template import RequestContext

def generator_list(request):

    return render_to_response('generators_list.html', {}, RequestContext(request))


def generator_item(request):
    world_json = request.REQUEST.get('world_json') or ''
    person_json = request.REQUEST.get('person_json') or ''
    pattern = request.REQUEST.get('pattern') or 'adjective:.7,origin:.7,item:1,power:1:that,quirk:.9:and'
    tags = request.REQUEST.get('tags') or ''
    rand_seed = request.REQUEST.get('rand_seed') or ''
    regenerate = request.REQUEST.get('regenerate') or ''
    if (regenerate):
        rand_seed = ''

    item_data = {}
    effects_data = []

    try:
        if world_json:
            world = json.loads(world_json)
        else:
            world = {}

        if person_json:
            person = json.loads(person_json)
        else:
            person = {}

        item, item_data, effects_data, rand_seed, note = story_helpers.create_random_item(world, person, pattern, tags, rand_seed)

        if item_data:
            item_data = json.dumps(item_data)
        else:
            item_data = None

        if effects_data:
            effects_data = json.dumps(effects_data)
        else:
            effects_data = None


    except ValueError:
        item = "Random Item"
        note = "Improper JSON variables passed in"
    except Exception, e:
        item = "Random Item"
        import traceback
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))

    return render_to_response('generator_item.html', {"item": item,
                                                      "item_data": item_data,
                                                      "effects_data": effects_data,
                                                      "pattern": pattern,
                                                      "tags": tags, "rand_seed": rand_seed,
                                                      "world_json": world_json, "person_json": person_json, "note": note},
                              RequestContext(request))


def generator_name(request):

    return render_to_response('generators_list.html', {}, RequestContext(request))


def generator_solarsystem(request):

    return render_to_response('generators_list.html', {}, RequestContext(request))


def generator_planet(request):

    return render_to_response('generators_list.html', {}, RequestContext(request))
