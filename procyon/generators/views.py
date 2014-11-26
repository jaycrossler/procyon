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
        world_data = json.loads(world_json) if world_json else {}
        override = json.loads(override_json) if override_json else {}

        for i in range(0, count):
            rand = rand_seed if i == 0 else ''
            item = story_helpers.create_random_item(world_data=world_data, override=override,
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

    metrics = []
    try:
        override = json.loads(override_json) if override_json else {}

        if not dna:
            dna, rand_seed = generate_dna(rand_seed=rand_seed, race=race, overrides=override)
        item_name = "Generated " + race + " DNA"

        qualities, attribute_mods = qualities_from_dna(dna)

        metrics = metrics_of_attributes()

    except ValueError, e:
        item_name = dna or "GATTACA"
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))
    except Exception, e:
        item_name = dna or "GATTACA"
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))

    if format_type == "json":
        data = json.dumps({"type": item_name, "dna": dna, "attributes": attribute_mods, "qualities": qualities})
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
                                    {"type": item_name, "dna": dna, "qualities": qualities, "note": note, "metrics": metrics,
                                     "attribute_mods": attribute_mods, "inputs": inputs, "generator": "dna",
                                     "RACE_ARRAY": RACE_ARRAY},
                                    RequestContext(request))
    return output


def generator_trap(request):
    return generator_default(request, generator_type="trap",
                             default_pattern="damage_adjective:1,damage_adjective:.6:and,weapon:1,trigger:1:triggered by")


def generator_name(request):
    format_type = request.REQUEST.get('format') or 'html'

    world_json = request.REQUEST.get('world_json') or ''
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
        world_data = json.loads(world_json) if world_json else {}
        override = json.loads(override_json) if override_json else {}
        count = int(count)
        modifications = int(modifications)
        if count < 1:
            count = 1
        if modifications < 0:
            modifications = 0

        for i in range(0, count):
            rand = rand_seed if i == 0 else ''
            item = story_helpers.create_random_name(world_data=world_data, override=override, pattern=pattern,
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
            "override_json": override_json
        }
        output = render_to_response('generator_generic.html',
                                    {"items": items, "inputs": inputs, "note": note, "generator": "name",
                                     "pattern_default": "rank:.1,namefile:1,namefile:.7,namefile:.2,placefile:.4:of"},
                                    RequestContext(request))
    return output


def generator_person(request):
    format_type = request.REQUEST.get('format') or 'html'

    world_json = request.REQUEST.get('world_json') or ''

    tags = request.REQUEST.get('tags') or ''
    rand_seed = request.REQUEST.get('rand_seed') or ''

    mother_dna = request.REQUEST.get('mother_dna') or ''
    mother_race = request.REQUEST.get('mother_race') or 'Human'
    mother_profession = request.REQUEST.get('mother_profession') or ''
    mother_education = request.REQUEST.get('mother_education') or ''
    mother_economic = request.REQUEST.get('mother_economic') or ''
    mother_conflict = request.REQUEST.get('mother_conflict') or ''
    mother = {"dna": mother_dna, "race": mother_race,  "profession": mother_profession, "education": mother_education, "economic": mother_economic, "conflict": mother_conflict}

    father_dna = request.REQUEST.get('father_dna') or ''
    father_race = request.REQUEST.get('father_race') or 'Human'
    father_profession = request.REQUEST.get('father_profession') or ''
    father_education = request.REQUEST.get('father_education') or ''
    father_economic = request.REQUEST.get('father_economic') or ''
    father_conflict = request.REQUEST.get('father_conflict') or ''
    father = {"dna": father_dna, "race": father_race,  "profession": father_profession, "education": father_education, "economic": father_economic, "conflict": father_conflict}

    gender = request.REQUEST.get('gender') or ''
    child_dna = request.REQUEST.get('child_dna') or ''

    regenerate = request.REQUEST.get('regenerate') or ''
    if regenerate:
        #A button was pushed with the name 'regenerate'
        rand_seed = ''

    try:
        world_data = json.loads(world_json) if world_json else {}

        person_data = story_helpers.create_person(world_data=world_data, father=father, mother=mother, child_dna=child_dna,
                                                  tags=tags, rand_seed=rand_seed, gender=gender)

        note = person_data.get('note')
        rand_seed = person_data.get('rand_seed')

    except ValueError, e:
        person_data = {"name": "Jon Snow", "description": "Male Human Ranger"}
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))
    except Exception, e:
        person_data = {"name": "Jon Snow", "description": "Male Human Ranger"}
        note = json.dumps(dict(error=500, message='Exception', details=traceback.format_exc(), exception=str(e)))

    if format_type == "json":
        data = json.dumps(person_data)
        output = HttpResponse(data, mimetype="application/json")

    elif format_type == "string":
        summary = person_data["name"] + " : " + person_data["description"]
        output = HttpResponse(summary, mimetype="text/html")

    else:
        inputs = {
            "tags": tags,
            "rand_seed": rand_seed,
            "gender": gender,
            "father": father,
            "mother": mother,
            "child_dna": child_dna,
            "world_json": world_json
        }
        output = render_to_response('generator_person_quick.html',
                                    {"person_data": person_data, "inputs": inputs, "note": note, "generator": "person",
                                     "RACE_ARRAY": RACE_ARRAY, "VALUE_ARRAY": VALUE_ARRAY},
                                    RequestContext(request))
    return output


def generator_city(request):
    return render_to_response('generator_city.html', {}, RequestContext(request))


def generator_solarsystem(request):
    return render_to_response('generator_list.html', {}, RequestContext(request))


def generator_planet(request):
    return render_to_response('generator_list.html', {}, RequestContext(request))
