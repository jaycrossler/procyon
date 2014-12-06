__author__ = 'jcrossler'

import numpy
import json
from procyon.starsystemmaker import math_helpers
from procyon.starsystemmaker.name_library import *
import dna_helpers
import story_person_helpers


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
            requirements = math_helpers.convert_string_to_req_object(requirements)

    if isinstance(requirements, list):
        for req in requirements:
            concept = req.get('concept', '')
            name = req.get('name', '')
            requirement = req.get('requirement', '')
            req_array = []
            if requirement and isinstance(requirement, list):
                req_array = requirement
            elif requirement and isinstance(requirement, basestring):
                req_array = requirement.split(".")
            elif concept and name:
                req_array = [concept, name]
            elif name:
                req_array = [name]

            r_is = req.get('is', '')
            r_exists = req.get('exists', '')
            r_has = req.get('has', '')
            r_exceeds = req.get('exceeds', '')
            r_empty = req.get('empty', '')
            r_below = req.get('below', '')
            r_gt = req.get('>', '')
            r_lt = req.get('<', '')

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
                            to_check = math_helpers.value_of_variable(to_check)
                            if r_exceeds:
                                r_exceeds = math_helpers.value_of_variable(r_exceeds)
                                checks.append(r_exceeds <= to_check)
                            if r_gt:
                                r_gt = math_helpers.value_of_variable(r_gt)
                                checks.append(r_gt < to_check)
                            if r_lt:
                                r_lt = math_helpers.value_of_variable(r_lt)
                                checks.append(r_lt > to_check)
                            if r_below:
                                r_below = math_helpers.value_of_variable(r_below)
                                r_below = float(r_below)
                                checks.append(r_below >= to_check)
                            if r_is:
                                try:
                                    temp = math_helpers.value_of_variable(r_is)
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
        if family:
            if 'tags' in family:
                family_tags = family.get('tags', '')
                tags_list = tags_list + family_tags.split(",")
            father = family.get("father", {})
            if 'tags' in father:
                family_tags = father.get('tags', '')
                tags_list = tags_list + family_tags.split(",")

            mother = family.get("mother", {})
            if 'tags' in mother:
                family_tags = mother.get('tags', '')
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
                    r = math_helpers.convert_string_to_req_object(r)

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

    tags_searching = tags_to_find(tags, world_data)
    for component in active_components:
        ctype = str(component.get("type", "None"))
        ctype = ctype.lower().strip()

        if ctype in pattern_list:
            is_match = check_requirements(component.get("requirements", ""), world_data)

            if is_match:
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
        rand_seed = math_helpers.set_rand_seed(rand_seed)
    note = ""

    pattern_list, pattern_probability, pattern_prefixes = turn_pattern_to_hash(pattern, override)

    new_pattern_list = []
    for p in pattern_list:
        p_parts = p.split("|")
        new_pattern_list.append(p_parts[0])

    component_types, component_tag_counts = breakout_component_types(world_data, tags, new_pattern_list)

    item_data = {}
    effects_data = []
    item_generators = []
    item_prefixes = []
    item_names = []
    properties = {}
    tags = []

    for idx, ctype in enumerate(pattern_list):
        ctype_filter = ctype
        ctype_parts = ctype.split("|")
        ctype = ctype_parts[0]

        if numpy.random.random() <= pattern_probability[idx]:
            if ctype in component_types:
                components = component_types.get(ctype)

                if override and ctype_filter in override:
                    # Use this component instead
                    component_name = override.get(ctype_filter)
                    component = {"name": component_name}
                    ctype_filter = 'overrode'

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
                    text = math_helpers.parse_dice_text(text)

                item_prefixes.append(pattern_prefixes[idx])
                item_names.append(text)
                item_generators.append(ctype_filter)

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
        rand_seed = math_helpers.set_rand_seed(rand_seed)
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
    rand_seed = math_helpers.set_rand_seed(rand_seed)

    seed_mother_dna = str(rand_seed) + "1"
    seed_father_dna = str(rand_seed) + "2"
    seed_child_dna = str(rand_seed) + "3"
    seed_name = str(rand_seed) + "42"

    person_data = {}
    person_data["note"] = ""
    person_data["rand_seed"] = rand_seed
    tag_manager = {}
    math_helpers.add_tags(tag_manager, 'initial', tags)

    father_dna = father.get("dna", "")
    mother_dna = mother.get("dna", "")
    if not father_dna:
        father_dna, temp = dna_helpers.generate_dna(rand_seed=seed_father_dna, race=father.get("race", "human"))
    if not mother_dna:
        mother_dna, temp = dna_helpers.generate_dna(rand_seed=seed_mother_dna, race=mother.get("race", "human"))
    if child_dna:
        dna = child_dna
    else:
        dna, temp = dna_helpers.combine_dna(mother_dna, father_dna, seed_child_dna)
    if gender:
        dna = dna_helpers.set_dna_gender(dna, gender)
    father["dna"] = father_dna
    mother["dna"] = mother_dna

    #TODO: tag_manager seems to be accumulating tags
    world_data, family_events = story_person_helpers.set_world_data(father, mother, world_data, tag_manager)

    last_name = father.get("family_name", None)
    if not last_name:
        last_name = mother.get("family_name", None)
    if not last_name:
        last_name = "Snow"

    year = world_data.get("year")
    year = int(year)

    math_helpers.set_rand_seed(rand_seed)
    dna = dna_helpers.mutate_dna(dna)
    gender = dna_helpers.gender_from_dna(dna)
    name_data = create_random_name(world_data=world_data, tags=math_helpers.flatten_tags(tag_manager),
                                   rand_seed=seed_name, gender=gender,
                                   pattern='namefile,namefile|last_given', override={'namefile|last_given': last_name})
    birth_place = create_random_item(world_data=world_data, set_random_key=False, pattern='birthplace', name_length=300)

    person_data["dna"] = dna
    person_data["events"] = family_events
    person_data["race"] = dna_helpers.race_from_dna(dna)
    person_data["name"] = name_data["name"]
    person_data["gender"] = gender

    person_data["qualities"], person_data["attribute_mods"] = dna_helpers.qualities_from_dna(dna)
    person_data["aspects"] = dna_helpers.aspects_from_dna(dna)
    person_data["skills"] = []
    person_data["item_list"] = []
    person_data["description"] = story_person_helpers.person_description(person_data)

    # TODO: Pass JSON back for every event that has:
    # person_data["birth_data"] = {
    #     "qualities": qualities,
    #     "attribute_mods": attribute_mods,
    #     "aspects": dna_helpers.aspects_from_dna(dna),
    #     "skills": [],
    #     "item_list": [],
    #     "description": story_person_helpers.person_description(person_data)
    # }

    event_id = len(family_events)
    age = 0
    person_event_data = apply_event_effects(person_data=person_data, world_data=world_data, age=age,
                                            event_data=birth_place, event_type='birthplace', year=year,
                                            tag_manager=tag_manager, event_id=event_id)
    person_data["events"].append(person_event_data)

    years_to_scan = 16 + math_helpers.roll_dice("2d10", use_numpy=True)
    for y in range(years_to_scan):
        age += 1
        event_id += 1
        world_data["year"] = year + age
        person_event_data = {"id": event_id, "age": age, "year": year + age, "message": "Had an uneventful birthday",
                             "world_data": json.dumps(world_data)}
        person_data["events"].append(person_event_data)

    person_data["tags"] = str(math_helpers.flatten_tags(tag_manager))

    return person_data


def apply_event_effects(person_data={}, world_data={}, event_data={}, event_type='birthplace', year=None,
                        age=None, tag_manager={}, event_id=42):
    message = ""

    if not year:
        year = world_data.get("year", 1100)
    world_data["year"] = year

    if age is None:
        age = person_data.get("age", 16 + numpy.random.randint(20))
    person_data["age"] = age

    name = event_data.get("name", "in a barn")
    properties = event_data.get("properties", {})

    if isinstance(properties, basestring):
        properties = math_helpers.convert_string_to_properties_object(properties)

    math_helpers.add_tags(tag_manager, 'event', event_data.get("tags", []))

    effect_was_applied = False
    generated_items = []
    addional_messages = []
    effects = event_data.get("effects", [])

    for effect in effects:
        # Don't consider if it's a unique effect
        prevent = effect.get("unique", False)

        if prevent and effect_was_applied:
            continue

        family = world_data.get("family", {})

        # Roll the dice, if the chance occurs then parse the rest
        chance = effect.get("chance", None)
        if chance:
            chance_modifier = family.get("conflict", 1)

            try:
                chance_modifier = float(chance_modifier)
            except ValueError:
                chance_modifier = 1

            try:
                chance = math_helpers.value_of_variable(chance)
                chance += chance_modifier
                chance /= 100

                if not numpy.random.random() < chance:
                    continue
            except ValueError:
                continue
        else:
            pass

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

        # Generators can create objects/items for use in the story
        #TODO: Generate a generator also if it's in a message text and not called out explicitly
        generator_data = {"generator": effect.get("generator", None),
                          "role": effect.get("role", None),
                          "years": effect.get("years", None),
                          "override": effect.get("override", None),
                          "power": effect.get("refresh", None) or effect.get("power", None)
        }
        # Run methods for everything in effects
        effect_data = effect.get("effect", None)  # pay = good, father.leave, disease = infection
        effect_data = math_helpers.convert_string_to_properties_object(effect_data)
        effect_data = math_helpers.add_or_merge_dicts(effect_data, generator_data)
        generated_items_new = story_person_helpers.apply_effects(person_data, world_data, effect_data, tag_manager)
        generated_items = generated_items + generated_items_new

        # Properties are always applied to the person after all effects are run
        ef_properties = effect.get("properties", None)  # JSON or str, "mother.profession = prostitute, lifespan +2
        if ef_properties:
            if isinstance(ef_properties, basestring):
                ef_properties = math_helpers.convert_string_to_properties_object(ef_properties)

            properties = math_helpers.add_or_merge_dicts(properties, ef_properties)
        effect_was_applied = True

    if event_type == 'birthplace':
        if isinstance(name, basestring) and name is not '':
            name_lower = name[0].lower() + name[1:]
        else:
            name_lower = name
        message += "<b>" + person_data.get("name") + " was born " + name_lower + "</b>"
        addional_messages = [message] + addional_messages

    if properties:
        message_new = story_person_helpers.apply_properties(person_data, world_data, properties, generated_items)
        if message_new:
            addional_messages.append(message_new)

    if generated_items:
        person_data["item_list"] += generated_items

    addional_messages = [m.strip() for m in addional_messages]
    message = "<br/>".join(addional_messages)

    return {"id": event_id, "age": age, "year": year, "message": message, "world_data": json.dumps(world_data)}