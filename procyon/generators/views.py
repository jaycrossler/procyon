from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render_to_response
from django.core import exceptions
from dna_helpers import *
import json
import story_helpers
import traceback

from django.template import RequestContext


def generator_list(request):
    return render_to_response('generators_list.html', {}, RequestContext(request))


def generator_default(request, generator_type="item", parse_dice=False,
                      default_pattern='adjective:.7,origin:.7,item:1,power:1:that,quirk:.9:and'):

    format_type = request.REQUEST.get('format') or 'html'

    world_json = request.REQUEST.get('world_json') or ''
    person_json = request.REQUEST.get('person_json') or ''
    override_json = request.REQUEST.get('override_json') or ''

    pattern = request.REQUEST.get('pattern') or default_pattern
    count = request.REQUEST.get('count') or 20
    tags = request.REQUEST.get('tags') or ''
    tag_weight = request.REQUEST.get('tag_weight') or 0.3
    rand_seed = request.REQUEST.get('rand_seed') or ''

    regenerate = request.REQUEST.get('regenerate') or ''
    if regenerate:
        #A button was pushed with the name 'regenerate'
        rand_seed = ''
    count = int(count)
    if count < 1:
        count = 1

    first_item = {}
    items = []

    try:
        world = json.loads(world_json) if world_json else {}
        person = json.loads(person_json) if person_json else {}
        override = json.loads(override_json) if override_json else {}

        for i in range(0, count):
            rand = rand_seed if i == 0 else ''
            item = story_helpers.create_random_item(world=world, person=person, override=override,
                                                    pattern=pattern, tags=tags, rand_seed=rand,
                                                    tag_weight=tag_weight, parse_dice=parse_dice)
            if i == 0:
                first_item = item
            items.append(item)

        # first_item['data'] = json.dumps(first_item.get('data')) if first_item.get('data') else None
        item_name = first_item.get('name')
        note = first_item.get('note')
        rand_seed = first_item.get('rand_seed')

    except ValueError:
        item_name = "Random " + generator_type
        note = "Improper JSON variables passed in - Value Error"
    except Exception, e:
        item_name = "Random " + generator_type
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))

    if format_type == "json":
        data = json.dumps(first_item)
        output = HttpResponse(data, mimetype="application/json")

    elif format_type == "string":
        output = HttpResponse(item_name, mimetype="text/html")

    else:
        inputs = {
            "pattern": pattern,
            "tags": tags,
            "tag_weight": tag_weight,
            "rand_seed": rand_seed,
            "count": count,
            "world_json": world_json,
            "person_json": person_json,
            "override_json": override_json
        }
        output = render_to_response('generator_generic.html',
                                    {"items": items, "inputs": inputs, "note": note, "generator": generator_type,
                                     "pattern_default": default_pattern},
                                    RequestContext(request))
    return output


def generator_item(request):
    return generator_default(request, generator_type="item",
                             default_pattern="adjective:.7,origin:.7,item:1,power:1:that,quirk:.9:and")


def generator_junk(request):
    return generator_default(request, generator_type="junk", default_pattern="junk:1", parse_dice=True)


def generator_dna(request):
    format_type = request.REQUEST.get('format') or 'html'

    override_json = request.REQUEST.get('override_json') or ''

    rand_seed = request.REQUEST.get('rand_seed') or ''
    race = request.REQUEST.get('race') or ''
    dna = request.REQUEST.get('dna') or ''
    note = ''
    qualities = []
    attribute_mods = {}

    regenerate = request.REQUEST.get('regenerate') or ''
    if regenerate:
        #A button was pushed with the name 'regenerate'
        rand_seed = ''

    try:
        override = json.loads(override_json) if override_json else {}

        if not dna:
            dna, rand_seed = generate_dna(rand_seed=rand_seed, race=race, overrides=override)
        item_name = "Generated " + race + " DNA"

        qualities, attribute_mods = qualities_from_dna(dna)

    except ValueError, e:
        item_name = dna or "GATTACA"
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))
    except Exception, e:
        item_name = dna or "GATTACA"
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))

    if format_type == "json":
        data = json.dumps({"type": item_name, "dna": dna, "attributes": attribute_mods})
        output = HttpResponse(data, mimetype="application/json")

    elif format_type == "string":
        output = HttpResponse(dna, mimetype="text/html")

    else:
        inputs = {
            "rand_seed": rand_seed,
            "race": race,
            "override_json": override_json
        }
        output = render_to_response('generator_dna.html',
                                    {"type": item_name, "dna": dna, "qualities": qualities,
                                     "attribute_mods": attribute_mods, "inputs": inputs, "note": note, "generator": "dna"},
                                    RequestContext(request))
    return output


def generator_trap(request):
    return generator_default(request, generator_type="trap",
                             default_pattern="damage_adjective:1,damage_adjective:.6:and,weapon:1,trigger:1:triggered by")


def generator_name(request):
    #TODO: Have names of different regions
    #TODO: Have different namefiles of male or female

    format_type = request.REQUEST.get('format') or 'html'

    world_json = request.REQUEST.get('world_json') or ''
    person_json = request.REQUEST.get('person_json') or ''
    override_json = request.REQUEST.get('override_json') or ''

    pattern = request.REQUEST.get('pattern') or ''
    tags = request.REQUEST.get('tags') or ''
    tag_weight = request.REQUEST.get('tag_weight') or 0.3
    rand_seed = request.REQUEST.get('rand_seed') or ''
    count = request.REQUEST.get('count') or 20

    modifications = request.REQUEST.get('modifications') or 1
    gender = request.REQUEST.get('gender') or ''

    regenerate = request.REQUEST.get('regenerate') or ''
    if regenerate:
        #A button was pushed with the name 'regenerate'
        rand_seed = ''

    first_item = {}
    items = []
    try:
        note = gender
        world = json.loads(world_json) if world_json else {}
        person = json.loads(person_json) if person_json else {}
        override = json.loads(override_json) if override_json else {}
        count = int(count)
        modifications = int(modifications)
        if count < 1:
            count = 1
        if modifications < 0:
            modifications = 0

        for i in range(0, count):
            rand = rand_seed if i == 0 else ''
            item = story_helpers.create_random_name(world=world, person=person, override=override, pattern=pattern,
                                                    tags=tags, rand_seed=rand, modifications=modifications,
                                                    tag_weight=tag_weight, gender=gender)
            if i == 0:
                first_item = item
            items.append(item)

        first_item['data'] = json.dumps(first_item.get('data')) if first_item.get('data') else None
        item_name = first_item.get('name')
        note = first_item.get('note')
        rand_seed = first_item.get('rand_seed')

    except ValueError, e:
        item_name = "Jon Snow"
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))
    except Exception, e:
        item_name = "Jon Snow"
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))

    if format_type == "json":
        data = json.dumps(first_item)
        output = HttpResponse(data, mimetype="application/json")

    elif format_type == "string":
        output = HttpResponse(item_name, mimetype="text/html")

    else:
        inputs = {
            "pattern": pattern,
            "tags": tags,
            "rand_seed": rand_seed,
            "modifications": modifications,
            "gender": gender,
            "count": count,
            "tag_weight": tag_weight,
            "world_json": world_json,
            "person_json": person_json,
            "override_json": override_json
        }
        output = render_to_response('generator_generic.html',
                                    {"items": items, "inputs": inputs, "note": note, "generator": "name",
                                     "pattern_default": "rank:.1,namefile:1,namefile:.7,namefile:.2,placefile:.4:of"},
                                    RequestContext(request))
    return output


def generator_city(request):
    return render_to_response('generators_city.html', {}, RequestContext(request))


def generator_person(request):
    return render_to_response('generators_person.html', {}, RequestContext(request))


def generator_solarsystem(request):
    return render_to_response('generators_list.html', {}, RequestContext(request))


def generator_planet(request):
    return render_to_response('generators_list.html', {}, RequestContext(request))
