from procyon.starsystemmaker.math_helpers import *
import numpy as np

QUALITY_ARRAY = [
    {"name": "Skin Pigment",
     "values": "Translucent:Cha--:Health---,Albino:Cha-,Alabaster,Pale White,Light,White,Fair,Medium,Tanned:Cha+,Light Brown,Olive,Moderate Brown,Brown,Brown,Dark Brown,Very Dark Brown,Black,Midnight"},
    {"name": "Skin Toughness",
     "values": "Scaley:Armor++:Cha--,Leathery:Armor+:Cha-,Thick:Cha-:Con+,Normal,Normal,Creamy,Silky:Cha+,Velvet:Cha+,Marble:Cha++:Armor+",
     "maternal": True},
    {"name": "Bone Length",
     "values": "Tiny:Health-:Height---,Stunted:Height--,Small:Height-,Normal,Normal,Normal,Normal,Normal,Large:Height+,Big:Height++,Long:Height+++"},
    {"name": "Eye Color",
     "values": "Hazel:Cha+,Amber,Green,Blue,Gray,Brown,Brown,Dark Brown,Black,Black,Black,Red:Cha-,Violet:Cha+"},
    {"name": "Eye Shape",
     "values": "Almond,Round,Upturned,Downturned,Monolid,Hooded"},
    {"name": "Eye Sight",
     "values": "Cross Eyed,Lazy Eye,Near Sighted,Far Sighted,Color Blind,Normal,Normal,Normal,Normal,Normal,Perfect Sight,Eagle Eyes"},
    {"name": "Hair Texture",
     "values": "Wavy,Curly,Straight,Smooth,Coily,Frizy"},
    {"name": "Head Size",
     "values": "Small,Oblong,Round,Oval,Square,Heart-shaped,Triangular,Diamond,Large,Giant Forehead,Bulbous"},
    {"name": "Finger Length",
     "values": "Stubby,Short,Normal,Long,Talons"},
    {"name": "Hairiness",
     "values": "Bald,Thin Hair,Thick Hair,Hairy,Fuzzy,Covered in Hair,Fury"},
    {"name": "Posture",
     "values": "Sway Back,Forward Head,Scoliosis,Flat Backed,Good Posture,Good Posture,Good Posture,Humpbacked"},
    {"name": "Nerve Response",
     "values": ""},
    {"name": "Skin Texture",
     "values": ""},
    {"name": "Teeth Shape",
     "values": ""},
    {"name": "Lung Capacity",
     "values": ""},
    {"name": "Heart Size",
     "values": ""},
    {"name": "Cell Longevity",
     "values": ""},
    {"name": "Gestation Rate",
     "values": "",
     "maternal": True}
]


def init_quality_arrays():
    for quality in QUALITY_ARRAY:
        values = quality.get("values", "Normal")
        values = values.split(",")
        quality["values"] = expand_array_to_16(values)


ASPECT_ARRAY = [
    {"name": "Giant", "requirements": "Height>16"},
    {"name": "Little Person", "requirements": "Height<6"},
    {"name": "Striking Looks", "requirements": "Cha>15"}
]

DNA_16_lOOKUPS = 'AA,AC,AG,AT,CA,CC,CG,CT,GA,GC,GG,GT,TA,TC,TG,TT'.split(',')  # Later, can switch this for obfuscation

# ----------------------
init_quality_arrays()
#----------------------


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


def qualities_from_dna(dna):
    if isinstance(dna, basestring):
        dna_arr = dna_array_from_string(dna)
    else:
        dna_arr = dna

    qualities = []
    attribute_mods = {}
    for idx, q in enumerate(dna_arr):
        quality = QUALITY_ARRAY[idx]
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

    #TODO: Derive Rand Seed
    return qualities, attribute_mods


def generate_dna(rand_seed='', race='human', overrides={}):
    try:
        rand_seed = float(rand_seed)
    except ValueError:
        rand_seed = np.random.random()
    rand_seed = set_rand_seed(rand_seed)

    dna_values = []
    for quality in QUALITY_ARRAY:
        gene_num = np.random.randint(1, 16) - 1  #Should this be randint(1,8)+randint(0,8) ?

        name = quality.get("name", "Quality")

        if name in overrides:
            override_value = overrides[name]
            if isinstance(override_value, basestring):
                # Search through value strings

                quality_values = quality.get("values", None)
                if quality_values:
                    for idx, quality_value in enumerate(quality_values):
                        value_data = override_value.split(":")
                        val_name = value_data[0]
                        if val_name.lower() == override_value.lower():  #TODO: Finds first, not middle
                            gene_num = idx
                            break
            else:
                #Int provided
                override_value = clamp(override_value, 0, 15)
                gene_num = override_value

        dna_values.append(gene_num)

    dna = dna_string_from_array(dna_values)

    return dna, rand_seed
