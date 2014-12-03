import numpy
from procyon.starsystemmaker import math_helpers
import story_helpers


def set_world_data(father, mother, world_data, tag_manager):
    father_economics = father.get("economic") or numpy.random.choice(math_helpers.VALUE_ARRAY)
    mother_economics = mother.get("economic") or numpy.random.choice(math_helpers.VALUE_ARRAY)
    father_education = father.get("education") or numpy.random.choice(math_helpers.VALUE_ARRAY)
    mother_education = mother.get("education") or numpy.random.choice(math_helpers.VALUE_ARRAY)
    father_conflict = father.get("conflict") or "low"
    mother_conflict = mother.get("conflict") or "low"
    father_profession = father.get("profession") or "Farmer"
    mother_profession = mother.get("profession") or "Farmer"

    year = world_data.get("year", numpy.random.randint(1000, 2000))
    world_data["year"] = int(year)
    family = world_data.get("family", {})
    city_data = world_data.get("city", {})

    world_tags = world_data.get("tags", "")
    city_tags = city_data.get("tags", "")

    try:
        economics = float(math_helpers.value_of_variable(father_economics) + math_helpers.value_of_variable(mother_economics))
        economics -= 3
    except ValueError:
        economics = father_economics
    family["economics"] = family.get("economics", economics)

    try:
        conflict = float(math_helpers.value_of_variable(father_conflict) + math_helpers.value_of_variable(mother_conflict))
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
    if father_economics > math_helpers.value_of_variable('fair'):
        father_tags += ",wealthy"
    if father_education > math_helpers.value_of_variable('fair'):
        father_tags += ",educated"
    father["tags"] = father_tags
    math_helpers.add_tags(tag_manager, 'father', father_tags)

    mother["profession"] = mother.get("profession", mother_profession)
    mother["economics"] = mother_economics
    mother["education"] = mother_education
    mother["conflict"] = mother_conflict
    mother_tags = mother.get("tags", mother_profession.lower())
    if mother_economics > math_helpers.value_of_variable('fair'):
        mother_tags += ",wealthy"
    if mother_education > math_helpers.value_of_variable('fair'):
        mother_tags += ",educated"
    mother["tags"] = mother_tags
    math_helpers.add_tags(tag_manager, 'mother', mother_tags)

    if "house" not in family:
        if economics >= math_helpers.value_of_variable('great'):
            family["house"] = "large"
        elif economics >= math_helpers.value_of_variable('good'):
            family["house"] = "medium"
        elif economics >= math_helpers.value_of_variable('fair'):
            family["house"] = "small"

    # TODO: Have parents leave if high conflict or low economics
    #TODO: Grandparents?
    #TODO: Nanny or Caretaker if ec > high
    #TODO: What to do with education? Job?
    #TODO: Create city
    #TODO: Ranks or royalty
    #TODO: For ages from 17 to now...


    family["father"] = father
    family["mother"] = mother

    world_data["family"] = family
    magic_num = numpy.random.choice(math_helpers.VALUE_ARRAY)
    world_data["magic"] = world_data.get("magic", magic_num)
    world_data["technology"] = world_data.get("technology", numpy.random.choice(math_helpers.VALUE_ARRAY))

    math_helpers.add_tags(tag_manager, 'world', world_tags)
    math_helpers.add_tags(tag_manager, 'city', city_tags)

    if math_helpers.value_of_variable(magic_num) > 6:
        math_helpers.add_tags(tag_manager, 'world', 'magic')

    return world_data


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


def apply_properties(person_data={}, world_data={}, properties_data={}, generated_items=list()):
    # Sample properties:
    # "lifespan": "1d6-3",
    # "reroll": "true",
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
            math_helpers.add_or_increment_dict_val(world_data, key, val)
        else:
            val = math_helpers.roll_dice(val, use_numpy=True)
            math_helpers.add_or_increment_dict_val(person_data, key, val)
            message += key + " was adjusted " + str(val)

    return message


def apply_effects(person_data={}, world_data={}, effect_data={}, tag_manager={}):
    # Sample events:
    # pay = good, father.leave, disease = infection, pay = low-fair, blessing, family.blessing,
    # cost = poor, disease = mutation, "gain [weapon], gain [armor]"

    # Sample Generators:
    #     generator =   # barmaid, country, wizard, sailor, horse, creature, scholar, royalty, "weapon, armor"
    #     power/refresh =  # 2
    #     years =  # 1d6
    #     role =   # caretaker, mount, pet, familiar

    tags = math_helpers.flatten_tags(tag_manager)
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
            override = math_helpers.convert_string_to_properties_object(override)

            effect_data.pop("generator", None)
            effect_data.pop("refresh", None)
            effect_data.pop("power", None)
            effect_data.pop("years", None)
            effect_data.pop("role", None)
            effect_data.pop("override", None)

            generators = generator_list.split(",")
            generators = [g.strip() for g in generators]
            for generator in generators:
                created = story_helpers.create_random_item(world_data=world_data, override=override, pattern=generator, tags=tags)
                generated = generate_object(generator=generator, world_data=world_data, item_template=created,
                                            power=power, tags=tags, role=role, years=years)

                data = generated.get("data", {})
                data["role"] = role
                years = effect_data.get("years", 1)
                years = math_helpers.roll_dice(years, use_numpy=True)
                data["years"] = years

                generated_items.append(generated)

                if role:
                    finished_year = int(world_data.get("year", 1100)) + int(years)
                    items.append({"type": role, "finished": finished_year, "active": True, "data": generated})

    family = person_data.get("family", {})
    father = family.get("father", {})
    mother = family.get("mother", {})
    year = world_data.get("year", 1100)

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
            math_helpers.add_or_increment_dict_val(person_data, "money", variable)

        elif effect == "father.leave":
            father["leave"] = year
            #TODO: reduce family income
            pass
        elif effect == "mother.leave":
            mother["leave"] = year
            #TODO: reduce family income
            pass

        elif effect == "disease":
            if not variable:
                variable = 3.0
            elif variable == 'exists':
                variable = 3.0
            if isinstance(variable, basestring):
                variable = 3.0
            math_helpers.add_or_increment_dict_val(qualities, 'lifespan', -variable)
            generated_items.append({"type": "disease", "name": "rickets"})  #TODO: Make a disease lookup table

        elif effect == "pay":
            if not variable:
                variable = 5.0
            elif variable == 'exists':
                variable = 5.0
            if isinstance(variable, basestring):
                variable = 5.0
            math_helpers.add_or_increment_dict_val(person_data, "money", variable)

        elif effect == "blessing":
            if not variable:
                variable = 3.0
            elif variable == 'exists':
                variable = 3.0
            if isinstance(variable, basestring):
                variable = 3.0
            math_helpers.add_or_increment_dict_val(qualities, 'lifespan', variable)
            generated_items.append({"type": "blessing", "name": "lucky"})

        elif effect == "family.blessing":
            if not variable:
                variable = 3.0
            elif variable == 'exists':
                variable = 3.0
            if isinstance(variable, basestring):
                variable = 3.0
            math_helpers.add_or_increment_dict_val(qualities, 'lifespan', -variable)
            generated_items.append({"type": "family blessing", "name": "wealthy"})

        elif effect == "cost":
            if not variable:
                variable = 5.0
            elif variable == 'exists':
                variable = 5.0
            if isinstance(variable, basestring):
                variable = 5.0
            math_helpers.add_or_increment_dict_val(person_data, "money", -variable)

        elif effect == "gain":
            pass

    return generated_items


def generate_object(generator='person', world_data={}, item_template={}, power=1, tags='', role='friend', years=4):
    end_date = world_data.get("year", 1100)
    years = math_helpers.roll_dice(years, use_numpy=True)
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

    # TODO: Expand this

    return generated


    #TODO: Move story generators and effects to new class
    #TODO: Have an economics lookup engine
    #TODO: Use names from parents, only use ranks if economics and world says so
    #TODO: Determine nationality, use names from those


def add_family_history(person_data={}, world_data={}, event_id=0, tag_manager={}):


    return event_id