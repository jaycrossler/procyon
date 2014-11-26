__author__ = 'jcrossler'

import numpy
import json
from procyon.starsystemmaker.math_helpers import *
from procyon.starsystemmaker.name_library import *
import dna_helpers

try:
    from django.core.cache import cache
    from django.forms.models import model_to_dict
except ImportError:
    # Probably Django not loaded, include for testing
    pass


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
    val = var
    if isinstance(var, basestring):
        var = var.lower().strip()

        lookups = {'epic': 144.0, 'fantastic': 89.0, 'superb': 55.0, 'great': 34.0, 'good': 21.0, 'high': 13.0,
                   'fair': 8.0, 'average': 5.0, 'medium': 5.0, 'moderate': 5.0, 'mediocre': 3.0,
                   'low': 3.0, 'poor': 2.0, 'terrible': 1.0, 'tiny': 0.1, 'none': 0.0}
        if var in lookups:
            val = lookups[var]
        try:
            val = float(var)
        except ValueError:
            pass

    else:
        try:
            val = float(var)
        except ValueError:
            pass
        except TypeError:
            pass

    return val


def convert_string_to_req_object(requirements):
    reqs = str(requirements)

    if len(reqs) < 3:
        return []

    reqs = reqs.split(",")
    reqs = [req.strip() for req in reqs]

    output = []
    for req in reqs:
        if " >= " in req:
            req_part = req.split(" >= ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "exceeds": req_part[1].strip()})

        elif " <= " in req:
            req_part = req.split(" <= ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "below": req_part[1].strip()})

        elif " > " in req:
            req_part = req.split(" > ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), ">": req_part[1].strip()})

        elif " < " in req:
            req_part = req.split(" < ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "<": req_part[1].strip()})

        elif " has " in req:  # Check that it's not in quotes
            req_part = req.split(" has ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "has": req_part[1].strip()})

        elif " = " in req:
            req_part = req.split(" = ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "is": req_part[1].strip()})

        elif " == " in req:
            req_part = req.split(" == ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "is": req_part[1].strip()})

        elif " is " in req:  # TODO: Check that it's not in quotes
            req_part = req.split(" is ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "is": req_part[1].strip()})

        elif req.endswith(" none"):
            req_part = req.split(" none")
            output.append({"requirement": req_part[0].strip(), "empty": req_part[0].strip()})

        elif req.endswith(" empty"):
            req_part = req.split(" empty")
            output.append({"requirement": req_part[0].strip(), "empty": req_part[0].strip()})

        elif req.endswith(" doesn't exist"):
            req_part = req.split(" doesn't exist")
            output.append({"requirement": req_part[0].strip(), "empty": req_part[0].strip()})

        elif req.endswith(" exists"):
            req_part = req.split(" exists")
            output.append({"requirement": req_part[0].strip(), "exists": req_part[0].strip()})

        elif req.endswith(" exist"):
            req_part = req.split(" exist")
            output.append({"requirement": req_part[0].strip(), "exists": req_part[0].strip()})

        else:  # Assume that it's an exists check
            output.append({"requirement": req.strip(), "exists": req.strip()})

    return output


def get_info_from_name_array(req_array, data_array, return_closest_match=False):
    pointer = data_array
    for req in req_array:
        if req.lower() == 'count' and isinstance(pointer, list):
            pointer = len(pointer)
        elif req.lower() == 'length' and isinstance(pointer, list):
            pointer = len(pointer)
        elif req in pointer:
            pointer = pointer.get(req)
        else:
            if return_closest_match:
                pass
            else:
                return False
    # TODO, Handle if arrays and * is passed in
    return pointer


def check_requirements(requirements, world_data):
    # Allow: [{concept:person,name:age,exceeds:20},{concept:world,name:magic,below:poor}]
    # Allow: 'magic > low, building has Church'
    # Allow: 'person.age > 20, world.magic < poor, person.business exists, person.siblings empty'

    if not requirements:
        return True

    checks = []
    if isinstance(requirements, basestring):
        if len(requirements) < 4:
            return True
        else:
            requirements = convert_string_to_req_object(requirements)

    if isinstance(requirements, list):
        for req in requirements:
            concept = get(req, 'concept', '')
            name = get(req, 'name', '')
            requirement = get(req, 'requirement', '')
            req_array = []
            if requirement and isinstance(requirement, list):
                req_array = requirement
            elif requirement and isinstance(requirement, basestring):
                req_array = requirement.split(".")
            elif concept and name:
                req_array = [concept, name]
            elif name:
                req_array = [name]

            r_is = get(req, 'is', '')
            r_exists = get(req, 'exists', '')
            r_has = get(req, 'has', '')
            r_exceeds = get(req, 'exceeds', '')
            r_empty = get(req, 'empty', '')
            r_below = get(req, 'below', '')
            r_gt = get(req, '>', '')
            r_lt = get(req, '<', '')

            if req_array:
                to_check = get_info_from_name_array(req_array, world_data)

                if not to_check:
                    if r_empty:
                        checks.append(True)
                    else:
                        checks.append(False)
                else:
                    if r_has and isinstance(to_check, list):
                        checks.append(r_has in to_check)  # TODO: Check for lower case and plural

                    elif r_exceeds or r_below or r_is or r_gt or r_lt or r_exists or r_empty:
                        try:
                            to_check = value_of_variable(to_check)
                            if r_exceeds:
                                r_exceeds = value_of_variable(r_exceeds)
                                checks.append(r_exceeds <= to_check)
                            if r_gt:
                                r_gt = value_of_variable(r_gt)
                                checks.append(r_gt < to_check)
                            if r_lt:
                                r_lt = value_of_variable(r_lt)
                                checks.append(r_lt > to_check)
                            if r_below:
                                r_below = value_of_variable(r_below)
                                r_below = float(r_below)
                                checks.append(r_below >= to_check)
                            if r_is:
                                try:
                                    temp = value_of_variable(r_is)
                                    r_is = float(temp)
                                    checks.append(r_is == to_check)
                                except ValueError:
                                    if isinstance(r_is, basestring) and isinstance(to_check, basestring):
                                        checks.append(r_is.lower() == to_check.lower())
                                    else:
                                        checks.append(r_is == to_check)

                            if r_exists:
                                checks.append(not to_check == False)

                        except Exception:
                            checks.append(False)
    else:
        return False

    is_valid = False
    if checks:
        is_valid = all(item for item in checks)

    return is_valid


def tags_to_find(tags, world_data):
    tags_list = tags.split(",")
    if world_data and 'tags' in world_data:
        world_tags = world_data.get('tags', '')
        tags_list = tags_list + world_tags.split(",")
    if 'person' in world_data:
        person = world_data.get('person', {})
        if person and 'tags' in person:
            person_tags = person.get('tags', '')
            tags_list = tags_list + person_tags.split(",")
    if 'family' in world_data:
        family = world_data.get('family', {})
        if family and 'tags' in family:
            family_tags = family.get('tags', '')
            tags_list = tags_list + family_tags.split(",")

    for idx, tag in enumerate(tags_list):
        tags_list[idx] = tag.strip().lower()

    return tags_list


def count_tag_matches(component_tags=list(), weighting=10.0, search_tags=list(), base_num=0.0):

    matches = float(base_num) + float(weighting)/10

    if isinstance(component_tags, basestring):
        if len(component_tags) < 1:
            return matches
        component_tags = component_tags.split(",")

    seen = set()
    for n in search_tags:
        if n not in seen:
            seen.add(n)

    for n in component_tags:
        n = n.strip().lower()
        if n in seen:
            matches += 1

    return matches


def breakout_component_types(world_data, tags, pattern_list):
    component_types = {}
    component_tag_counts = {}
    active_components = []

    try:
        from procyon.stories.models import Component

        active_components = cache.get('active_components', None)
        if not active_components:
            all_components = Component.objects.filter(active=True)

            active_components = []
            for component in all_components:
                new_component = model_to_dict(component)

                r = component.requirements
                if ((r.startswith("{") and r.endswith("}")) or (r.startswith("[") and r.endswith("]"))) and len(r) > 4:
                    try:
                        r = json.dumps(r)
                    except ValueError:
                        r = ''
                elif len(r) > 3 and isinstance(r, basestring):
                    r = convert_string_to_req_object(r)

                new_component['requirements'] = r

                active_components.append(new_component)

            cache.set('active_components', active_components)

    except ImportError:
        #Django not loaded, use local file cache instead - best for testing

        with open('procyon/fixtures/components_cache.txt', mode='r') as infile:
            c_text = str(infile.read())
        try:
            comps = json.loads(c_text)
            for c in comps:
                active_components.append(c)
        except ValueError:
            pass

    for component in active_components:
        ctype = str(component.get("type", "None"))
        ctype = ctype.lower().strip()

        if ctype in pattern_list:
            is_match = check_requirements(component.get("requirements", ""), world_data)

            if is_match:
                tags_searching = tags_to_find(tags, world_data)
                tag_match = count_tag_matches(component.get("tags", ""), component.get("weighting", ""), tags_searching)

                if not ctype in component_types:
                    component_types[ctype] = []
                    component_tag_counts[ctype] = []
                component_types[ctype].append(component)
                component_tag_counts[ctype].append(tag_match)

    return component_types, component_tag_counts


def counts_to_probabilities(counts, padding=.3):
    # TODO: Change weighting to 1/n

    total = 0
    probs = []
    try:
        padding = float(padding)
    except ValueError:
        padding = .3

    for count in counts:
        total += (count + padding)
    for count in counts:
        prob = float((count + padding) / float(total))
        probs.append(prob)

    return probs


def create_random_item(world_data={}, override={}, set_random_key=True, parse_dice=False,
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

    component_types, component_tag_counts = breakout_component_types(world_data, tags, pattern_list)

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

                try:
                    text = component.get("name", "")
                except AttributeError:
                    component = model_to_dict(component)
                    text = component.get("name", "")

                if parse_dice:
                    text = parse_dice_text(text)

                item_prefixes.append(pattern_prefixes[idx])
                item_names.append(text)
                item_generators.append(ctype)

                component_props = component.get("properties", {})
                if component_props and isinstance(component_props, dict):
                    properties = component_props
                    item_data = dict(item_data.items() + properties.items())

                component_effects = component.get("effects", [])
                if component_effects and isinstance(component_effects, list) and len(component_effects):
                    effect = component_effects
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


def create_random_name(world_data={}, override={}, pattern="", tags="", rand_seed=None,
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

        if 'year' in world_data:
            year = int(world_data.get('year', None))
            if year:
                if year < 1400:
                    if numpy.random.random() < .5:
                        pattern = name_patterns['king_jon_snow_the_pierced']
                    else:
                        pattern = name_patterns['king_jon_tyrion_snow_of_winterfell']
                elif year > 1900:
                    pattern = name_patterns['jon_snow']
                else:
                    pattern = name_patterns['jon_tyrion_snow']

    generated_item = create_random_item(world_data=world_data, override=override, pattern=pattern, tags=tags,
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


def create_person(world_data={}, father={}, mother={}, child_dna="", tags="", rand_seed="", gender=""):
    try:
        rand_seed = float(rand_seed)
    except Exception:
        rand_seed = numpy.random.random()
    rand_seed = set_rand_seed(rand_seed)

    seed_mother_dna = str(rand_seed)+"1"
    seed_father_dna = str(rand_seed)+"2"
    seed_child_dna = str(rand_seed)+"3"
    seed_name = str(rand_seed)+"42"

    person_data = {}
    person_data["note"] = "Created"
    person_data["rand_seed"] = rand_seed

    year = world_data.get("year", "1100")
    year = int(year)

    father_dna = father.get("dna", "")
    mother_dna = mother.get("dna", "")
    if not father_dna:
        father_dna, temp = dna_helpers.generate_dna(rand_seed=seed_father_dna, race=father.get("race", "human"))
    if not mother_dna:
        mother_dna, temp = dna_helpers.generate_dna(rand_seed=seed_mother_dna, race=father.get("race", "human"))
    dna, temp = dna_helpers.combine_dna(mother_dna, father_dna, seed_child_dna)
    if gender:
        dna = dna_helpers.set_dna_gender(dna, gender)

    set_rand_seed(rand_seed)
    # dna = dna_helpers.mutate_dna(dna)

    race = dna_helpers.race_from_dna(dna)
    # race = father.get("race", "human") #TODO: Temporary

    gender = dna_helpers.gender_from_dna(dna)
    name_data = create_random_name(world_data=world_data, tags=tags, rand_seed=seed_name, gender=gender)
    name = name_data["name"]

    qualities = dna_helpers.qualities_from_dna(dna)
    aspects = dna_helpers.aspects_from_dna(dna)


    events = []
    events.append({"age": 0, "year": year, "message": name + " was born"})
    events.append({"age": 1, "year": year+1, "message": "Had an uneventful 1st birthday"})
    events.append({"age": 2, "year": year+2, "message": "Had an uneventful 2nd birthday"})
    note = name + " born!"


    person_data["dna"] = dna
    person_data["events"] = events
    person_data["note"] = note
    person_data["race"] = race
    person_data["name"] = name
    person_data["gender"] = gender
    person_data["qualities"] = qualities
    person_data["aspects"] = aspects
    person_data["description"] = person_description(person_data)

    return person_data


def person_description(person_data):
    description = ""

    if person_data.get("age", None):
        description += str(person_data["age"]) + " year old"
    if person_data.get("gender", None):
        description += " " + person_data["gender"].title()
    if person_data.get("race", None):
        description += " " + person_data["race"].title()
    if person_data.get("profession", None):
        description += " " + person_data["profession"].title()

    return description