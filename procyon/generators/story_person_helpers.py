import numpy
from procyon.starsystemmaker import math_helpers
import story_helpers
import dna_helpers


def set_world_data(father, mother, world_data, tag_manager):
    father_economic = father.get("economic") or numpy.random.choice(math_helpers.VALUE_ARRAY)
    mother_economic = mother.get("economic") or numpy.random.choice(math_helpers.VALUE_ARRAY)
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
        economic = float(math_helpers.value_of_variable(father_economic) + math_helpers.value_of_variable(mother_economic)) / 2.0
        economic -= 3
    except ValueError:
        economic = father_economic
    family["economic"] = family.get("economic", economic)

    try:
        conflict = float(math_helpers.value_of_variable(father_conflict) + math_helpers.value_of_variable(mother_conflict)) / 2.0
        conflict -= 5
    except ValueError:
        conflict = father_conflict
    family["conflict"] = family.get("conflict", conflict)

    father = father or family.get("father", {})
    mother = mother or family.get("mother", {})

    father["profession"] = father.get("profession", father_profession)
    father["economic"] = father_economic
    father["education"] = father_education
    father["conflict"] = father_conflict
    father_tags = father.get("tags", father_profession.lower())
    if father_economic > math_helpers.value_of_variable('fair'):
        father_tags += ",wealthy"
    if father_education > math_helpers.value_of_variable('fair'):
        father_tags += ",educated"
    father["tags"] = father_tags
    math_helpers.add_tags(tag_manager, 'father', father_tags)

    mother["profession"] = mother.get("profession", mother_profession)
    mother["economic"] = mother_economic
    mother["education"] = mother_education
    mother["conflict"] = mother_conflict
    mother_tags = mother.get("tags", mother_profession.lower())
    if mother_economic > math_helpers.value_of_variable('fair'):
        mother_tags += ",wealthy"
    if mother_education > math_helpers.value_of_variable('fair'):
        mother_tags += ",educated"
    mother["tags"] = mother_tags
    math_helpers.add_tags(tag_manager, 'mother', mother_tags)

    if not father.get("family_name", None):
        father["family_name"] = story_helpers.create_random_name(world_data=world_data, pattern='namefile|family',
                                                                 tags=math_helpers.flatten_tags(tag_manager), gender='Male')['name']
    if not mother.get("family_name", None):
        mother["family_name"] = story_helpers.create_random_name(world_data=world_data, pattern='namefile|family',
                                                                 tags=math_helpers.flatten_tags(tag_manager), gender='Female')['name']

    family_events = build_parent_history(year=year, father=father, mother=mother, world_data=world_data)

    #TODO: Have parent histories go beyond birth and cover siblings
    #TODO: Grandparents
    #TODO: Nanny or Caretaker if ec > high
    #TODO: What to do with education? Job?
    #TODO: Create city
    #TODO: Ranks or royalty
    #TODO: Adoptions
    #TODO: Same-sex marriages


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

    return world_data, family_events


def build_parent_history(year=1100, father={}, mother={}, world_data={}):
    #Calculate Parents History
    family_events = []

    father_economic = math_helpers.value_of_variable(father.get("economic", 1)) or math_helpers.rand_weighted(midpoint=0.2)*120
    mother_economic = math_helpers.value_of_variable(mother.get("economic", 1)) or math_helpers.rand_weighted(midpoint=0.2)*120
    father_education = math_helpers.value_of_variable(father.get("education", 1)) or math_helpers.rand_weighted(midpoint=0.2)*120
    mother_education = math_helpers.value_of_variable(mother.get("education", 1)) or math_helpers.rand_weighted(midpoint=0.2)*120
    father_conflict = math_helpers.value_of_variable(father.get("conflict", 1)) or math_helpers.rand_weighted(midpoint=0.2)*120
    mother_conflict = math_helpers.value_of_variable(mother.get("conflict", 1)) or math_helpers.rand_weighted(midpoint=0.2)*120

    father_dna = father.get("dna", dna_helpers.generate_dna())
    mother_dna = mother.get("dna", dna_helpers.generate_dna())
    father_qualities, father_attribute_mods = dna_helpers.qualities_from_dna(father_dna)
    mother_qualities, mother_attribute_mods = dna_helpers.qualities_from_dna(mother_dna)

    father_family_name = father.get("family_name", "")
    mother_family_name = mother.get("family_name", "")

    mother_tags = mother.get("tags", "")
    father_tags = father.get("tags", "")

    #Being "of age" changes through the years, from 13 to 17
    #TODO: Modify this by racial longevity
    base_age = int(math_helpers.percent_range(value=year, start_min=1000, start_max=2000, end_min=14, end_max=20))

    family = world_data.get("family", {})
    house = family.get("house", 1) or math_helpers.rand_weighted(midpoint=0.2)*100
    house = math_helpers.value_of_variable(house)

    #Parents age when they have main child is later with conflict and education, earlier with economic
    father_age_mod = math_helpers.percent_range(father_education, 0, 100, 1, 20)
    father_age_at_birth = int(base_age + math_helpers.rand_range(0, 20+father_age_mod, 3, 4))
    father_age_at_birth += math_helpers.percent_range(father_conflict, 0, 100, 0, 10)
    father_age_at_birth += math_helpers.percent_range(father_economic, 0, 100, 0, 5)
    father_age_at_birth = math_helpers.clamp(father_age_at_birth, base_age*1.5, int(base_age*3.2))

    mother_age_mod = math_helpers.percent_range(mother_education, 0, 100, 1, 16)
    mother_age_at_birth = int(base_age + math_helpers.rand_range(0, 20+mother_age_mod, 3, 4))
    mother_age_at_birth += math_helpers.percent_range(mother_conflict, 0, 100, 0, 8)
    mother_age_at_birth += math_helpers.percent_range(mother_economic, 0, 100, 0, 4)
    mother_age_at_birth = math_helpers.clamp(mother_age_at_birth, base_age*1.5, int(base_age*2.6))

    if father_age_at_birth > mother_age_at_birth:
        parent_start_year = int(year - (father_age_at_birth - base_age))  # 1000 - (30 - 20) = 990
    else:
        parent_start_year = int(year - (mother_age_at_birth - base_age))

    siblings = []
    father_married = False
    mother_married = False
    parents_married_together = False
    father_left = False
    father_deceased = False
    mother_deceased = False
    mother_left = False
    parents_broken_up = False

    event_id = 0
    for y in range(parent_start_year, year):
        father_age = int(father_age_at_birth - (year - y))
        mother_age = int(mother_age_at_birth - (year - y))
        main_person_age = int(y - year)

        f_emo = biorhythms_at_age(mods=father_attribute_mods, age=father_age, economic=father_economic, education=father_education, conflict=father_conflict)
        m_emo = biorhythms_at_age(mods=mother_attribute_mods, age=mother_age, economic=mother_economic, education=mother_education, conflict=mother_conflict)

        #TODO: This is all kinda hacky and should be in the Components rules engine
        details = []
        # import ipdb; ipdb.set_trace()
        if not parents_broken_up and not parents_married_together and not father_married and not mother_married:
            if (f_emo["Passion"] + m_emo["Passion"]) > 0 and (f_emo["Conscience"] + m_emo["Conscience"]) > 0 \
                    and (f_emo["Happiness"] + m_emo["Happiness"]) > 0\
                    and father_age > base_age and mother_age > base_age\
                    and not father_deceased and not mother_deceased:

                details.append("Father and Mother were married together")
                father_married = True
                mother_married = True
                parents_married_together = True
                father_attribute_mods["Happiness"] += 2
                mother_attribute_mods["Happiness"] += 2
                father_attribute_mods["Passion"] += 1
                mother_attribute_mods["Passion"] += 1
                father_economic -= 2
                mother_economic -= 2

        if not father_married and f_emo["Passion"] > 2 and f_emo["Conscience"] > 3 and father_age > base_age and not father_deceased:
            details.append("Father was married to someone else")
            father_married = True
            father_attribute_mods["Happiness"] += 2
            father_attribute_mods["Passion"] += 1
            father_economic -= 3

        if not mother_married and m_emo["Passion"] > 2 and m_emo["Conscience"] > 3 and mother_age > base_age and not mother_deceased:
            details.append("Mother was married to someone else")
            mother_married = True
            mother_attribute_mods["Happiness"] += 2
            mother_attribute_mods["Passion"] += 1
            mother_economic -= 3

        #Have a child if no one was married
        if len(details) == 0:
            if not mother_married and (m_emo["Passion"]-len(siblings)) > 3 and mother_age > base_age and not mother_deceased:
                sibling_dna = dna_helpers.combine_dna(mother=mother_dna)[0]
                child_gender = dna_helpers.gender_from_dna(sibling_dna)
                child_name = story_helpers.create_random_name(world_data=world_data, pattern='namefile', tags=mother_tags, gender=child_gender)['name'] + " " + mother_family_name
                siblings.append({"dna": sibling_dna, "gender": child_gender, "born": y, "father": "Other", "Mother": "Yours", "name": child_name})
                details.append("Mother had a " + child_gender + " child (" + child_name + ") while unmarried")

                mother_attribute_mods["Happiness"] -= 3
                mother_attribute_mods["Constitution"] -= 2
                mother_attribute_mods["Passion"] -= 4
                mother_economic -= 3
                mother_conflict += 1
                mother_education += 2

            if not father_married and (f_emo["Passion"]-len(siblings)) > 4 and father_age > base_age and not father_deceased:
                sibling_dna = dna_helpers.combine_dna(father=father_dna)[0]
                child_gender = dna_helpers.gender_from_dna(sibling_dna)
                child_name = story_helpers.create_random_name(world_data=world_data, pattern='namefile', tags=father_tags, gender=child_gender)['name'] + " " + father_family_name
                siblings.append({"dna": sibling_dna, "gender": child_gender, "born": y, "father": "Yours", "Mother": "Other", "name": child_name})
                details.append("Father had a " + child_gender + " child (" + child_name + ") while unmarried")

                father_attribute_mods["Happiness"] -= 1
                father_attribute_mods["Constitution"] -= 1
                father_attribute_mods["Passion"] -= 4
                father_economic -= 3
                father_conflict += 2
                father_education += 1

            elif parents_married_together and (f_emo["Passion"]+m_emo["Passion"]-len(siblings)) > 2 \
                    and f_emo["Conscience"]+m_emo["Conscience"] > 2 \
                    and father_age > base_age and mother_age > base_age and not father_deceased and not mother_deceased:

                sibling_dna = dna_helpers.combine_dna(father=father_dna, mother=mother_dna)[0]
                child_gender = dna_helpers.gender_from_dna(sibling_dna)
                child_name = story_helpers.create_random_name(world_data=world_data, pattern='namefile', tags=father_tags, gender=child_gender)['name'] + " " + father_family_name
                siblings.append({"dna": sibling_dna, "gender": child_gender, "born": y, "father": "Yours", "Mother": "Yours", "name": child_name})
                details.append("Your parents had a " + child_gender + " child (" + child_name + ") while married together")

                father_attribute_mods["Happiness"] -= 1
                father_attribute_mods["Passion"] -= 1
                father_attribute_mods["Constitution"] -= 1
                father_attribute_mods["Conscienciousness"] += 2

                mother_attribute_mods["Passion"] -= 3
                mother_attribute_mods["Constitution"] -= 2
                mother_attribute_mods["Conscienciousness"] += 2

                father_economic -= 1
                mother_economic -= 1
                father_conflict -= 2
                mother_conflict -= 2
                father_education += 1
                mother_education += 1

            elif not parents_married_together and mother_married and (m_emo["Passion"]-len(siblings)) > 5 and m_emo["Conscience"] > 2 \
                    and mother_age > base_age and not mother_deceased:
                sibling_dna = dna_helpers.combine_dna(mother=mother_dna)[0]
                child_gender = dna_helpers.gender_from_dna(sibling_dna)
                child_name = story_helpers.create_random_name(world_data=world_data, pattern='namefile', tags=mother_tags, gender=child_gender)['name'] + " " + mother_family_name
                siblings.append({"dna": sibling_dna, "gender": child_gender, "born": y, "father": "Husband", "Mother": "Yours", "name": child_name})
                details.append("Mother had a " + child_gender + " child (" + child_name + ") while married to someone else")

                mother_attribute_mods["Happiness"] -= 1
                mother_attribute_mods["Passion"] -= 3
                mother_attribute_mods["Constitution"] -= 2
                mother_economic -= 1
                mother_conflict -= 1
                mother_education += 2

            if not parents_married_together and father_married and (f_emo["Passion"]-len(siblings)) > 5 and f_emo["Conscience"] > 2 \
                    and father_age > base_age and not father_deceased:
                sibling_dna = dna_helpers.combine_dna(father=father_dna)[0]
                child_gender = dna_helpers.gender_from_dna(sibling_dna)
                child_name = story_helpers.create_random_name(world_data=world_data, pattern='namefile', tags=mother_tags, gender=child_gender)['name'] + " " + father_family_name
                siblings.append({"dna": sibling_dna, "gender": child_gender, "born": y, "father": "Yours", "Mother": "Wife", "name": child_name})
                details.append("Father had a " + child_gender + " child (" + child_name + ") while married to someone else")

                father_attribute_mods["Happiness"] -= 1
                father_attribute_mods["Passion"] -= 3
                father_attribute_mods["Constitution"] -= 1
                father_economic -= 1
                father_conflict -= 2
                father_education += 1

        #Leave each other if things go poorly
        if parents_married_together and (f_emo["Passion"]+m_emo["Passion"]-len(siblings)) < -3 \
                and f_emo["Conscience"]+m_emo["Conscience"] < -3 and not father_deceased and not mother_deceased:
            details.append("Parents left each other")
            parents_married_together = False
            father_married = False
            mother_married = False
            mother_attribute_mods["Happiness"] += 1
            mother_attribute_mods["Passion"] += 1
            mother_attribute_mods["Anger"] += 1
            father_attribute_mods["Happiness"] += 1
            father_attribute_mods["Passion"] += 1
            father_attribute_mods["Anger"] += 1
            mother_economic -= 2
            father_economic -= 2
            parents_broken_up = True

            if f_emo["Conscience"] < m_emo["Conscience"]:
                father_left = True
                father["left"] = y
            else:
                mother_left = True
                mother["left"] = y

        elif not parents_married_together and mother_married and m_emo["Passion"] < 0 and m_emo["Conscience"] < 3 and m_emo["Happiness"] < 2 and not mother_deceased:
            details.append("Mother left her husband")
            mother_married = False
            mother_attribute_mods["Happiness"] += 2
            mother_attribute_mods["Passion"] += 1
            mother_attribute_mods["Anger"] += 1
            mother_economic -= 2

        elif not parents_married_together and father_married and f_emo["Passion"] < 0 and f_emo["Conscience"] < 3 and f_emo["Happiness"] < 2 and not father_deceased:
            details.append("Father left his wife")
            father_married = False
            father_attribute_mods["Happiness"] += 1
            father_attribute_mods["Passion"] += 2
            father_attribute_mods["Anger"] += 1
            father_economic -= 3

        #Annual family modifiers
        father_economic_tithe = float(father_economic) * .05
        mother_economic_tithe = float(mother_economic) * .05

        if father_age < 17:
            pass
        elif father_age > 45:
            father_attribute_mods["Constitution"] -= 1
        elif father_age < 25:
            father_attribute_mods["Passion"] += .5
            father_attribute_mods["Happiness"] += .5
            father_attribute_mods["Constitution"] += .5
            father_attribute_mods["Conscienciousness"] += .5
        elif father_age > 40:
            father_attribute_mods["Wisdom"] += .5
        elif father_age > 30:
            father_attribute_mods["Conscienciousness"] += .5

        if mother_age < 17:
            pass
        elif mother_age > 45:
            mother_attribute_mods["Constitution"] -= 1
        elif mother_age < 25:
            mother_attribute_mods["Passion"] += .5
            mother_attribute_mods["Happiness"] += .5
            mother_attribute_mods["Constitution"] += .5
            mother_attribute_mods["Conscienciousness"] += .5
        elif mother_age > 40:
            mother_attribute_mods["Wisdom"] += .5
        elif mother_age > 30:
            mother_attribute_mods["Conscienciousness"] += .5

        father_economic += father_economic * numpy.random.random()/40.0
        mother_economic += mother_economic * numpy.random.random()/40.0

        if parents_married_together and not father_deceased and not mother_deceased:
            if father_economic > mother_economic:
                father_economic -= father_economic_tithe
                mother_economic += father_economic_tithe
            else:
                father_economic += mother_economic_tithe
                mother_economic -= mother_economic_tithe

        if father_married and not father_deceased:
            for improvement in numpy.random.choice("Extraversion,Artistic,Happiness,Happiness,Happiness,Business,Meekness,Conscienciousness,Religiousness".split(","), 2):
                father_attribute_mods[improvement] += 1
            for improvement in numpy.random.choice("Appearance,Passion,Constitution,Realism".split(","), 1):
                father_attribute_mods[improvement] -= 1
            house += father_economic_tithe
            father_economic -= father_economic_tithe

        if mother_married and not mother_deceased:
            for improvement in numpy.random.choice("Extraversion,Artistic,Happiness,Passion,Meekness,Conscienciousness,Conscienciousness,Conscienciousness,Religiousness".split(","), 2):
                mother_attribute_mods[improvement] += 1
            for improvement in numpy.random.choice("Appearance,Constitution,Realism".split(","), 1):
                mother_attribute_mods[improvement] -= 1
            house += mother_economic_tithe
            mother_economic -= mother_economic_tithe

        if father_economic < 2:
            father_attribute_mods["Happiness"] -= 1

        if mother_economic < 2:
            mother_attribute_mods["Happiness"] -= 1

        #TODO: Parents should be deceased as kid isn't born yet... maybe tee that up to happen after birth?
        if not father_deceased and f_emo["Health"] < -10:
            father_deceased = True
            father_married = False
            parents_married_together = False
            father["deceased"] = y
        if not mother_deceased and m_emo["Health"] < -10:
            mother_deceased = True
            mother_married = False
            parents_married_together = False
            mother["deceased"] = y

        #TESTING
        father["emotions"] = f_emo
        mother["emotions"] = m_emo

        family["father"] = father
        family["mother"] = mother

        if house > 60:
            family["house"] = "Superb"
        elif house > 40:
            family["house"] = "Great"
        elif house > 20:
            family["house"] = "Average"
        elif house > 5:
            family["house"] = "Poor"
        else:
            family["house"] = "Tiny"

        family["economic"] = father_economic+mother_economic / 2
        family["education"] = father_education+mother_education / 2
        family["conflict"] = father_conflict+mother_conflict / 2

        world_data["family"] = family
        world_data["year"] = y

        w_data = str(world_data)
        TESTING = False
        if TESTING:
            if not len(details):
                details.append("Nothing significant")
            w_data = "Father: "
            for key, val in f_emo.iteritems():
                w_data += "<br/>" + key + ": " + str(val)
            w_data += "<br/><br/>Mother: "
            for key, val in m_emo.iteritems():
                w_data += "<br/>" + key + ": " + str(val)

        if len(details):

            event_details = {"id": event_id, "age": main_person_age, "year": y, "message": ", ".join(details), "world_data": w_data}
            family_events.append(event_details)
            event_id += 1

    return family_events


def biorhythms_at_age(mods=[], age=17, economic=42.0, education=21.0, conflict=10.0):
    economic = math_helpers.value_of_variable(economic)
    education = math_helpers.value_of_variable(education)
    conflict = math_helpers.value_of_variable(conflict)

    happy = math_helpers.get_formula_from_obj(mods, "Happiness,Anger-,Terror-,Extraversion,Intelligence-,Meekness,Appearance,Realism-", -10, 10)
    passion = math_helpers.get_formula_from_obj(mods, "Artistic,Extraversion,Constitution,Religiousness-,Constraint-,Realism-,Passion,Meekness-", -10, 10)
    conscience = math_helpers.get_formula_from_obj(mods, "Conscienciousness,Terror-,Intelligence,Manipulation-,Charisma", -10, 10)
    health = math_helpers.get_formula_from_obj(mods, "Constitution,Strength,Dexterity,Anger-,Intelligence,Weight-,Lifespan,Neuroticism-,Immune System", -10, 10)

    if age > 60:
        conscience += 3
        passion -= 3
    elif age > 40:
        conscience += 1
        passion -= 1
    elif age > 20:
        conscience -= 1
        passion += 3
        happy += 2

    if education >= 40.0:
        conscience += 3
        happy -= 1
        passion += 1
    elif education >= 13:
        conscience += 1
        passion -= 1
        happy -= 1
    elif education >= 5:
        conscience -= 1
        passion += 2
        happy += 1

    if economic >= 40.0:
        conscience -= 3
        happy += 3
        passion += 2
    elif economic >= 13:
        conscience -= 1
        passion += 1
        happy += 1
    elif economic >= 5:
        conscience += 1
        passion += 1
        happy -= 1

    if conflict >= 40.0:
        conscience -= 3
        happy -= 2
        passion += 2
    elif conflict >= 13:
        conscience -= 2
        passion += 1
        happy -= 2
    elif conflict >= 5:
        conscience -= 1
        passion += 1
        happy -= 1

    # rands = numpy.random.randint(-2, 2, 4)
    # happy = math_helpers.clamp(happy+rands[0], -10, 10)
    # passion = math_helpers.clamp(passion+rands[1], -10, 10)
    # conscience = math_helpers.clamp(conscience+rands[2], -10, 10)
    # health = math_helpers.clamp(health+rands[3], -10, 10)

    return {"age": age, "Happiness": happy, "Passion": passion, "Conscience": conscience, "Health": health, "economic": economic, "Education": education, "Conflict": conflict}


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


    #TODO: Have an economic lookup engine
    #TODO: Use ranks if economic and world says so
    #TODO: Determine nationality, use names from those
