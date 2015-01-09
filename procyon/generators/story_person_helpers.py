from procyon.starsystemmaker import math_helpers
import dna_helpers
import json
import world
import numpy

#-----------------------------------------

#TODO: Grandparents
#TODO: Nanny or Caretaker if ec > high
#TODO: What to do with education? Job?
#TODO: Create city
#TODO: Ranks or royalty
#TODO: Adoptions
#TODO: Same-sex marriages
#TODO: Have an economic lookup engine
#TODO: Use ranks if economic and world says so
#TODO: Determine nationality, use names from those
#TODO: Return list of people, with world snapshots for each year


def generate_world_and_events(world_obj=None):
    if world_obj is None:
        world_obj = world.World()

    try:
        rand_seed = float(world_obj.get('rand_seed'))
    except ValueError:
        rand_seed = numpy.random.random()
    except TypeError:
        rand_seed = numpy.random.random()

    rand_seed = math_helpers.set_rand_seed(rand_seed)
    world_obj.set('rand_seed', rand_seed)

    #Calculate Parents History
    family_events = []

    #Generate Father
    father_data = world_obj.get('family.father')
    father = world.Person(world_obj, data=father_data, gender='Male', role='Father')
    father.dna = father.get("dna", dna_helpers.generate_dna()[0], random_number=False)
    if not father.get("family_name", None):
        father.create_name(create_new_last=True)
    message = father.name + " (Father) was born in " + str(father.birth_year)
    event_data = {"id": -2, "year": father.birth_year, "message": message, "significance": 0, 'people': world_obj.people_copy}
    family_events.append(event_data)

    #Generate Mother
    mother_data = world_obj.get('family.mother')
    mother = world.Person(world_obj, data=mother_data, gender='Female', role='Mother')
    mother.dna = mother.get("dna", dna_helpers.generate_dna()[0], random_number=False)
    if not mother.get("family_name", None):
        mother.create_name(create_new_last=True)
    message = mother.name + " (Mother) was born in " + str(mother.birth_year)
    event_data = {"id": -1, "year": father.birth_year, "message": message, "significance": 0, 'people': world_obj.people_copy}
    family_events.append(event_data)

    if father.age > mother.age:
        start_sim_year = int(world_obj.year - father.age + world_obj.age_of_consent)
    else:
        start_sim_year = int(world_obj.year - mother.age + world_obj.age_of_consent)
    end_sim_year = int(world_obj.year + 30)

    world_starter_year = world_obj.year

    years_data = []

    event_id = 0
    for y in range(start_sim_year, end_sim_year):
        world_obj.set("year", y)

        for p in world_obj.people_objects:
            p.update_biorhythms()

        details = []
        # import ipdb; ipdb.set_trace()
        if mother.can_marry and father.can_marry:
            mother.get_married(father)
            father.get_married(mother)
            details.append("Father (age "+str(father.age)+") and Mother (age "+str(mother.age)+") were married together")

        elif mother.can_marry and mother.passion > 2:
            spouse = mother.get_married()
            details.append("Mother (age "+str(+mother.age)+") was married to " + spouse.name)

        elif father.can_marry and father.passion > 2:
            spouse = father.get_married()
            details.append("Father (age "+str(father.age)+") was married to " + spouse.name)

        elif not mother.married and mother.chance_to_have_child():
            child = mother.have_child(event_id=event_id)
            details.append("Mother (age "+str(mother.age)+") had a " + child.gender + " child (" + child.name + ") while unmarried")
            birth_event = child.get('birth_event', None)
            if birth_event:
                details.append(birth_event.get('message'))

        elif not father.married and father.chance_to_have_child():
            child = father.have_child(event_id=event_id)
            details.append("Father (age "+str(father.age)+") had a " + child.gender + " child (" + child.name + ") while unmarried")
            birth_event = child.get('birth_event', None)
            if birth_event:
                details.append(birth_event.get('message'))

        elif father.is_married_to(mother) and father.chance_to_have_child() and mother.chance_to_have_child():
            child = father.have_child(spouse=mother, event_id=event_id)
            details.append("Father (age "+str(father.age)+") and Mother (age "+str(mother.age)+") had a " + child.gender + " child (" + child.name + ") while married together")
            birth_event = child.get('birth_event', None)
            if birth_event:
                details.append(birth_event.get('message'))

        elif not mother.is_married_to(father) and mother.married and mother.chance_to_have_child():
            spouse = mother.spouse
            child = mother.have_child(spouse=spouse, event_id=event_id)
            message = "Mother (age "+str(mother.age)+") had a " + child.gender + " child (" + child.name + ") while married to ("+spouse.name+")"
            details.append(message)
            birth_event = child.get('birth_event', None)
            if birth_event:
                details.append(birth_event.get('message'))

        elif not father.is_married_to(mother) and father.married and father.chance_to_have_child():
            spouse = father.spouse
            child = father.have_child(spouse=spouse, event_id=event_id)
            message = "Father (age "+str(father.age)+") had a " + child.gender + " child (" + child.name + ") while married to ("+spouse.name+")"
            details.append(message)
            birth_event = child.get('birth_event', None)
            if birth_event:
                details.append(birth_event.get('message'))

        #Leave each other if things go poorly
        elif father.married and father.conscience < -3 and father.passion < -3 and not father.deceased:
            details.append("Father (age "+str(father.age)+") left his family")
            father.leave_family()

        elif mother.married and mother.conscience < -4 and mother.passion < -4 and not mother.deceased:
            details.append("Mother (age "+str(mother.age)+") left her family")
            mother.leave_family()

        math_helpers.dict_round_floats(father.output, places=3)
        math_helpers.dict_round_floats(mother.output, places=3)
        math_helpers.dict_round_floats(world_obj.world_data, places=1)

        #TODO: instead of list of events, return array of people with updates per year
        significance = 1
        if not len(details):
            significance = 0
            details.append("Nothing eventful occurred")

        event_data = {"id": event_id, "year": y, "message": ", ".join(details), "significance": significance,
                      "people": world_obj.people[:]}

        family_events.append(event_data)
        event_id += 1


        years_data.append({"year": y, "events": details, "people": world_obj.people_copy})
        #End Sim loop

    world_obj.set('year', world_starter_year)

    #return family_events, world_obj.people
    return years_data


def world_info():
    # Testing function for command line vieweing

    years_data = generate_world_and_events()

    for year_data in years_data:
        year = year_data.get("year", 1000)
        people = year_data.get("people", [])
        out = str(year) + ": "
        for p in people:
            out += p.get('name') + "(" + str(p.get('age')) + "), "

        print(out)


def person_info(p):
    msg = str(p.get('birth_year')) + ": (" + p.get('role','') + ') ' + str(p.get('age')) + " = " + p.get('name')
    msg += ' Mom:'+p.get('mother_name','') + ' Dad:'+p.get('father_name','') + ' Spouse:'+p.get('spouse_name','')
    return msg