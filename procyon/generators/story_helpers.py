__author__ = 'jcrossler'

import numpy
import json
from procyon.starsystemmaker.math_helpers import *
from procyon.starsystemmaker.name_library import *
import dna_helpers

VALUE_ARRAY = 'none tiny terrible poor mediocre average fair good great superb fantastic epic'.split(" ")


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
        if len(var) < 1:
            return var

        negative = False

        if var[0] == "-":
            negative = True
            var = var[1:]

        lookups = {'epic': 144.0, 'fantastic': 89.0, 'superb': 55.0, 'great': 34.0, 'good': 21.0, 'high': 13.0,
                   'fair': 8.0, 'average': 5.0, 'medium': 5.0, 'moderate': 5.0, 'mediocre': 3.0,
                   'low': 3.0, 'poor': 2.0, 'terrible': 1.0, 'tiny': 0.1, 'none': 0.0}
        if var in lookups:
            val = lookups[var]
        else:
            val = var

        try:
            val = float(val)
        except ValueError:
            pass

        if negative and isinstance(val, float):
            val = -val

    else:
        try:
            val = float(var)
        except ValueError:
            pass
        except TypeError:
            pass

    return val


def convert_string_to_properties_object(props):
    # lifespan +2, cost = poor, mother.profession = teacher, father.leaves, blessings
    properties = {}
    props = str(props)

    if len(props) < 3:
        return {}

    props_split = props.split(",")
    props_split = [req.strip() for req in props_split]

    for p in props_split:
        key = ""
        val = ""
        if "=" in p:
            p_parts = p.split("=")
            if len(p_parts) > 1:
                key = p_parts[0].strip()
                val = p_parts[1].strip()
        elif " " in p:
            # check for ending in number
            p_parts = p.rsplit(' ', 1)
            if len(p_parts) > 1:
                key = p_parts[0].strip()
                val = p_parts[1].strip()
        else:
            key = p
            val = 'exists'

        if key and val:
            try:
                val = float(val)
            except ValueError:
                pass
            key = key.lower()
            val = value_of_variable(val)
            if key in properties:
                old_val = properties[key]
                if isinstance(old_val, float) and isinstance(val, float):
                    val += old_val
                else:
                    val = str(old_val) + ", " + str(val)
            properties[key] = val

    return properties


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
    # TODO: Work with 'family.*.profession sailor'

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
    matches = float(base_num) + float(weighting) / 10

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
        # Django not loaded, use local file cache instead - best for testing

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
                       tag_weight=.3, name_length=200):
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
    properties = {}
    tags = []

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

                component_tags = component.get("tags", '')
                if component_tags and isinstance(component_tags, basestring):
                    component_tags = component_tags.split(',')
                component_tags = [c.strip().lower() for c in component_tags]
                tags += component_tags

                component_props = component.get("properties", {})
                if component_props and isinstance(component_props, dict):
                    properties = component_props
                    item_data = dict(item_data.items() + properties.items())

                component_effects = component.get("effects", [])
                if component_effects and isinstance(component_effects, list) and len(component_effects):
                    effect = component_effects
                    effects_data += effect

    item_name = generate_item_name(item_prefixes, item_names, try_for_max_length=name_length)

    item_return = dict(name=item_name, data=item_data, effects=effects_data, note=note, rand_seed=rand_seed,
                       prefixes=item_prefixes, name_parts=item_names, generators=item_generators,
                       tags=tags, properties=properties)
    return item_return


def generate_item_name(item_prefixes, item_names, titleize=False, try_for_max_length=22):
    name = ""
    for idx, item in enumerate(item_names):
        name += item_prefixes[idx] + item_names[idx]

    name = name.strip().capitalize()
    if titleize:
        name = name.title()

    if len(name) > try_for_max_length:
        name_final_pieces = name.split(" ")
        name = name_final_pieces[0] + " " + name_final_pieces[-1]

    if len(name) > try_for_max_length:
        name_final_pieces = name.split(" ")
        first = name_final_pieces[0]
        last = name_final_pieces[-1]
        len_last = len(last)
        len_first = try_for_max_length - len_last

        if len_first > 5:
            first = first[0:len_first]
        name = first + " " + last

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
    name_patterns['jon_snow'] = 'namefile:1,namefile|family:1'
    name_patterns['king_jon_snow_the_pierced'] = 'rank:.1,namefile:1,namefile|family:.7,adjective:.4:the'
    name_patterns['king_jon_tyrion_snow_of_winterfell'] = 'rank:.1,namefile:1,namefile:.2,namefile|family:.8,placefile:.4:of'
    name_patterns['jon_tyrion_snow'] = 'namefile:1,namefile:1,namefile|family:1'

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
                                        rand_seed=rand_seed, set_random_key=set_random_key, tag_weight=tag_weight,
                                        name_length=22)

    for idx, generator in enumerate(generated_item.get('generators')):
        generator_parts = generator.split("|")
        generator = generator_parts[0]
        generator_restrictions = generator_parts[1:]

        if generator == "namefile" or generator == "placefile":
            filename = generated_item['name_parts'][idx]
            restrictions = [filename]
            if generator_restrictions:
                restrictions += generator_restrictions
            elif gender:
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

    seed_mother_dna = str(rand_seed) + "1"
    seed_father_dna = str(rand_seed) + "2"
    seed_child_dna = str(rand_seed) + "3"
    seed_name = str(rand_seed) + "42"

    person_data = {}
    person_data["note"] = ""
    person_data["rand_seed"] = rand_seed

    world_data = set_world_data(father, mother, world_data)
    year = world_data.get("year")
    year = int(year)

    father_dna = father.get("dna", "")
    mother_dna = mother.get("dna", "")
    if not father_dna:
        father_dna, temp = dna_helpers.generate_dna(rand_seed=seed_father_dna, race=father.get("race", "human"))
    if not mother_dna:
        mother_dna, temp = dna_helpers.generate_dna(rand_seed=seed_mother_dna, race=father.get("race", "human"))
    if child_dna:
        dna = child_dna
    else:
        dna, temp = dna_helpers.combine_dna(mother_dna, father_dna, seed_child_dna)
    if gender:
        dna = dna_helpers.set_dna_gender(dna, gender)

    set_rand_seed(rand_seed)
    dna = dna_helpers.mutate_dna(dna)

    race = dna_helpers.race_from_dna(dna)

    gender = dna_helpers.gender_from_dna(dna)
    name_data = create_random_name(world_data=world_data, tags=tags, rand_seed=seed_name, gender=gender)
    name = name_data["name"]

    birth_place = create_random_item(world_data=world_data, set_random_key=False, pattern='birthplace', name_length=300)

    qualities, attribute_mods = dna_helpers.qualities_from_dna(dna)

    person_data["dna"] = dna
    person_data["events"] = []
    person_data["race"] = race
    person_data["name"] = name
    person_data["tags"] = add_tags(5, father.get("tags", ""), mother.get("tags", ""))
    person_data["gender"] = gender
    person_data["qualities"] = qualities
    person_data["attribute_mods"] = attribute_mods
    person_data["aspects"] = dna_helpers.aspects_from_dna(dna)
    person_data["skills"] = []
    person_data["item_list"] = []
    person_data["description"] = person_description(person_data)

    person_data, world_data = apply_event_effects(person_data=person_data, world_data=world_data, age=0,
                                                  event_data=birth_place, event_type='birthplace', year=year)

    person_data["events"].append({"age": 1, "year": year + 1, "message": "Had an uneventful 1st birthday"})
    person_data["events"].append({"age": 2, "year": year + 2, "message": "Had an uneventful 2nd birthday"})

    person_data["world_data"] = str(world_data)

    return person_data


def person_description(person_data):
    description = ""

    if not person_data.get("age", "undefined") == "undefined":
        description += str(person_data["age"]) + " year old"
    if person_data.get("gender", None):
        description += " " + person_data["gender"].title()
    if person_data.get("race", None):
        description += " " + person_data["race"].title()
    if person_data.get("profession", None):
        description += " " + person_data["profession"].title()

    return description


def add_tags(num_from_each=5, *tag_list):
    tags = []
    for tag_words in tag_list:
        if not tag_words:
            continue
        tag_array = []
        if isinstance(tag_words, basestring):
            tag_array = tag_words.split(",")
        elif isinstance(tag_words, dict):
            for tag in tag_words.items():
                tag_array.append(tag[0])

        if len(tag_array):
            tags += np.random.choice(tag_array, num_from_each)
    tags = [tag.lower().strip() for tag in tags]

    return ",".join(tags)


def apply_event_effects(person_data={}, world_data={}, event_data={}, event_type='birthplace', year=None,
                        age='undefined'):
    message = ""

    if not year:
        if "year" in world_data:
            year = world_data["year"]
        else:
            year = 1100
    world_data["year"] = year
    if age == 'undefined':
        if "age" in person_data:
            age = person_data["age"]
        else:
            age = 16 + numpy.random.randint(20)
    person_data["age"] = age

    name = event_data.get("name", "in a barn")
    properties = event_data.get("properties", {})

    if isinstance(properties, basestring):
        properties = convert_string_to_properties_object(properties)

    tags = event_data.get("tags", [])
    if tags:
        tags = person_data.get("tags", name).split(",") + tags
        tags = [t for t in tags if t]
        person_data["tags"] = ",".join(tags)  # TODO: Make a tag manager

    generated_items = []
    addional_messages = []
    effects = event_data.get("effects", [])
    for effect in effects:

        # Roll the dice, if the chance occurs then parse the rest
        chance = effect.get("chance", 100)
        family = world_data.get("family", {})
        chance_modifier = family.get("conflict", 1)

        try:
            chance_modifier = float(chance_modifier)
        except ValueError:
            chance_modifier = 1

        try:
            chance = value_of_variable(chance)
            chance += chance_modifier
            chance /= 100

            if not numpy.random.random() < chance:
                continue
        except ValueError:
            continue

        # Check the requirements # family.enemy has Elves, "family.*.profession sailor", family.*.profession has doctor
        requirement = effect.get("requirement", None)
        if requirement:
            passes = check_requirements(requirement, world_data)
            if not passes:
                continue

        # Update the message # "An innkeeper named [barmaid.name] assists, You were born the day your father was killed in battle. His [weapon.type] and [armor.type] are passed to you.
        ef_message = effect.get("message", None)
        if ef_message:
            addional_messages.append(ef_message)

        #Generators can create objects/items for use in the story
        generator_data = {"generator": effect.get("generator", None),
                          "role": effect.get("role", None),
                          "years": effect.get("years", None),
                          "override": effect.get("override", None),
                          "power": effect.get("refresh", None) or effect.get("power", None)
        }
        #Run methods for everything in effects
        effect_data = effect.get("effect", None)  # pay = good, father.leave, disease = infection
        effect_data = convert_string_to_properties_object(effect_data)
        effect_data = dict_update_add(effect_data, generator_data)
        generated_items_new = apply_effects(person_data, world_data, effect_data)
        generated_items = generated_items + generated_items_new

        #Properties are always applied to the person after all effects are run
        ef_properties = effect.get("properties", None)  # JSON or str, "mother.profession = prostitute, lifespan +2
        if ef_properties:
            if isinstance(ef_properties, basestring):
                ef_properties = convert_string_to_properties_object(ef_properties)

            properties = dict_update_add(properties, ef_properties)

    if event_type == 'birthplace':
        name_lower = name[0].lower() + name[1:]
        message += "<b>" + person_data.get("name") + " was born " + name_lower + "</b>"
        addional_messages = [message] + addional_messages

    if properties:
        message_new = apply_properties(person_data, world_data, properties, generated_items)
        if message_new:
            addional_messages.append(message_new)

    if generated_items:
        person_data["item_list"] += generated_items

    addional_messages = [m.strip() for m in addional_messages]
    message = "<br/>".join(addional_messages)

    person_data["events"].append({"age": age, "year": year, "message": message})

    return person_data, world_data


# TODO: Add version that modifies existing object instead of making clone
def dict_update_add(dict1, dict2):
    d = {}
    for k, v in dict1.items():
        try:
            d[k] = float(v)
        except ValueError:
            d[k] = v

    for k, v in dict2.items():
        if k in d or k.lower() in d:
            try:
                v1 = float(d[k])
                v2 = float(v)
                d[k] = v1 + v2
            except ValueError:
                d[k] = str(d[k]) + "," + str(v)
        else:
            d[k] = v
    return d


def dict_add(d, key, val):
    if isinstance(d, tuple):
        raise Exception("Tuple Exception inside of 'dict_add' method: " + str(d))

    if isinstance(d, list):
        found = False
        for d_item in d:
            if d_item.get("name", "") == key and d_item.get("value"):
                existing_val = d_item.get("value")
                try:
                    v1 = float(existing_val)
                    v2 = float(val)
                    d_item["name"] = v1 + v2
                except ValueError:
                    d_item["name"] = str(existing_val) + "," + str(val)
            found = True
        if not found:
            try:
                val = float(val)
            except ValueError:
                pass
            d.append({"name": key, "value": val})
    else:
        if key in d or key.lower() in d:
            try:
                v1 = float(d[key])
                v2 = float(val)
                d[key] = v1 + v2
            except ValueError:
                d[key] = str(d[key]) + "," + str(val)
        else:
            if isinstance(key, basestring):
                d[key] = val
            else:
                #TODO: Fix this - what's trying to add complex items?
                pass

    return d


def apply_properties(person_data={}, world_data={}, properties_data={}, generated_items=list()):
    # Sample properties:
    # "lifespan": "1d6-3",
    #   "reroll": "true",
    #   "message": "Born while traveling to [country]"
    # }
    message = ""
    for key, val in properties_data.items():
        if key == "message":
            message = val
            #TODO: Build func to parse out names and subnames
            for item in generated_items:
                name = item.get("name", "")
                nickname = item.get("nickname", "item")
                if name:
                    message = message.replace("[" + nickname + "]", name)

                    #TODO: parse in text from generated_items
        elif key.startswith("world."):
            #TODO: have this work for multiple-level settings
            key = key[6:]
            dict_add(world_data, key, val)
        else:
            val = roll_dice(val)
            dict_add(person_data, key, val)
            message += key + " was adjusted " + str(val)

    return message


def apply_effects(person_data={}, world_data={}, effect_data={}):
    # Sample events:
    # pay = good, father.leave, disease = infection, pay = low-fair, blessing, family.blessing,
    #  cost = poor, disease = mutation, "gain [weapon], gain [armor]"

    # Sample Generators:
    #     generator =   # barmaid, country, wizard, sailor, horse, creature, scholar, royalty, "weapon, armor"
    #     power/refresh =  # 2
    #     years =  # 1d6
    #     role =   # caretaker, mount, pet, familiar

    tags = person_data.get("tags", "")
    items = person_data.get("children", [])
    qualities = person_data["qualities"]

    generated_items = []
    if "generator" in effect_data:
        generator_list = effect_data.get("generator", "")
        if generator_list:
            power = effect_data.get("refresh", None) or effect_data.get("power", 1)
            years = effect_data.get("years", 4)
            role = effect_data.get("role", "friend")
            override = effect_data.get("override", "")
            override = convert_string_to_properties_object(override)

            effect_data.pop("generator", None)
            effect_data.pop("refresh", None)
            effect_data.pop("power", None)
            effect_data.pop("years", None)
            effect_data.pop("role", None)
            effect_data.pop("override", None)

            generators = generator_list.split(",")
            generators = [g.strip() for g in generators]
            for generator in generators:
                created = create_random_item(world_data=world_data, override=override, pattern=generator, tags=tags)
                generated = generate_object(generator=generator, world_data=world_data, item_template=created,
                                            power=power, tags=tags, role=role, years=years)

                data = generated.get("data", {})
                data["role"] = role
                years = effect_data.get("years", 1)
                years = roll_dice(years)
                data["years"] = years

                generated_items.append(generated)

                if role:
                    finished_year = int(world_data.get("year", 1100)) + int(years)
                    items.append({"type": role, "finished": finished_year, "active": True, "data": generated})

    for effect, variable in effect_data.items():
        # pay = good, father.leave, disease = infection, pay = low-fair, blessing, family.blessing,
        #  cost = poor, disease = mutation, "gain [weapon], gain [armor]"

        #TODO: All other non-generators, run functions
        if effect == "pay":
            if not variable:
                #TODO: Dynamically calculate difficulty
                variable = 5.0
            elif variable == 'exists':
                variable = 5.0
            if isinstance(variable, basestring):
                variable = 5.0
            dict_add(person_data, "money", variable)

        elif effect == "father.leave":
            pass
        elif effect == "disease":
            if not variable:
                variable = 3.0
            elif variable == 'exists':
                variable = 3.0
            if isinstance(variable, basestring):
                variable = 3.0
            dict_add(qualities, 'lifespan', -variable)
            items.append({"type": "disease", "name": "rickets"})

        elif effect == "pay":
            if not variable:
                variable = 5.0
            elif variable == 'exists':
                variable = 5.0
            if isinstance(variable, basestring):
                variable = 5.0
            dict_add(person_data, "money", variable)

        elif effect == "blessing":
            if not variable:
                variable = 3.0
            elif variable == 'exists':
                variable = 3.0
            if isinstance(variable, basestring):
                variable = 3.0
            dict_add(qualities, 'lifespan', variable)
            items.append({"type": "blessing", "name": "lucky"})

        elif effect == "family.blessing":
            if not variable:
                variable = 3.0
            elif variable == 'exists':
                variable = 3.0
            if isinstance(variable, basestring):
                variable = 3.0
            dict_add(qualities, 'lifespan', -variable)
            items.append({"type": "family blessing", "name": "wealthy"})

        elif effect == "cost":
            if not variable:
                variable = 5.0
            elif variable == 'exists':
                variable = 5.0
            if isinstance(variable, basestring):
                variable = 5.0
            dict_add(person_data, "money", -variable)

        elif effect == "gain":
            pass

    return generated_items


def set_world_data(father, mother, world_data):
    father_economics = father.get("economic") or numpy.random.choice(VALUE_ARRAY)
    mother_economics = mother.get("economic") or numpy.random.choice(VALUE_ARRAY)
    father_education = father.get("education") or numpy.random.choice(VALUE_ARRAY)
    mother_education = mother.get("education") or numpy.random.choice(VALUE_ARRAY)
    father_conflict = father.get("conflict") or "low"
    mother_conflict = mother.get("conflict") or "low"
    father_profession = father.get("profession") or "Farmer"
    mother_profession = mother.get("profession") or "Farmer"

    year = world_data.get("year", numpy.random.randint(1000, 2000))
    world_data["year"] = int(year)
    family = world_data.get("family", {})

    try:
        economics = float(value_of_variable(father_economics) + value_of_variable(mother_economics))
        economics -= 3
    except ValueError:
        economics = father_economics
    family["economics"] = family.get("economics", economics)

    try:
        conflict = float(value_of_variable(father_conflict) + value_of_variable(mother_conflict))
        conflict -= 5
    except ValueError:
        conflict = father_conflict
    family["conflict"] = family.get("conflict", conflict)

    father = family.get("father", {})
    mother = family.get("mother", {})

    father["profession"] = father.get("profession", father_profession)
    father["economics"] = father_economics
    father["education"] = father_education
    father["conflict"] = father_conflict
    father_tags = father.get("tags", father_profession.lower())
    if father_economics > value_of_variable('fair'):
        father_tags += ",wealthy"
    if father_education > value_of_variable('fair'):
        father_tags += ",educated"
    father["tags"] = father_tags

    mother["profession"] = mother.get("profession", mother_profession)
    mother["economics"] = mother_economics
    mother["education"] = mother_education
    mother["conflict"] = mother_conflict
    mother_tags = mother.get("tags", mother_profession.lower())
    if mother_economics > value_of_variable('fair'):
        mother_tags += ",wealthy"
    if mother_education > value_of_variable('fair'):
        mother_tags += ",educated"
    mother["tags"] = mother_tags

    if "house" not in family:
        if economics >= value_of_variable('great'):
            family["house"] = "large"
        elif economics >= value_of_variable('good'):
            family["house"] = "medium"
        elif economics >= value_of_variable('fair'):
            family["house"] = "small"

    #TODO: Have parents leave if high conflict or low economics
    #TODO: Grandparents?
    #TODO: Nanny or Caretaker if ec > high
    #TODO: What to do with education? Job?

    family["father"] = father
    family["mother"] = mother

    world_data["family"] = family
    world_data["magic"] = world_data.get("magic", numpy.random.choice(VALUE_ARRAY))
    world_data["technology"] = world_data.get("technology", numpy.random.choice(VALUE_ARRAY))

    return world_data


def generate_object(generator='person', world_data={}, item_template={}, power=1, tags='', role='friend', years=4):
    end_date = world_data.get("year", 1100)
    years = roll_dice(years)
    try:
        if end_date:
            end_date = int(end_date)
        else:
            end_date = 1100

        if years:
            years = int(years)
        else:
            years = 4
        end_date = end_date + years
    except ValueError:
        end_date = None
    generated = {"type": role, "power": power, "tags": tags, "name": generator, "end_date": end_date}

    #TODO: Expand this

    return generated


    #TODO: Move story generators and effects to new class
    #TODO: Have an economics lookup engine
    #TODO: Use names from parents, only use ranks if economics and world says so
    #TODO: Determine nationality, use names from those