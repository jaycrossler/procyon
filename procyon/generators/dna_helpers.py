from procyon.starsystemmaker.math_helpers import *
import numpy as np

# TODO: Move this to a model, allow extra DNA junk space that can be filled in by anthology-specific values. Or have some hash-mapper to add more
GENE_ARRAY = [
    {"name": "Sex",
     "values": "Male,Female"},
    {"name": "Skin Pigment",
     "values": "Translucent:Charisma--:Constitution---,Albino:Charisma-,Alabaster,Pale White,Light,White,Fair,Medium,Tanned:Charisma+,Light Brown,Olive,Moderate Brown,Brown,Brown,Dark Brown,Very Dark Brown,Black,Midnight"},
    {"name": "Skin Toughness",
     "values": "Scaley:Armor++:Charisma--,Leathery:Armor+:Appearance-,Thick:Charisma-:Constitution+,Normal,Normal,Creamy,Silky:Charisma+,Velvet:Charisma+,Marble:Charisma++:Armor+",
     "maternal": True},
    {"name": "Bone Length",
     "values": "Tiny:Constitution-:Height---:Speed+:Dexterity++,Stunted:Height--:Dexterity+,Small:Height-,Normal,Normal,Normal,Normal,Normal,Large:Height+,Big:Height++:Speed-,Very Long:Height+++:Speed-:Dexterity-:Armor-"},
    {"name": "Eye Color",
     "values": "Hazel:Appearance+,Amber,Green,Blue,Gray,Brown,Brown,Dark Brown,Black,Black,Black,Red:Charisma-:Manipulation+,Violet:Charisma+:Manipulation+"},
    {"name": "Eye Shape",
     "values": "Almond,Round,Upturned,Downturned,Monolid:Appearance-,Hooded"},
    {"name": "Eye Sight",
     "values": "Cross Eyed:Charisma-,Lazy Eye,Near Sighted,Far Sighted,Color Blind,Normal,Normal,Normal,Normal,Normal,Perfect Sight:Perception+,Eagle Eyes:Perception++:Terror+"},
    {"name": "Eye Spectrum",
     "values": "Infrared:Infravision+,Normal,Normal,Normal,Normal,Normal,Normal,Normal,Normal,Vibrant Colors:Perception+,Ultraviolet:Perception+"},
    {"name": "Hair Texture",
     "values": "Wavy,Curly,Straight,Smooth:Appearance+,Coily,Frizy"},
    {"name": "Head Size",
     "values": "Small:Manipulation-,Oblong,Round,Oval,Square,Heart-shaped,Triangular,Diamond,Large,Giant Forehead:Manipulation+,Bulbous:Intelligence+"},
    {"name": "Finger Length",
     "values": "Stubby:Dexterity-:Swimming-,Short,Normal,Normal,Normal,Long:Dexterity+,Talons:Dexterity-:Unarmed Attack+"},
    {"name": "Hand Shape",
     "values": "Heavily Webbed:Dexterity--:Swimming++,Webbed:Dexterity-:Swimming+,Normal,Normal,Normal,Strong Joints:Strength+,Fist of Stone:Dexterity-:Unarmed Attack+:Strength+:Swimming-"},
    {"name": "Male Hairiness",
     "values": "Bald:Swimming+,Thin Hair,Thick Hair,Hairy,Fuzzy,Bearded:Appearance-,Covered in Hair:Warm+,Fury:Charisma+:Appearance-:Warm+:Terror+:Swimming-"},
    {"name": "Female Hairiness",
     "values": "Bald:Appearance-:Swimming+,Thin Hair,Thick Hair,Thick Hair,Thick Hair,Thick Hair,Thick Hair,Hairy,Fuzzy,Bearded:Appearance-,Covered in Hair:Warm+:Charisma-,Fury:Appearance--:Charisma+:Warm+:Terror+:Swimming-"},
    {"name": "Posture",
     "values": "Forward Head:Charisma-:Manipulation+,Scoliosis,Flat Backed,Good Posture,Good Posture,Good Posture,Humpbacked:Charisma-,Sway Back:Charisma-"},
    {"name": "Toe length",
     "values": "Sensitive Toenails::Speed-,Big Toe longest,Second toe longest,Stubby Toes:Dexterity-"},
    {"name": "Feet shapes",
     "values": "Flat footed:Speed-:Swimming+,Normal,Normal,High arch,Runner Feet:Speed+:Swimming-"},
    {"name": "Leg Shape",
     "values": "Bow legged:Dexterity-,Straight Legs,Straight Legs,Knees knocked in,Floating kneecap,Massive Thighs:Constitution+:Swimming--"},
    {"name": "Torso Shape",
     "values": "Long:Constitution++:Height+:Appearance-,Barrel Chested:Constitution+:Strength+,Apple shaped,Pear shaped,Thin,Short,Extremely Thin:Constitution-:Strength-"},
    {"name": "Neck Size",
     "values": "Thick:Strength+:Appearance-,Thin,Normal,Normal,Long:Strength-:Constitution+,Short:Appearance-"},
    {"name": "Nose Shape",
     "values": "Empty Cavity:Terror+:Appearance-:Swimming-,Flat,Wide,Thin,Turned up/perky:Appearance+,Hooked down,Bulbous:Appearance-:Terror-,Giant Nostrils:Appearance-:Constitution+"},

    {"name": "Nerve Response",
     "values": "Very Fast Reflexes:Dexterity++:Lifespan-,Fast Reflexes:Dexterity+,Normal,Normal,Normal,Normal,Normal,Normal,Normal,Slow Reflexes:Dexterity-:Constitution+"},
    {"name": "Skin Texture",
     "values": "Bad Acne:Appearance--,Acne:Appearance-,Birth Mark:Appearance-,Smooth,Normal,Normal,Normal,Soft,Rough,Barky:Charisma-:Lifespan+,Textured with Runes:Magic Power+:Magic Resistant+:Charisma-:Terror+"},
    {"name": "Teeth Shape",
     "values": "Sharp and Pointed:Manipulation++,Large with Two Rows:Manipulation+:Terror+,Large Canines:Manipulation+,Normal,Normal,Normal,Well Spaced Teeth,Perfect Teeth:Appearance+"},
    {"name": "Lung Capacity",
     "values": "Huge:Dexterity+:Constitution+:Strength+:Lifespan-:Swimming+,Large:Constitution++:Strength+:Swimming+,Normal,Normal,Stilted:Constitution-,Small:Constitution-,Withered:Constitution-:Strength--:Lifespan-:Swimming++"},
    {"name": "Heart Size",
     "values": "Thin and Fast:Dexterity++:Lifespan-,Small:Lifespan-:Dexterity-,Strong:Lifespan+:Happiness+:Immune System+,Normal,Normal,Big:Lifespan+:Immune System+:Constitution+,Large:Lifespan-:Strength+,Very Large:Constitution++:Strength+:Lifespan--:Constitution-"},
    {"name": "Cell Longevity",
     "values": "Quick Burner:Lifespan---:Constitution+:Strength+:Dexterity+:Immune System+:Regeneration+,Half-lived:Regeneration+:Lifespan--:Constitution+:Immune System+,Multiplicator:Lifespan-:Strength+,Normal,Normal,Normal,Normal,Normal,Normal,Slow Replicator:Lifespan+:Radiation Resistant-,Frozen:Lifespan++:Constitution-:Regeneration-,Methuselah:Lifespan+++:Constitution-:Strength-:Immune System-:Regeneration-"},
    {"name": "Gestation Rate",
     "values": "6 Months:Wisdom-:Lifespan-:Constitution-,9 Months,9.5 Months,9.5 Months,9.5 Months,9.5 Months:Constitution+,10 Months,11 Months,12 Months:Lifespan+,14 Months:Lifespan+,16 Months:Lifespan++,20 Months:Lifespan+++,24 Months:Lifespan++++:Wisdom+",
     "maternal": True},
    {"name": "Multiple Children",
     "values": "Single,Single,Single,Single,Single,Single,Single,Single,Single,Single,Single,Single,Single,Twins:Twins+,Twins:Twins++,Multiple:Regeneration+:Twins+++"},
    {"name": "Dwarfism",
     "values": "Normal,Normal,Normal,Normal,Normal,Normal,Normal,Normal,Normal,Normal,Normal,Normal,Normal,Normal,Shorter:Height-:Twins-,Dwarfed Height:Height---:Twins--"},

    {"name": "Blood Type",
     "values": "C:Regeneration+,A,A,A,A,A,A,B,B,AB,AB,O,O,O,O,O:Regeneration+"},

    {"name": "Blood Rh Factor",
     "values": "Exotic::Regeneration+:Lifespan+:Warm-,Plus,Plus,Plus,Plus,Plus,Plus,Plus,Plus,Plus,Plus,Plus,Plus,Negative,Negative,Negative:Constitution+"},

    {"name": "Stomach Composition",
     "values": "Broken Belly:Immune System--:Hunger-:Weight-:Lifespan-,Weak Abdomen:Strength-:Immune System-,Hernias:Lifespan-:Strength-,Gastric Acid:Immune System+:Weight-:Happiness-,Normal,Normal,Normal,Normal,Lead Belly:Radiation Resistant+:Immune System+:Hunger+,Ravishing Appetite:Hunger++:Constitution+:Immune System++:Weight+"},

    {"name": "Skull Thickness",
     "values": "Thin Bones:Constitution--:Lifespan-:Weight:-,Soft Spot:Constitution-,Normal,Normal,Normal,Normal,Thick Skull:Constitution+,Solid Skull:Constitution++,Intelligence-"},

    {"name": "Arterial Size",
     "values": "Cold Blooded:Constitution-:Lifespan+++:Terror+:Warm++,Collapsed:Lifespan--:Warm-,Constricted:Constitution-,Thin:Immune System+:Constitution-,Normal,Normal,Normal,Thick:Immune System-:Constitution+:Warm+,Dilated:Constitution+:Warm++:Armor-"},

    {"name": "Realistic Thinking",
     "values": "Objective Worldview:Wisdom+:Intelligence++:Realism+:Charisma-:Artistic-:Magic Resistant+:Magic Power-,Realist:Realism+:Intelligence+,Objectivist:Constraint+:Extraversion-,Normal,Normal,Fantasist:Artistic+:Realism-,Day Dreamer:Artistic+:Neuroticism-:Happiness+,Dreamer:Conscienciousness-:Realism-:Magic Resistant-:Wisdom-",
     "mental": True},

    {"name": "Investigative Thinking",
     "values": "Detailed Worldview:Intelligence++:Neuroticism+:Realism+:Charisma-:Awareness+:Manipulation+,Detective:Realism+:Intelligence+:Awareness+,Structured Thinker:Constraint+:Dexterity-:Extraversion-,Normal,Normal,Normal,Dull:Dexterity-:Realism-,Imaginator:Artistic+:Neuroticism-:Happiness+:Extraversion+,Creator:Realism-:Constraint-:Anger-:Openness+",
     "mental": True},

    {"name": "Artistic Expression",
     "values": "Tabula Rosa:Artistic-:Neuroticism-:Openness+:Wisdom-:Terror-:Religiousness+,Inspired:Artistic+:Openness+:Religiousness+,Creator:Artistic++:Realism-:Happiness+:Neuroticism+,Normal,Normal:Wisdom+,Boring:Artistic-:Intelligence-:Conscienciousness+,Energetic:Artistic-:Anger-:Constitution+,Fanatic:Realism+:Conscienciousness-,Openness-,Terror+:Wisdom-",
     "mental": True},

    {"name": "Social Awareness",
     "values": "Closed:Conscienciousness--:Anger-:Openness-,Alone:Conscienciousness-:Openness-:Extraversion-,Aloof:Extraversion-,Embedded:Extraversion-,Reflexive:Religiousness+,Normal:Religiousness+,Normal,Self Aware,Engaged:Extraversion+,Self Accepted,Collaborative:Extraversion++:Conscienciousness+,Resonant:Conscienciousness++:Anger-:Openness++:Wisdom+",
     "social": True},

    {"name": "Enterprising Thought",
     "values": "Entrepreneur:Business++:Terror+:Openness+:Manipulation+:Conscienciousness-:Wisdom-,Business Leader:Business+:Manipulation+:Conscienciousness-:Awareness+,Manager:Business+:Extraversion+,Normal:Business-,Normal,Normal,Normal:Business-,Normal:Business-,Calculator:Openness-:Business+,Interconnected Thinker:Business++:Artistic+:Realism+:Neuorticism++:Wisdom+",
     "mental": True},

    {"name": "Conventionality",
     "values": "",
     "social": True},

    {"name": "Conservatism",
     "values": "",
     "social": True},

    {"name": "Authoritarianism",
     "values": "",
     "social": True},

    {"name": "Religiousness",
     "values": "",
     "mental": True},

    {"name": "Extraversion",
     "values": "",
     "social": True},

    {"name": "Agreeableness",
     "values": "",
     "social": True},

    {"name": "Conscienciousness",
     "values": "",
     "social": True},

    {"name": "Neuroticism",
     "values": "",
     "mental": True},

    {"name": "Openness",
     "values": "",
     "social": True},

    {"name": "Constraint",
     "values": "",
     "mental": True},

    {"name": "Positive Emotionality",
     "values": "Normal,Normal,Happy:Happiness+,Excited:Happiness+:Conscienciousness+:Meekness+:Wisdom+,Loving:Happiness++:Meekness++:Conscienciousness+:Wisdom+,Big Hearted:Happiness++:Conscienciousness+:Meekness+++:Wisdom+",
     "social": True},

    {"name": "Negative Emotionality",
     "values": "Depressive,Angry:Terror+,Sad,Tired,Grumpy,Normal,Normal,Normal,Normal:Wisdom+,Peaceful:Manipulation-:Wisdom+",
     "social": True},

    {"name": "Chi",
     "values": "Empty:Magic Resistant+++,Null:Magic Resistant++,Blank:Magic Resistant+,Normal,Normal,Normal,Normal,Normal,Normal,In Tune:Magic Resistant-:Magic Power+,Powerful:Magic Power++:Magic Resistant--",
     "maternal": True},

    {"name": "Gnosis",
     "values": "Rooted:Magic Resistant++,Normal,Normal,Normal,Normal,Normal,Normal,Powerful:Magic Resistant+:Magic Power+,Alar:Magic Resistant++:Magic Power++,Awakened:Magic Resistant+:Magic Power+++",
     "paternal": True}

]

RACE_ARRAY = [
    {"name": "Human",
     "values": "Bone Length:Normal,Gestation Rate:10 Months,Skin Toughness:Normal,Eye Spectrum:Normal,Teeth Shape:Normal,Gnosis:Normal,Cell Longevity:Normal"},

    {"name": "Elf",
     "values": "Positive Emotionality:Happy,Bone Length:Big,Gestation Rate:24 Months,Nerve Response:Fast Reflexes,Eye Shape:Hooded,Eye Spectrum:Infrared,Chi:In Tune,Lung Capacity:Stilted,Cell Longevity:Slow-Replicator"},

    {"name": "Dwarf",
     "values": "Negative Emotionality:Grumpy,Neck Size:Thick,Bone Length:Stunted,Skin Toughness:Thick,Hairiness:Bearded,Female Hairiness:Bearded,Torso Shape:Barrel Chested,Heart Size:Large,Chi:Blank,Cell Longevity:Methuselah,Dwarfism:Dwarfed Height"},

    {"name": "Ork",
     "values": "Negative Emotionality:Angry,Skin Toughness:Leathery,Gestation Rate:6 Months,Neck Size:Thick,Torso Shape:Long,Stomach Composition:Ravishing Appetite,Teeth Shape:Large Canines,Multiple Children:Twins,Hand Shape:Strong Joints,Cell Longevity:Half-lived"},

    {"name": "Halfling",
     "values": "Dwarfism:Dwarfed Height"},

    {"name": "Dragonborn",
     "values": "Skin Toughness:Scaley,Gestation Rate:12 Months,Eye Color:Red,Neck Size:Thick,Head Size:Diamond,Torso Shape:Barrel Chested,Stomach Composition:Ravishing Appetite,Teeth Shape:Large Canines,Eye Spectrum:Infrared,Hand Shape:Webbed,Nose Shape:Empty Cavity,Posture:Forward Head,Male Hairiness:Bald,Finger Length:Talons,Cell Longevity:Quick Burner"},

    {"name": "Gnome",
     "values": "Dwarfism:Dwarfed Height"},

    {"name": "Tiefling",
     "values": ""},
]

ASPECT_ARRAY = [
    {"name": "Giant", "requirements": "Height>16"},
    {"name": "Little Person", "requirements": "Height<6"},
    {"name": "Striking Looks", "requirements": "Cha>15"},
    {"name": "See in the Dark", "requirements": "Eye Spectrum=Infrared,Eye Spectrum = Ultraviolet"},
]

DNA_16_lOOKUPS = 'AA,AC,AG,AT,CA,CC,CG,CT,GA,GC,GG,GT,TA,TC,TG,TT'.split(',')  # Later, can switch this for obfuscation


def init_quality_arrays():
    for quality in GENE_ARRAY:
        values = quality.get("values", "Normal")
        values = values.split(",")
        quality["values"] = expand_array_to_16(values)

    for quality in RACE_ARRAY:
        values = quality.get("values", "Normal")
        quality["values"] = values.split(",")

    for quality in ASPECT_ARRAY:
        values = quality.get("requirements", "None")
        quality["requirements"] = values.split(",")


# ----------------------
init_quality_arrays()
# ----------------------


def dna_string_from_array(dna_values):
    str_values = []
    for v in dna_values:
        str_values.append(DNA_16_lOOKUPS[v])
    return "".join(str_values)


def dna_array_from_string(dna):
    dna_values = []
    len_dna = len(dna)

    for i in range(len_dna / 2):
        try:
            start = i * 2
            end = i * 2 + 2
            snippet = dna[start:end]
            val = DNA_16_lOOKUPS.index(snippet) + 1
        except ValueError:
            val = 0
        dna_values.append(val)
    return dna_values


def aspects_from_dna(dna):
    if isinstance(dna, basestring):
        dna_arr = dna_array_from_string(dna)
    else:
        dna_arr = dna

    aspects = []
    qualities = qualities_from_dna(dna)  # TODO: Cache this?

    # TODO: Build this out
    return aspects


def qualities_from_dna(dna):
    if isinstance(dna, basestring):
        dna_arr = dna_array_from_string(dna)
    else:
        dna_arr = dna

    qualities = []
    attribute_mods = {}
    for idx, q in enumerate(dna_arr):
        quality = GENE_ARRAY[idx]
        name = quality.get("name", "Quality")
        values = quality.get("values", None)
        if values:
            val = values[q - 1]
            value_data = val.split(":")
            val = value_data[0]

            qualities.append({"name": name, "value": val})

            modifiers = value_data[1:]
            for mod in modifiers:
                mod_num = mod.count('+') - mod.count('-')
                mod_name = mod.replace('+', '').replace('-', '')
                if mod_name:
                    if mod_name in attribute_mods:
                        attribute_mods[mod_name] += mod_num
                    else:
                        attribute_mods[mod_name] = mod_num

    # TODO: Derive Rand Seed

    #Ensure frequently used variables are set:
    #TODO: Loop through all possible mods
    for var in "Conscienciousness,Wisdom,Happiness,Passion,Appearance,Realism,Anger,Strength,Constitution,Intelligence,Extraversion,Artistic,Business,Meekness,Religiousness".split(
            ","):
        attribute_mods[var] = attribute_mods.get(var, 0)

    return qualities, attribute_mods


def generate_dna(rand_seed='', race='Human', overrides={}):
    try:
        rand_seed = float(rand_seed)
    except ValueError:
        rand_seed = np.random.random()
    rand_seed = set_rand_seed(rand_seed)

    race_overrides = overrides_from_race(race=race, overrides=overrides)

    dna_values = []
    for quality in GENE_ARRAY:
        gene_num = np.random.randint(0, 15)  # Should this be randint(1,8)+randint(0,8) ?

        name = quality.get("name", "Quality")

        if name in race_overrides or name.lower() in race_overrides:
            override_value = race_overrides[name]
            if isinstance(override_value, basestring):
                # Search through value strings

                quality_values = quality.get("values", None)
                if quality_values:
                    value_indexes = []
                    for idx, quality_value in enumerate(quality_values):
                        value_data = quality_value.split(":")
                        val_name = value_data[0]
                        if val_name.lower() == override_value.lower():
                            value_indexes.append(idx)
                    if value_indexes:
                        gene_num = np.random.choice(value_indexes)

            else:
                # Int provided
                override_value = clamp(override_value, 0, 15)
                gene_num = override_value

        dna_values.append(gene_num)

    dna = dna_string_from_array(dna_values)

    return dna, rand_seed


def metrics_of_attributes():
    used = {}
    average = {}
    highest = {}
    lowest = {}

    for qual in GENE_ARRAY:
        values = qual.get("values", [])

        lowests = {}
        highests = {}
        for value_data in values:
            value_data = value_data.split(":")
            if len(value_data) > 1:
                modifiers = value_data[1:]
                for mod in modifiers:

                    mod_num = mod.count('+') - mod.count('-')
                    mod_name = mod.replace('+', '').replace('-', '')
                    if mod_name:
                        if mod_name in used:
                            used[mod_name] += 1
                        else:
                            used[mod_name] = 1

                        if mod_name in average:
                            average[mod_name] += mod_num
                        else:
                            average[mod_name] = mod_num

                        if mod_num < 0:
                            if mod_name in lowests:
                                low = lowests[mod_name]
                                if low > mod_num:
                                    lowests[mod_name] = mod_num
                            else:
                                lowests[mod_name] = mod_num

                        if mod_num > 0:
                            if mod_name in highests:
                                high = highests[mod_name]
                                if high < mod_num:
                                    highests[mod_name] = mod_num
                            else:
                                highests[mod_name] = mod_num
        for key in lowests:
            val = lowests[key]
            if key in lowest:
                lowest[key] += val
            else:
                lowest[key] = val
        for key in highests:
            val = highests[key]
            if key in highest:
                highest[key] += val
            else:
                highest[key] = val

    totals = []
    for key, val in used.iteritems():
        data = (key + ":").ljust(30) + ("Used: " + str(val)).ljust(10)
        data += ("Avg: " + str(average.get(key, 0))).ljust(10)
        range_data = (str(lowest.get(key, 0))).rjust(3) + " - " + str(highest.get(key, 0))
        data += ("Range: " + range_data)
        totals.append(data)

    return totals


def get_quality_values_array_named(quality, array=GENE_ARRAY):
    values = []
    for val in array:
        name = val.get("name", "name")
        value_list = val.get("values", [])
        if name.lower() == quality.lower():
            values = value_list
            break
    return values


def does_quality_value_exist(quality, value):
    exists = False
    values_arr = get_quality_values_array_named(quality)
    for val in values_arr:
        val_arr = val.split(":")
        val_name = val_arr[0]
        if val_name.lower() == value.lower():
            exists = True
            break
    return exists


def overrides_from_race(race='Human', overrides={}):
    new_overrides = overrides.copy()
    race_values = get_quality_values_array_named(race, array=RACE_ARRAY)

    if race_values:
        for idx, race_val in enumerate(race_values):
            race_val_arr = race_val.split(":")
            if len(race_val_arr) > 1:
                race_val_name = race_val_arr[0]
                race_att_name = race_val_arr[1]

                if does_quality_value_exist(race_val_name, race_att_name):
                    new_overrides[race_val_name] = race_att_name

    return new_overrides


def gene_single_merge(m, f, is_maternal, is_paternal):
    if is_maternal:
        return m
    if is_paternal:
        return f

    out = ""
    roll = np.random.randint(0, 3)
    if roll == 0:
        out = m[0] + f[0]
    if roll == 1:
        out = m[0] + f[1]
    if roll == 2:
        out = m[1] + f[0]
    if roll == 3:
        out = m[1] + f[1]

    return out


def race_from_dna(dna):
    race_variations = {}

    for race in RACE_ARRAY:
        race_name = race.get("name", "race")
        race_val_count = len(race.get("values", []))
        if race_val_count > 3:
            race_variations[race_name] = 0

    if len(dna) < len(GENE_ARRAY) * 2 + 2:
        return 'Human'

    for gene_index, val in enumerate(GENE_ARRAY):
        gene_name = val.get("name", "name").lower()
        gene_values = val.get("values", [])
        start = gene_index * 2
        end = gene_index * 2 + 2
        snippet = dna[start:end]
        if not snippet:
            continue
        snippet = snippet.upper()
        current_gene_val = DNA_16_lOOKUPS.index(snippet)

        for race in RACE_ARRAY:
            race_values = race.get("values", [])
            if len(race_values) > 3:
                race_offest = 0
                race_name = race.get("name", "race")
                for race_val in race_values:
                    race_val_arr = race_val.split(":")
                    if len(race_val_arr) > 1:
                        race_value_name = race_val_arr[0].lower()

                        if race_value_name == gene_name:
                            race_attribute_name = race_val_arr[1].lower()

                            # Get the gene ids that match and DNA value for this gene, and find distance to target
                            shortest_dist = 15
                            shorter_dist_found = False
                            for idx_gene_vals, gene_val in enumerate(gene_values):
                                compared_gene_val_name = gene_val.split(":")[0].lower()
                                if compared_gene_val_name == race_attribute_name:
                                    abs_distance = abs(idx_gene_vals - current_gene_val)
                                    if abs_distance < shortest_dist:
                                        shortest_dist = abs_distance
                                        shorter_dist_found = True
                            if shorter_dist_found:
                                race_offest += shortest_dist

                if race_offest:
                    increase = float(race_offest) / float(len(race_values))
                    race_variations[race_name] += increase

    race_rank = []
    for w in sorted(race_variations, key=race_variations.get):
        race_rank.append(w)
    closest_race = race_rank[0]
    closest_race_second = race_rank[1]
    closest_race_third = race_rank[2]

    if closest_race == 'Human' and not closest_race_second == 'Human':
        amt_human = race_variations.get(closest_race)
        amt_second = race_variations.get(closest_race_second)
        amt_third = race_variations.get(closest_race_third)
        if amt_second - amt_human < 2.5 and amt_third - amt_second > 1.1:
            closest_race = "Half-" + closest_race_second

    if closest_race_second == 'Human' and not closest_race == 'Human':
        amt_second = race_variations.get(closest_race)
        amt_human = race_variations.get(closest_race_second)
        amt_third = race_variations.get(closest_race_third)

        if amt_human - amt_second < 2.5 and amt_third - amt_second > 1.1:
            closest_race = "Half-" + closest_race

    return closest_race


def gender_from_dna(dna):
    snippet = dna[0:2]
    gender_gene = GENE_ARRAY[0].get('values')
    snippet = snippet.upper()
    val = DNA_16_lOOKUPS.index(snippet)
    gender = gender_gene[val].title()
    return gender


def set_dna_gender(dna, gender=''):
    if gender:
        gender_gene = GENE_ARRAY[0].get('values')
        gender_vals = []
        for idx, gene_val in enumerate(gender_gene):
            if gene_val.lower() == gender.lower():
                gender_vals.append(idx)
        new_dna_num = np.random.choice(gender_vals)
        snippet = DNA_16_lOOKUPS[new_dna_num]
    else:
        snippet = DNA_16_lOOKUPS[np.random.randint(0, 15)]
    dna = snippet + dna[2:]

    return dna


def combine_dna(mother="", father="", rand_seed=''):
    len_genes = len(GENE_ARRAY) * 2
    if len(father) < len_genes:
        father = generate_dna()[0]
    if len(mother) < len_genes:
        mother = generate_dna()[0]

    try:
        rand_seed = float(rand_seed)
    except ValueError:
        rand_seed = np.random.random()
    rand_seed = set_rand_seed(rand_seed)

    new_dna = ""

    for idx, gene in enumerate(GENE_ARRAY):
        first = idx * 2
        last = first + 2
        snippet_m = mother[first:last]
        snippet_f = father[first:last]
        snippet = gene_single_merge(snippet_m, snippet_f, gene.get('maternal', False), gene.get('paternal', False))
        new_dna += snippet

    new_dna = set_dna_gender(new_dna, gender='')

    return new_dna, rand_seed


def mutate_dna(dna="", mutation_factor=0.003):
    out = ""

    len_alleles = len(dna) / 2
    rolls = np.random.random_sample(len_alleles)

    for i in range(len_alleles):
        roll = rolls[i]
        first = dna[i * 2]
        second = dna[i * 2 + 1]

        quarter = mutation_factor / 4.0

        if roll >= 1 - quarter:
            out += second + first
        elif roll >= 1 - (2 * quarter):
            out += first + first
        elif roll >= 1 - (3 * quarter):
            out += second + second
        elif roll >= 1 - (4 * quarter):
            out += DNA_16_lOOKUPS[np.random.randint(16) - 1]
        else:
            out += first + second

    return out