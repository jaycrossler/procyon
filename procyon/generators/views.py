from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render_to_response
from django.core import exceptions
import json
import story_helpers
import traceback

from django.template import RequestContext


def generator_list(request):
    return render_to_response('generators_list.html', {}, RequestContext(request))


def generator_item(request):
    format_type = request.REQUEST.get('format') or 'html'

    world_json = request.REQUEST.get('world_json') or ''
    person_json = request.REQUEST.get('person_json') or ''
    override_json = request.REQUEST.get('override_json') or ''

    pattern = request.REQUEST.get('pattern') or 'adjective:.7,origin:.7,item:1,power:1:that,quirk:.9:and'
    tags = request.REQUEST.get('tags') or ''
    rand_seed = request.REQUEST.get('rand_seed') or ''
    regenerate = request.REQUEST.get('regenerate') or ''
    if regenerate:
        #A button was pushed with the name 'regenerate'
        rand_seed = ''

    item_data = {}
    effects_data = []

    try:
        world = json.loads(world_json) if world_json else {}
        person = json.loads(person_json) if person_json else {}
        override = json.loads(override_json) if override_json else {}
        # if world_json:
        #     world = json.loads(world_json)
        # else:
        #     world = {}
        #
        # if person_json:
        #     person = json.loads(person_json)
        # else:
        #     person = {}
        #
        # if override_json:
        #     override = json.loads(override_json)
        # else:
        #     override = {}

        item, item_data, effects_data, rand_seed, note = story_helpers.create_random_item(world, person, override,
                                                                                          pattern, tags, rand_seed)

        item_data = json.dumps(item_data) if item_data else None
        effects_data = json.dumps(effects_data) if effects_data else None
        # if item_data:
        #     item_data = json.dumps(item_data)
        # else:
        #     item_data = None
        # if effects_data:
        #     effects_data = json.dumps(effects_data)
        # else:
        #     effects_data = None

    except ValueError:
        item = "Random Item"
        note = "Improper JSON variables passed in"
    except Exception, e:
        item = "Random Item"
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))

    if format_type == "json":
        data = json.dumps(dict(name=item, data=item_data, effects=effects_data, note=note))
        output = HttpResponse(data, mimetype="application/json")

    elif format_type == "string":
        output = HttpResponse(item, mimetype="text/html")

    else:
        output = render_to_response('generator_item.html', {"item": item,
                                                            "item_data": item_data,
                                                            "effects_data": effects_data,
                                                            "pattern": pattern,
                                                            "tags": tags,
                                                            "rand_seed": rand_seed,
                                                            "world_json": world_json,
                                                            "person_json": person_json,
                                                            "override_json": override_json,
                                                            "note": note},
                                    RequestContext(request))
    return output


def generator_name(request):
    format_type = request.REQUEST.get('format') or 'html'

    world_json = request.REQUEST.get('world_json') or ''
    person_json = request.REQUEST.get('person_json') or ''
    override_json = request.REQUEST.get('override_json') or ''

    pattern = request.REQUEST.get('pattern') or ''
    tags = request.REQUEST.get('tags') or ''
    rand_seed = request.REQUEST.get('rand_seed') or ''
    regenerate = request.REQUEST.get('regenerate') or ''
    if regenerate:
        #A button was pushed with the name 'regenerate'
        rand_seed = ''

    item_data = {}
    try:
        world = json.loads(world_json) if world_json else {}
        person = json.loads(person_json) if person_json else {}
        override = json.loads(override_json) if override_json else {}

        item, item_data, rand_seed, note = story_helpers.create_random_name(world, person, override,
                                                                            pattern, tags, rand_seed)

        item_data = json.dumps(item_data) if item_data else None

    except ValueError:
        item = "Jon Snow"
        note = "Improper JSON variables passed in"
    except Exception, e:
        item = "Jon Snow"
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))

    if format_type == "json":
        data = json.dumps(dict(name=item, data=item_data, note=note))
        output = HttpResponse(data, mimetype="application/json")

    elif format_type == "string":
        output = HttpResponse(item, mimetype="text/html")

    else:
        output = render_to_response('generator_name.html', {"item": item,
                                                            "item_data": item_data,
                                                            "pattern": pattern,
                                                            "tags": tags,
                                                            "rand_seed": rand_seed,
                                                            "world_json": world_json,
                                                            "person_json": person_json,
                                                            "override_json": override_json,
                                                            "note": note},
                                    RequestContext(request))
    return output


def generator_solarsystem(request):
    return render_to_response('generators_list.html', {}, RequestContext(request))


def generator_planet(request):
    return render_to_response('generators_list.html', {}, RequestContext(request))
