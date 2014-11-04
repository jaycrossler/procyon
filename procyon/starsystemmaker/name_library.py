from procyon.starsystemmaker.math_helpers import *
import random
import os
import numpy as np
import fuzzy
from string import maketrans


def list_of_names(name_file='', num_requested=20, use_prefix=True, prefix='New', prefix2='Old'):
    name_file_dir = 'procyon/fixtures/names/'
    if not name_file:
        name_file_list = os.listdir(name_file_dir)
        name_num = np.random.randint(len(name_file_list))
        name_file = name_file_list[name_num]
    if not name_file.endswith('txt'):
        name_file += '.txt'
    name_file = name_file.strip()

    with open(name_file_dir + name_file, mode='r') as infile:
        name_list = [line.strip() for line in infile]

    np.random.shuffle(name_list)

    if use_prefix and prefix:
        for i in range(len(name_list)):
            if not name_list[i].startswith(prefix):
                if np.random.random() < 0.02:
                    name_list[i] = prefix + " " + name_list[i]
                elif np.random.random() < 0.02:
                    name_list[i] = prefix2 + " " + name_list[i]

    return name_list


def name_part_fuzzer(name_parts, modifications=4):
    if isinstance(name_parts,basestring):
        name_parts = name_parts.split(" ")
    if modifications:
        part_count = len(name_parts)
        function_names = ["name_nysiis", "name_vowel_switch", "name_chars_replace"]
        for i in range(0, int(modifications)):
            idx_part = np.random.randint(part_count)
            name_part = name_parts[idx_part]

            func = np.random.choice(function_names, 1)[0]
            method_to_call = globals()[func]
            result = method_to_call(name_part)

            # result = locals()[func](name_part)
            name_parts[idx_part] = result

    return name_parts


def name_nysiis(word):
    if word:
        word = fuzzy.nysiis(word)
    return word


def name_vowel_switch(word):
    if word:
        intab = "aeiouyAEIOUY"
        outtab = np.random.choice(["aaiuuyAAIUUY", "eeeuuyEEEUUY", "ieiouyIEIOUY",
                                   "aeaooyAEAOOY", "aeiuuiAEIUUI", "eeiooyEEIOOY"], 1)[0]
        if not intab == outtab:
            try:
                trantab = maketrans(intab, outtab)
                result = word.translate(trantab)
            except Exception:
                result = word
            word = result
    return word


def name_chars_replace(word):
    if word:
        intab = ""
        outtab = ""
        switches = [['b', 'f', 'p', 'v'], ['c', 'g', 'k', 'q'], ['s', 'x', 'z'], ['d', 't'], ['m', 'n'],
                    ['r', 'l'], ['a', 'e', 'i', 'o', 'u', 'y']]
        for i in range(0, np.random.randint(len(word))):
            letter_set = np.random.choice(switches, 1)[0]
            intab += np.random.choice(letter_set, 1)[0]
            outtab += np.random.choice(letter_set, 1)[0]

        if not intab == outtab:
            try:
                trantab = maketrans(intab, outtab)
                result = word.translate(trantab)
            except Exception:
                result = word
            word = result
    return word