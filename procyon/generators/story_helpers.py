__author__ = 'jcrossler'

from procyon.stories.models import Component
import numpy
import json
from procyon.starsystemmaker.math_helpers import *
from procyon.starsystemmaker.name_library import *
from django.core.cache import cache


def turn_pattern_to_hash(pattern, override={}):
    pattern_parts = pattern.split(",")
    pattern_probability = []
    pattern_list = []
    pattern_prefixes = []
    for pattern_part in pattern_parts:
        pieces = pattern_part.split(":")
        type = pieces[0]
        weight = 1
        prefix = ' '
        if len(pieces) > 1:
            weight = pieces[1]
            try:
                weight = float(weight)
            except Exception:
                weight = 1

            if len(pieces) > 2:
                prefix = ' ' + pieces[2] + ' '

        if type in override:
            weight = 1

        pattern_list.append(type)
        pattern_probability.append(weight)
        pattern_prefixes.append(prefix)
    return pattern_list, pattern_probability, pattern_prefixes


def get(holder, variable, default):
    val = default
    if variable in holder:
        val = holder[variable]
    return val


def value_of_variable(var):
    val = 0
    if isinstance(var, basestring):
        var = var.lower().strip()
    else:
        var = 0

    if var == 'epic':
        val = 512
    elif var == 'fantastic':
        val = 256
    elif var == 'superb':
        val = 128
    elif var == 'great':
        val = 64
    elif var == 'good':
        val = 32
    elif var == 'fair':
        val = 16
    elif var == 'average':
        val = 8
    elif var == 'mediocre':
        val = 4
    elif var == 'poor':
        val = 2
    elif var == 'terrible':
        val = 1
    elif var == 'none':
        val = 0
    return val


def check_requirements(requirements, world, person):
    checks = []
    if isinstance(requirements, list):
        for req in requirements:
            concept = get(req, 'concept', 'world')
            name = get(req, 'name', '')
            r_has = get(req, 'has', '')
            r_exceeds = get(req, 'exceeds', '')
            r_below = get(req, 'below', '')
            r_is = get(req, 'is', '')
            if concept and name:

                if concept == 'city':
                    source = get(world, 'city', {})
                elif concept == 'family':
                    source = get(world, 'family', {})
                elif concept == 'character' or concept == 'person':
                    source = person
                else:
                    source = world

                to_check = get(source, name, '')

                if to_check:
                    if r_has and isinstance(to_check, list):
                        checks.append(r_has in to_check)

                    elif r_exceeds or r_below or r_is:
                        try:
                            to_check = value_of_variable(to_check)
                            to_check = float(to_check)
                            if r_exceeds:
                                r_exceeds = value_of_variable(r_exceeds)
                                r_exceeds = float(r_exceeds)
                                checks.append(r_exceeds <= to_check)
                            if r_below:
                                r_below = value_of_variable(r_below)
                                r_below = float(r_below)
                                checks.append(r_below >= to_check)
                            if r_is:
                                r_is = value_of_variable(r_is)
                                #TODO: Also check if strings and matches
                                r_is = float(r_is)
                                checks.append(r_is == to_check)
                        except Exception:
                            checks.append(False)
    is_valid = True
    for check in checks:
        if not check:
            is_valid = False

    return is_valid


def tags_to_find(tags, world, person):
    tags_list = tags.split(",")
    if world and 'tags' in world:
        world_tags = world.get('tags')
        tags_list = tags_list + world_tags.split(",")
    if person and 'tags' in person:
        person_tags = person.get('tags')
        tags_list = tags_list + person_tags.split(",")
    for idx, tag in enumerate(tags_list):
        tags_list[idx] = tag.strip().lower()

    return tags_list


def count_tag_matches(component_tags, search_tags, base_num=0):
    matches = base_num
    if isinstance(component_tags, basestring):
        tags = component_tags.split(",")
        for idx, tag in enumerate(tags):
            tags[idx] = tag.strip().lower()
        for tag in tags:
            if tag in search_tags:
                matches += 1

    return matches


def breakout_component_types(world, person, tags, pattern_list):
    component_types = {}
    component_tag_counts = {}

    active_components = cache.get('active_components', None)
    if not active_components:
        active_components = Component.objects.filter(active=True)
        cache.set('active_components', active_components)

    for component in active_components:
        ctype = str(component.type) or "None"
        ctype = ctype.lower().strip()

        if ctype in pattern_list:
            is_match = check_requirements(component.requirements, world, person)
            tags_searching = tags_to_find(tags, world, person)
            tag_match = count_tag_matches(component.tags, tags_searching)

            if is_match:
                if not ctype in component_types:
                    component_types[ctype] = []
                    component_tag_counts[ctype] = []
                component_types[ctype].append(component)
                component_tag_counts[ctype].append(tag_match)

    return component_types, component_tag_counts


def counts_to_probabilities(counts, padding=.3):

#TODO: Change weighting to 1/n

    total = 0
    probs = []
    try:
        padding = float(padding)
    except ValueError:
        return probs

    for count in counts:
        total += (count + padding)
    for count in counts:
        prob = float((count + padding) / float(total))
        probs.append(prob)

    return probs


def create_random_item(world={}, person={}, override={}, set_random_key=True, parse_dice=False,
                       pattern='adjective:.7,origin:.7,item:1,power:1:that,quirk:.9:and', tags="", rand_seed=None,
                       tag_weight=.3):
    # Build the random number seed
    if set_random_key:
        try:
            rand_seed = float(rand_seed)
        except Exception:
            rand_seed = numpy.random.random()
        rand_seed = set_rand_seed(rand_seed)
    note = ""

    pattern_list, pattern_probability, pattern_prefixes = turn_pattern_to_hash(pattern, override)

    component_types, component_tag_counts = breakout_component_types(world, person, tags, pattern_list)

    item_data = {}
    effects_data = []
    item_generators = []
    item_prefixes = []
    item_names = []

    for idx, ctype in enumerate(pattern_list):
        if numpy.random.random() <= pattern_probability[idx]:
            if ctype in component_types:
                components = component_types.get(ctype)
                if override and ctype in override:
                    # Use this component instead
                    component_name = override.get(ctype)
                    component = {"name": component_name}
                    for comp in components:
                        if comp.name == component_name:
                            component = comp
                            break

                else:
                    # Randomly pick a component
                    component_counts = component_tag_counts.get(ctype)

                    component_tag_probabilities = counts_to_probabilities(component_counts, padding=tag_weight)

                    option = numpy.random.choice(components, 1, p=component_tag_probabilities)
                    component = option[0]

                text = component.name
                if parse_dice:
                    text = parse_dice_text(text)

                item_prefixes.append(pattern_prefixes[idx])
                item_names.append(text)
                item_generators.append(ctype)

                if component.properties and isinstance(component.properties, dict):
                    properties = component.properties
                    item_data = dict(item_data.items() + properties.items())

                if component.effects and isinstance(component.effects, list) and len(component.effects):
                    effect = component.effects
                    effects_data += effect

    item_name = generate_item_name(item_prefixes, item_names)

    item_return = dict(name=item_name, data=item_data, effects=effects_data, note=note, rand_seed=rand_seed,
                       prefixes=item_prefixes, name_parts=item_names, generators=item_generators)
    return item_return


def generate_item_name(item_prefixes, item_names, titleize=False):
    name = ""
    for idx, item in enumerate(item_names):
        name += item_prefixes[idx] + item_names[idx]

    name = name.strip().capitalize()
    if titleize:
        name = name.title()

    return name


def create_random_name(world={}, person={}, override={}, pattern="", tags="", rand_seed=None,
                       modifications=0, set_random_key=True, tag_weight=.3, gender=""):
    # Build a pattern if it doesn't exist, based on time and asian/other influences - TODO: Expand these rules
    # Can do {"namefile":"european"} to force country

    if set_random_key:
        try:
            rand_seed = float(rand_seed)
        except Exception:
            rand_seed = numpy.random.random()
        rand_seed = set_rand_seed(rand_seed)
        set_random_key = False

    name_patterns = {}
    name_patterns['jon_snow'] = 'namefile:1,namefile:1'
    name_patterns['king_jon_snow_the_pierced'] = 'rank:.1,namefile:1,namefile:.7,adjective:.4:the'
    name_patterns['king_jon_tyrion_snow_of_winterfell'] = 'rank:.1,namefile:1,namefile:.7,namefile:.2,placefile:.4:of'
    name_patterns['jon_tyrion_snow'] = 'namefile:1,namefile:1,namefile:1'

    if not pattern:
        pattern = name_patterns[np.random.choice(name_patterns.keys(), 1)[0]]

        if 'year' in world:
            year = int(world.get('year'))
            if year < 1400:
                if numpy.random.random() < .5:
                    pattern = name_patterns['king_jon_snow_the_pierced']
                else:
                    pattern = name_patterns['king_jon_tyrion_snow_of_winterfell']
            elif year > 1900:
                pattern = name_patterns['jon_snow']
            else:
                pattern = name_patterns['jon_tyrion_snow']

    generated_item = create_random_item(world=world, person=person, override=override, pattern=pattern, tags=tags,
                                        rand_seed=rand_seed, set_random_key=set_random_key, tag_weight=tag_weight)

    for idx, generator in enumerate(generated_item.get('generators')):
        if generator == "namefile" or generator == "placefile":
            filename = generated_item['name_parts'][idx]
            restrictions = [filename]
            if gender:
                restrictions.append(gender)
            names = list_of_names(file_sub_strings=restrictions, prefix_chance=0)

            if len(names):
                generated_item['name_parts'][idx] = names[0]

    generated_item['name_parts'] = name_part_fuzzer(generated_item['name_parts'], modifications)

    generated_item['name'] = generate_item_name(generated_item['prefixes'], generated_item['name_parts'], titleize=True)

    generated_item['pattern'] = pattern

    return generated_item
