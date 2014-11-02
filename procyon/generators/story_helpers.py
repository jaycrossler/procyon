__author__ = 'jcrossler'

from procyon.stories.models import Component
import numpy
import json
from procyon.starsystemmaker.math_helpers import *


def turn_pattern_to_hash(pattern):
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
                prefix = pieces[2] + ' '

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
    for component in Component.objects.filter(active=True):
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


def counts_to_probabilities(counts, padding=1):
    total = 0
    probs = []
    for count in counts:
        total += (count + padding)
    for count in counts:
        prob = float((count + padding) / float(total))
        probs.append(prob)

    return probs


def create_random_item(world, person, pattern, tags, rand_seed):
    note = ""

    # Build the random number seed
    try:
        rand_seed = float(rand_seed)
    except Exception:
        rand_seed = numpy.random.random()
    rand_seed = set_rand_seed(rand_seed)

    pattern_list, pattern_probability, pattern_prefixes = turn_pattern_to_hash(pattern)

    component_types, component_tag_counts = breakout_component_types(world, person, tags, pattern_list)

    item = ''
    item_data = {}
    effects_data = []

    for idx, ctype in enumerate(pattern_list):
        if numpy.random.random() <= pattern_probability[idx]:
            if ctype in component_types:
                components = component_types.get(ctype)
                component_counts = component_tag_counts.get(ctype)

                component_tag_probabilities = counts_to_probabilities(component_counts)

                option = numpy.random.choice(components, 1, p=component_tag_probabilities)
                component = option[0]

                prefix = pattern_prefixes[idx]
                name = component.name
                item += prefix + name + " "

                if component.properties and isinstance(component.properties, dict):
                    properties = component.properties
                    item_data = dict(item_data.items() + properties.items())

                if component.effects and isinstance(component.effects, list) and len(component.effects):
                    effect = component.effects
                    effects_data += effect

    item = item.strip().capitalize()
    return item, item_data, effects_data, rand_seed, note