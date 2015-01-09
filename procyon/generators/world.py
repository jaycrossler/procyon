from procyon.starsystemmaker import math_helpers
from procyon.generators import dna_helpers
import json
import numpy
from procyon.generators.story_helpers import create_random_name, apply_event_effects, create_random_item
#import ipdb

PERSON_DEFAULT_DICT = {
    "dna": "",
    "rand_seed": 42,
    "tags": "",
    "family_name": "",
    "economic": 4,
    "education": 4,
    "conflict": 4,
    "gender": "Male",
    "race": "Human",
    "profession": "Farmer",
    "birth_year": None,
    "married": False,
    "left": False,
    "spouse": False,
    "deceased": False,
    "house": 4
}

WORLD_DEFAULT_DICT = {
    "magic": None,
    "technology": None,
    "year": None,
    "people": [],
    "family": {"father": {}, "mother": {}}
}


def initialize_family_settings_from_request(req_obj):
    rand_seed = req_obj.get('rand_seed') or ''

    if req_obj.get('regenerate', None):
        # A button was pushed with the name 'regenerate'
        rand_seed = ''

    world_json = req_obj.get('world_json') or ''
    world_data = json.loads(world_json) if world_json else {}

    mother_dna = req_obj.get('mother_dna') or ''
    mother_race = req_obj.get('mother_race') or 'Human'
    mother_profession = req_obj.get('mother_profession') or ''
    mother_education = req_obj.get('mother_education') or ''
    mother_economic = req_obj.get('mother_economic') or ''
    mother_conflict = req_obj.get('mother_conflict') or ''
    mother = {"dna": mother_dna, "race": mother_race, "profession": mother_profession,
              "education": mother_education, "economic": mother_economic,
              "conflict": mother_conflict}

    father_dna = req_obj.get('father_dna') or ''
    father_race = req_obj.get('father_race') or 'Human'
    father_profession = req_obj.get('father_profession') or ''
    father_education = req_obj.get('father_education') or ''
    father_economic = req_obj.get('father_economic') or ''
    father_conflict = req_obj.get('father_conflict') or ''
    father = {"dna": father_dna, "race": father_race, "profession": father_profession,
              "education": father_education, "economic": father_economic,
              "conflict": father_conflict}

    family = world_data.get("family", {})
    mother_f = family.get("mother", {})
    father_f = family.get("father", {})
    family["mother"] = math_helpers.extend(PERSON_DEFAULT_DICT, mother_f, mother)
    family["father"] = math_helpers.extend(PERSON_DEFAULT_DICT, father_f, father)

    world_data = math_helpers.extend(WORLD_DEFAULT_DICT, world_data)
    world_data["rand_seed"] = rand_seed
    world_data["family"] = family

    return world_data


class World(object):
    def __init__(self, world_data={}):
        self.world_data = world_data

        self.year = self.get('year', numpy.random.randint(1000, 2000))

        self.world_data = math_helpers.extend(WORLD_DEFAULT_DICT, self.world_data)

        self.tag_manager = {}
        starting_tags = math_helpers.get_val(world_data, 'tags', '')
        math_helpers.add_tags(self.tag_manager, 'initial', starting_tags)

        magic = self.get('magic', random_number=True)
        magic = round(magic, 1)
        self.set('magic', magic)

        tech = self.get('technology', random_number=True)
        tech = round(tech, 1)
        self.set('technology', tech)

        self.people = self.get('people', [])
        self.people_objects = []

    def get(self, val='', default=None, random_number=False, min=0.0, mid=0.2, max=120.0, weight=4, use_words=False):
        return math_helpers.get_val(self.world_data, val=val, default=default, use_words=use_words,
                                    random_number=random_number, min=min, mid=mid, max=max, weight=weight)

    def set(self, val, amount, use_words=False):
        return math_helpers.set_val(self.world_data, val=val, amount=amount, use_words=use_words)

    # -------------------------------------------

    def get_person(self, name):
        found_person = False
        for person in self.people_objects:
            if isinstance(person, Person) and person.name and person.name.lower() == name.lower():
                found_person = person
                break
        return found_person

    def add_person(self, person_obj):
        person_name = person_obj.get('name')
        if person_name and self.get_person(person_name):
            # already exists
            pass
        else:
            if isinstance(person_obj, Person):
                self.people_objects.append(person_obj)
                self.people.append(person_obj.output)
            else:
                raise Exception("world.add_person of a non-Person object")

    @property
    def people_copy(self):
        people = []
        for p in self.people_objects:
            people.append(p.output)

        return people

    @property
    def tags(self):
        tags = math_helpers.flatten_tags(self.tag_manager)

        if self.get('magic') > 20.0:
            tags += ', magical'
        if self.get('magic') > 60.0:
            tags += ', high-magic'
        if self.get('technology') > 20.0:
            tags += ', technical'
        if self.get('technical') > 60.0:
            tags += ', high-tech'

        return tags

    def get_tags(self, category):
        return math_helpers.flatten_tags(self.tag_manager, area=category)

    def set_tags(self, category, tags):
        if not isinstance(tags, list):
            tags = [tags]
        math_helpers.add_tags(self.tag_manager, category, tags)

    @property
    def year(self):
        return self.get('year', 1100)

    @year.setter
    def year(self, val):
        self.set('year', val)

    @property
    def age_of_consent(self):
        # Being "of age" changes through the years, from 14 to 20
        # TODO: Modify this by racial longevity
        return int(math_helpers.percent_range(value=self.year, start_min=1000, start_max=2000, end_min=14, end_max=20))

    def export_object(self):
        world_data_copy = self.world_data.copy()
        father = world_data_copy.get("family.father", {})
        mother = world_data_copy.get("family.mother", {})

        father["economic"] = math_helpers.word_from_value(father.get("economic", 0))
        mother["economic"] = math_helpers.word_from_value(mother.get("economic", 0))
        father["education"] = math_helpers.word_from_value(father.get("education", 0))
        mother["education"] = math_helpers.word_from_value(mother.get("education", 0))
        father["conflict"] = math_helpers.word_from_value(father.get("conflict", 0))
        mother["conflict"] = math_helpers.word_from_value(mother.get("conflict", 0))

        world_json = json.dumps(world_data_copy)

        inputs = {
            "tags": self.tags,
            "rand_seed": self.world_data.get('rand_seed'),
            "father": father,
            "mother": mother,
            "world_json": world_json
        }
        return inputs

    def to_JSON(self):
        json_copy = self.world_data.copy()
        # people = []
        # for person in self.people:
        #     people.append(person.output_short)
        #
        # json_copy["people"] = people
        return json_copy


class Person(object):
    def __init__(self, world_obj, data={}, gender=None, role='Child'):

        if isinstance(world_obj, World):
            self.world_obj = world_obj
        else:
            raise Exception('Non-World Object passed to Person')

        if not data:
            data = {}

        if isinstance(data, Person):
            data = data.output

        if not isinstance(data, dict):
            raise Exception('Non-dict Data passed to Person')

        self.pointer = math_helpers.extend(PERSON_DEFAULT_DICT, data)

        self.rand_seed_counter = numpy.random.randint(1, 100000)
        self.attribute_base = {}
        self.attribute_mods_dict = {}
        self.qualities_base = {}
        self.quality_mods_dict = {}

        self.role = role
        # if not self.dna:
        #     self.generate_dna()

        if gender:
            self.gender = gender
        family_name = self.get('family_name', None)
        if family_name:
            self.family_name = family_name
            self.create_name()
        else:
            self.create_name(create_new_last=True)
        self.world_obj.add_person(self)

    def get(self, val='', default=None, random_number=False, min=0.0, mid=0.2, max=120.0, weight=4, use_words=False):
        return math_helpers.get_val(self.pointer, val=val, default=default, use_words=use_words,
                                    random_number=random_number, min=min, mid=mid, max=max, weight=weight)

    def set(self, val, amount, use_words=False):
        return math_helpers.set_val(self.pointer, val=val, amount=amount, use_words=use_words)

    @property
    def father(self):
        father_name = self.get('father_name', None)
        if not father_name:
            father_data = self.create_name(gender='Male', set_to_person=False)
            father_name = father_data.get('name','')
            self.set('father_name', father_name)

        father = self.world_obj.get_person(father_name)
        #TODO: As a backup, scan through people to see if anyone has self listed as a kid?
        if not father:
            father_data = {"name": father_name,
                           "family_name": self.family_name,
                           "age": self.age + numpy.random.randint(40) + self.world_obj.age_of_consent
            }
            role = 'Grandfather' if self.role in ['Father', 'Mother'] else 'Father'
            father = Person(self.world_obj, data=father_data, gender='Male', role=role)
            self.world_obj.add_person(father)
        return father

    @property
    def mother(self):
        mother_name = self.get('mother_name', None)
        mother_family_name = ''
        if not mother_name:
            name_obj = create_random_name(world_data=self.world_obj.world_data, tags=self.world_obj.tags,
                                          rand_seed=self.rand_seed_next, gender='Female',
                                          pattern=self.name_file_pattern)
            mother_name = name_obj['name']
            self.set('mother_name', mother_name)

            mother_family_name = name_obj['name_parts'][-1]

        mother = self.world_obj.get_person(mother_name)
        if not mother:
            mother_data = {"name": mother_name,
                           "family_name": mother_family_name,
                           "age": self.age + numpy.random.randint(30) + self.world_obj.age_of_consent
            }
            role = 'Grandmother' if self.role in ['Father', 'Mother'] else 'Mother'
            mother = Person(self.world_obj, data=mother_data, gender='Female', role=role)
        return mother

    @property
    def married(self):
        if self.deceased:
            is_married = False
        else:
            is_married = self.get('married', default=False)
        return is_married

    @married.setter
    def married(self, is_married):
        self.set('married', is_married)

    @property
    def can_marry(self):
        if self.deceased or self.married:
            can_married = False
        else:
            can_married = self.age_past_consent and self.happy > 0
        return can_married

    @property
    def deceased(self):
        return self.get('deceased', default=False)

    @deceased.setter
    def deceased(self, is_deceased):
        self.set('deceased', is_deceased)

    @property
    def dna(self):
        return self.get('dna', default='')

    @dna.setter
    def dna(self, dna_string):
        self.set('dna', dna_string)

    def generate_dna(self, force_generation_if_exists=False):
        if force_generation_if_exists or self.dna is '' or self.dna and len(self.dna) < 3:
            self.dna, temp = dna_helpers.combine_dna(self.mother.dna, self.father.dna, self.rand_seed_counter)
            self.dna = dna_helpers.set_dna_gender(self.dna, self.gender)

    @property
    def race(self):
        val = self.get('race', default='Human')
        if val and self.dna:
            val_dna = dna_helpers.race_from_dna(self.dna)
            if val is not val_dna:
                self.race = val_dna
                val = val_dna
        return val

    @race.setter
    def race(self, race_string):
        self.set('race', race_string)

    @property
    def gender(self):
        val = self.get('gender', default='')
        if val and self.dna:
            val_dna = dna_helpers.gender_from_dna(self.dna)
            if val is not val_dna:
                self.gender = val_dna
                val = val_dna
        return val

    @gender.setter
    def gender(self, gender_string):
        self.set('gender', gender_string)
        #TODO: Set DNA before gender
        new_dna = dna_helpers.set_dna_gender(self.dna, gender=gender_string)
        self.set('dna', new_dna)

    @property
    def rand_seed_next(self):
        self.rand_seed_counter += 1

        rand_seed = self.world_obj.get('rand_seed', default=None)
        if rand_seed:
            rand_seed = str(rand_seed) + str(self.rand_seed_counter)
            try:
                rand_seed = float(rand_seed)
            except ValueError:
                rand_seed = numpy.random.random()
        else:
            rand_seed = numpy.random.random()

        return rand_seed

    # birth_place = create_random_item(world_data=world_obj.world_data, set_random_key=False, pattern='birthplace')

    @property
    def nationality(self):
        # Earth-based nationality used for DNA, Names, Cultural Norms
        return self.get('nationality', 'European')

    @nationality.setter
    def nationality(self, val):
        self.set('nationality', val)

    @property
    def rank(self):
        # TODO: Base on nationality
        return self.get('rank', 'Commoner')

    @rank.setter
    def rank(self, val):
        self.set('rank', val)

    @property
    def name(self):
        return self.get('name')

    @name.setter
    def name(self, val):
        self.set('name', val.title())

    @property
    def family_name(self):
        val = self.get('family_name', default='')
        if not val:
            val = self.get('family.father.family_name', default='')
            if not val:
                val = self.get('family.mother.family_name', default='')
                if not val:
                    name_obj = create_random_name(world_data=self.world_obj.world_data, tags=self.world_obj.tags,
                                                  rand_seed=self.rand_seed_next, pattern='namefile|family')
                    val = name_obj.get('name')
            self.family_name = val
        return val

    @family_name.setter
    def family_name(self, name_string):
        self.set('family_name', name_string)

    @property
    def name_file_pattern(self):
        # TODO: Differ based on nationality, rank
        pattern = self.get('name_file_pattern', None)
        if not pattern:
            pattern = 'namefile,namefile,namefile|given'
            if self.nationality is 'European' and self.rank is 'Commoner':
                pattern = 'namefile,namefile|given'
            if self.nationality is 'Asian' and self.rank is 'Commoner':
                pattern = 'namefile|given,namefile,namefile'

        return pattern

    @name_file_pattern.setter
    def name_file_pattern(self, val):
        self.set('name_file_pattern', val)

    def create_name(self, set_to_person=True, gender=None, create_new_last=False):
        if gender is None:
            gender = self.gender
        if create_new_last:

            name_obj = create_random_name(world_data=self.world_obj.world_data, tags=self.world_obj.tags,
                                          rand_seed=self.rand_seed_next, gender=gender,
                                          pattern=self.name_file_pattern)
            self.family_name = name_obj.get('name_parts')[-1]

        else:
            name_obj = create_random_name(world_data=self.world_obj.world_data, tags=self.world_obj.tags,
                                          rand_seed=self.rand_seed_next, gender=gender,
                                          pattern=self.name_file_pattern,
                                          override={'namefile|given': self.family_name})
        name = name_obj['name']
        if set_to_person:
            self.name = name
        return name_obj

    @property
    def age(self):
        birth_year = self.birth_year
        if birth_year is None:
            age_mod = math_helpers.rand_range(low=0, high=40 if self.gender is 'Male' else 30, avg=0.1)
            age = self.world_obj.age_of_consent + age_mod
            self.set("birth_year", int(self.world_obj.year - age))
        else:
            age = int(self.world_obj.year) - int(birth_year)

        return age

    def age_at_year(self, year):
        return int(year) - int(self.birth_year)

    @property
    def age_past_consent(self):
        return self.age >= self.world_obj.age_of_consent

    @property
    def birth_year(self):
        return self.get("birth_year", None)

    def mutate(self):
        math_helpers.set_rand_seed(self.rand_seed_next)
        self.dna = dna_helpers.mutate_dna(self.dna)

    @property
    def aspects(self):
        return dna_helpers.aspects_from_dna(self.dna)

    @property
    def skills(self):
        return self.get('skills', [])

    @property
    def items(self):
        return self.get('items', [])

    @property
    def economic(self):
        val = self.get('economic', random_number=True)
        if isinstance(val, float):
            val = round(val, 2)
        return val

    @economic.setter
    def economic(self, val):
        self.set('economic', val)

    @property
    def education(self):
        val = self.get('education', random_number=True)
        if isinstance(val, float):
            val = round(val, 2)
        return val

    @education.setter
    def education(self, val):
        self.set('education', val)

    @property
    def conflict(self):
        val = self.get('conflict', random_number=True)
        if isinstance(val, float):
            val = round(val, 2)
        return val

    @conflict.setter
    def conflict(self, val):
        self.set('conflict', val)

    @property
    def conscience(self):
        val = self.get('conscience', random_number=True, min=-10, max=20)
        if isinstance(val, float):
            val = round(val, 2)
        return val

    @conscience.setter
    def conscience(self, val):
        self.set('conscience', val)

    @property
    def happy(self):
        val = self.get('happy', random_number=True, min=-10, max=20)
        if isinstance(val, float):
            val = round(val, 2)
        return val

    @happy.setter
    def happy(self, val):
        self.set('happy', val)

    @property
    def passion(self):
        val = self.get('passion', random_number=True, min=-10, max=20)
        if isinstance(val, float):
            val = round(val, 2)
        return val

    @passion.setter
    def passion(self, val):
        self.set('passion', val)

    @property
    def health(self):
        val = self.get('health', random_number=True, min=-10, max=20)
        if isinstance(val, float):
            val = round(val, 2)
        return val

    @health.setter
    def health(self, val):
        self.set('health', val)

    @property
    def profession(self):
        # TODO: Modify by year and economics and others
        return self.get('profession', 'Farmer')

    @property
    def tags(self):
        tags = []
        tags_local = self.get('tags', '')
        if isinstance(tags_local, list):
            tags += tags_local
        elif isinstance(tags_local, str):
            tags += tags_local.split(",")

        tags.append(self.profession)
        if self.economic > math_helpers.value_of_variable('high'):
            tags.append('wealthy')
        if self.economic > math_helpers.value_of_variable('great'):
            tags.append('rich')
        if self.education > math_helpers.value_of_variable('high'):
            tags.append('educated')
        if self.education > math_helpers.value_of_variable('great'):
            tags.append('smart')

        # Lowercase, remove empties, and remove dupes
        tags = [tag.lower().strip() for tag in tags if tag]
        tags = list(set(tags))

        return ",".join(tags)

    @property
    def quality_mods(self):
        # Take mods from DNA combines with any ongoing mods and merge those
        if not self.qualities_base or not self.attribute_base:
            self.qualities_base, self.attribute_base = dna_helpers.qualities_from_dna(self.dna)

        qualities = self.qualities_base[:]  # using [:] is a way to copy the list
        for qual in self.quality_mods_dict:
            qualities = math_helpers.add_or_increment_dict_val(qualities, qual.get("name"), qual.get("value"))
        return qualities

    def quality_mod_update(self, quality_mods, amount=None):
        if isinstance(quality_mods, dict):
            quality_copies = quality_mods.copy()
            self.quality_mods_dict.update(quality_copies)
        elif isinstance(quality_mods, basestring) and amount is not None:
            current = math_helpers.get_val(self.quality_mods_dict, val=quality_mods, default=0)
            current += amount
            math_helpers.set_val(self.quality_mods_dict, val=quality_mods, amount=current)

    @property
    def attribute_mods(self):
        # Take mods from DNA combines with any ongoing mods and merge those
        if not self.qualities_base or not self.attribute_base:
            self.qualities_base, self.attribute_base = dna_helpers.qualities_from_dna(self.dna)

        attributes = self.attribute_base.copy()
        return math_helpers.add_or_merge_dicts(attributes, self.attribute_mods_dict)

    def attribute_mod_update(self, attribute_mods, amount=None):
        if isinstance(attribute_mods, dict):
            attribute_copies = attribute_mods.copy()
            self.attribute_mods_dict.update(attribute_copies)
        elif isinstance(attribute_mods, basestring) and amount is not None:
            current = math_helpers.get_val(self.attribute_mods_dict, val=attribute_mods, default=0)
            current += amount
            math_helpers.set_val(self.attribute_mods_dict, val=attribute_mods, amount=current)

    @property
    def role(self):
        self_role = self.get('role', None)
        if not self_role:
            family_role = 'Child'
            for person in self.world_obj.people_objects:
                if person.name and self.name and person.name.lower() == self.name.lower():
                    family_role = person.role
                    break
            self.role = family_role
            self_role = family_role
        return self_role

    @role.setter
    def role(self, val):
        self.set('role', val)
        for person in self.world_obj.people_objects:
            if person.name and self.name and person.name.lower() == self.name.lower():
                person.role = val
                break

    @property
    def num_kids(self):
        num = 0
        for person in self.world_obj.people_objects:
            if self.name and person.get('father_name', '').lower() is self.name.lower()\
                    or person.get('mother_name', '').lower() is self.name.lower():
                num += 1
        return num

    def leave_family(self):
        self.set('married', False)
        self.set('leave', self.world_obj.year)
        spouse_name = self.get('spouse_name', '')
        spouse = self.world_obj.get_person(spouse_name)
        self.set('spouse_name', None)

        self.attribute_mod_update('Happiness', 1)
        self.attribute_mod_update('Passion', 1)
        self.attribute_mod_update('Anger', 2)
        self.economic += numpy.random.randint(-4, -1)
        self.conflict += 2
        spouse.attribute_mod_update('Happiness', 1)
        spouse.attribute_mod_update('Passion', 1)
        spouse.attribute_mod_update('Anger', 2)
        spouse.economic += numpy.random.randint(-4, -1)
        spouse.conflict += 2

    def get_married(self, spouse=None):
        self.married = True
        if spouse is None:
            spouse_gender = 'Male' if self.gender is 'Female' else 'Female'
            role = 'Wife' if self.gender is 'Male' else 'Husband'
            spouse = Person(world_obj=self.world_obj, gender=spouse_gender, data={}, role=role)
            self.world_obj.add_person(spouse)
        self.set('spouse_name', spouse.name)
        self.attribute_mod_update('Happiness', 2)
        self.attribute_mod_update('Passion', 1)
        self.economic -= 2
        return spouse

    def is_married_to(self, spouse):
        spouse_name = self.get('spouse_name', '')
        return spouse_name is spouse.name

    @property
    def spouse(self):
        spouse = None
        if self.married:
            spouse_name = self.get('spouse_name', '')
            spouse = self.world_obj.get_person(spouse_name)
        return spouse

    def pass_away(self):
        self.set('married', False)
        self.set('deceased', self.world_obj.year)

    def chance_to_have_child(self, year=None, return_boolean=True):
        chance = 0.0
        if year:
            age = self.age_at_year(year)
        else:
            age = self.age

        if age > self.world_obj.age_of_consent:
            # Up to 20% chance based on age
            max_age = self.world_obj.age_of_consent + (40 if self.gender is 'Male' else 30)

            chance += 0.2 - math_helpers.percent_range(value=age, start_min=self.world_obj.age_of_consent,
                                                       start_max=max_age, end_min=0, end_max=0.2)

            # Up to 10% chance of having kids if lower educated
            chance += 0.1 - math_helpers.percent_range(self.education, 0, 100, 0, .1)

            # Reduce 10% chance if high conflict
            chance -= math_helpers.percent_range(self.conflict, 0, 100, 0, .1)

            #Up to 15% higher if wealthy
            chance += math_helpers.percent_range(self.economic, 0, 100, 0, .15)

            # 5% less chance per kid
            chance -= (self.num_kids * .05)

            chance += float(self.get('passion', 0)) * 0.01

            chance = math_helpers.clamp(chance, 0.01, 0.4)

        if return_boolean:
            chance = chance > numpy.random.random()

        return chance

    def have_child(self, child_data={}, spouse=None, event_id=0):
        father = self if self.gender is 'Male' else spouse
        mother = spouse if self.gender is 'Male' else self

        if not isinstance(father, Person):
            father = Person(self.world_obj, father, 'Male', 'Father')
            spouse = father
        if not isinstance(mother, Person):
            mother = Person(self.world_obj, mother, 'Female', 'Mother')
            spouse = mother

        child_dna, temp = dna_helpers.combine_dna(mother=mother.dna, father=father.dna)
        child_gender = dna_helpers.gender_from_dna(child_dna)
        child_dna = math_helpers.get_val(child_data, 'dna', child_dna)
        child_data_new = {
            "dna": child_dna,
            "gender": child_gender,
            "father_name": father.name,
            "mother_name": mother.name
        }
        child_data = math_helpers.extend(child_data, child_data_new)
        child = Person(self.world_obj, child_data, gender=child_gender, role='Child')
        child.create_name()

        world_data = self.world_obj.world_data
        birth_place = create_random_item(world_data=world_data, set_random_key=False, pattern='birthplace')
        birth_event_data = apply_event_effects(person_data=child.pointer, world_data=world_data, age=0,
                                               event_data=birth_place, event_type='birthplace', event_id=event_id,
                                               tag_manager=self.world_obj.tag_manager)

        child.set('birth_year', int(self.world_obj.get('year')))

        child.set('birth_event', birth_event_data)
        if spouse is None:
            child.set('parents_unmarried_while_born', True)
            child.set('family_name', mother.family_name)
            self.conflict += 2
            spouse.conflict += 2
            self.economic -= 2
            spouse.economic -= 2
        else:
            child.set('family_name', self.family_name if self.gender is 'Male' else mother.family_name)
            self.conflict -= 1
            self.economic -= 1
            spouse.economic -= 1
        self.education += 1

        child.create_name(set_to_person=True)
        self.world_obj.add_person(child)

        self.attribute_mod_update('Happiness', numpy.random.randint(-2, 2))
        self.attribute_mod_update('Constitution', numpy.random.randint(-2, 0))
        self.attribute_mod_update('Passion', numpy.random.randint(-4, -1))
        if self.gender is 'Female':
            self.attribute_mod_update('Happiness', -1)
            self.attribute_mod_update('Constitution', -1)
        return child

    @property
    def description(self):
        description = ""

        # TODO: Add height and other descriptions of physical appearance
        description += str(self.age) + " year old"
        description += " " + self.gender.title()
        if self.race is not 'Human':
            description += " " + self.race.title()
        description += " " + self.profession.title()

        return description

    def update_biorhythms(self, age=None):
        if age is None:
            age = self.age

        HUSBAND_IMPROVEMENTS = "Extraversion,Artistic,Happiness,Happiness,Happiness,Business,Meekness,Conscienciousness,Religiousness"
        HUSBAND_DEGRADATIONS = "Extraversion,Artistic,Happiness,Meekness,Conscienciousness"
        WIFE_IMPROVEMENTS    = "Extraversion,Artistic,Happiness,Happiness,Happiness,Business,Meekness,Conscienciousness,Religiousness"
        WIFE_DEGRADATIONS    = "Extraversion,Artistic,Happiness,Conscienciousness,Religiousness"
        HAPPY_FORMULA = "Happiness,Anger-,Terror-,Extraversion,Intelligence-,Meekness,Appearance,Realism-"
        PASSION_FORMULA = "Artistic,Extraversion,Constitution,Religiousness-,Constraint-,Realism-,Passion,Meekness-"
        CONSCIENCE_FORMULA = "Conscienciousness,Terror-,Intelligence,Manipulation-,Charisma"
        HEALTH_FORMULA = "Constitution,Strength,Dexterity,Anger-,Intelligence,Weight-,Lifespan,Neuroticism-,Immune System"

        happy = math_helpers.get_formula_from_obj(self.attribute_mods, HAPPY_FORMULA, -10, 20)
        passion = math_helpers.get_formula_from_obj(self.attribute_mods, PASSION_FORMULA, -10, 20)
        conscience = math_helpers.get_formula_from_obj(self.attribute_mods, CONSCIENCE_FORMULA, -10, 20)
        health = math_helpers.get_formula_from_obj(self.attribute_mods, HEALTH_FORMULA, -10, 20)

        if self.education is None or not isinstance(self.education, float):
            self.education = math_helpers.rand_range(1.0, 120.0, 3, 4.0)
        if self.economic is None or not isinstance(self.economic, float):
            self.economic = math_helpers.rand_range(1.0, 120.0, 3, 4.0)
        if self.conflict is None or not isinstance(self.conflict, float):
            self.conflict = math_helpers.rand_range(1.0, 120.0, 3, 4.0)

        # TODO: Revise by modified age
        if age > 60:
            self.attribute_mod_update('Constitution', -.4)
            self.attribute_mod_update('Appearance', -.2)
            conscience += 3
            passion -= 3
            health -= 1
        elif age > 40:
            self.attribute_mod_update('Constitution', -.3)
            self.attribute_mod_update('Appearance', -.1)
            self.attribute_mod_update('Wisdom', .3)
            conscience += 1
            passion -= 1
        elif age > 20:
            self.attribute_mod_update('Passion', .2)
            self.attribute_mod_update('Happiness', .2)
            self.attribute_mod_update('Constitution', .2)
            self.attribute_mod_update('Conscienciousness', .2)
            self.attribute_mod_update('Appearance', .1)
            conscience -= 1
            passion += 3
            happy += 2
            health += 4
        elif age > 17:
            self.attribute_mod_update('Appearance', .2)

        if self.education >= 40.0:
            conscience += 3
            happy -= 1
            passion += 1
        elif self.education >= 13:
            conscience += 1
            passion -= 1
            happy -= 1
            health -= 2
        elif self.education >= 5:
            conscience -= 1
            passion += 2
            happy += 1
            health -= 1
        else:
            health -= 1
            happy -= 1

        if self.economic >= 40.0:
            conscience -= 3
            happy += 3
            passion += 2
            health += 1
        elif self.economic >= 13:
            conscience -= 1
            passion += 1
            happy += 1
        elif self.economic >= 5:
            conscience += 1
            passion += 1
            happy -= 1
            health -= 1
        else:
            health -= 2
            happy -= 2
            passion += 2

        if self.conflict >= 40.0:
            conscience -= 3
            happy -= 2
            passion += 2
            health -= 2
        elif self.conflict >= 13:
            conscience -= 2
            passion += 1
            happy -= 2
            health -= 1
        elif self.conflict >= 5:
            conscience -= 1
            passion += 1
            happy -= 1
            health -= 1

        # rands = numpy.random.randint(-2, 2, 4)
        # happy = math_helpers.clamp(happy+rands[0], -10, 10)
        # passion = math_helpers.clamp(passion+rands[1], -10, 10)
        # conscience = math_helpers.clamp(conscience+rands[2], -10, 10)
        # health = math_helpers.clamp(health+rands[3], -10, 10)

        self.conscience = conscience
        self.passion = passion
        self.happy = happy
        self.health = health

        #Annual family modifiers
        economic_tithe = float(self.economic) * .03

        #Inflation and growth from working - #TODO: Make job dependent
        self.economic += math_helpers.weighted_number(mid=0.03, max=self.economic / 4, weight=8)

        #shift some money between parents
        if self.married and self.spouse:
            spouse = self.spouse

            #TODO: Should everyone have house?
            house = self.get("house", random_number=True, mid=0.02, max=self.economic)
            house = math_helpers.value_of_variable(house)

            if self.economic > spouse.economic:
                self.economic -= economic_tithe
                spouse.economic += economic_tithe

            #Increase parents stats through marriage
            improvements = HUSBAND_IMPROVEMENTS if self.gender is "Male" else WIFE_IMPROVEMENTS
            degradations = HUSBAND_DEGRADATIONS if self.gender is "Male" else WIFE_DEGRADATIONS
            for improvement in numpy.random.choice(improvements.split(","), 2):
                self.attribute_mod_update(improvement, 1)
            for degradation in numpy.random.choice(degradations.split(","), 1):
                self.attribute_mod_update(degradation, -1)

            house += economic_tithe
            self.set("house", house)
            self.economic -= economic_tithe

        if self.economic < 2:
            self.attribute_mod_update("Happiness", -1)

        if not self.deceased and self.health < -9:
            self.pass_away()


    @property
    def output_short(self):
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "role": self.role
        }

    @property
    def output(self):
        person_data = {
            "name": self.name,
            "year": self.world_obj.year,
            "age": self.age,
            "birth_year": self.birth_year,
            "race": self.race,
            "rank": self.rank,
            "nationality": self.nationality,
            "family_name": self.family_name,
            "gender": self.gender,
            "profession": self.profession,
            "role": self.role,
            # "qualities": self.quality_mods,
            # "attributes": self.attribute_mods,
            # "aspects": self.aspects,
            # "skills": self.skills,
            # "items": self.items,
            "economic": self.economic,
            "education": self.education,
            "conflict":  self.conflict,
            "conscience": self.conscience,
            "happy": self.happy,
            "passion": self.passion,
            "health": self.health,
            "status": "deceased" if self.deceased else "alive",
            "num_kids": self.num_kids,
            # "dna": self.dna,
            "description": self.description
        }

        spouse = self.spouse
        if isinstance(spouse, Person):
            person_data["spouse_name"] = spouse.name
        father_name = self.get('father_name', None)
        if father_name:
            person_data["father_name"] = father_name
        mother_name = self.get('mother_name', None)
        if mother_name:
            person_data["mother_name"] = mother_name

        return person_data

    def __repr__(self):
        return "<Person Class: " + json.dumps(self.output) + " >"

    def __str__(self):
        return json.dumps(self.output)

    def __dict__(self):
        return self.output