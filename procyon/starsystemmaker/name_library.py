from procyon.starsystemmaker.math_helpers import *
import random
import os
import numpy as np
import fuzzy
from string import maketrans


def list_of_names(file_sub_strings=list(), prefix_chance=0, prefixes=list(), max_count=50):
    #TODO: Should this be list() not [] ?
    # Can limit names like file_sub_strings=['korean','male'] or ['avian'] or ['male','1980']

    name_file_dir = 'procyon/fixtures/names/'
    name_file_list = os.listdir(name_file_dir)

    sub_file_list = []
    for search_string in file_sub_strings:
        for n in name_file_list:
            if search_string == 'male':
                if '_male' in n:
                    sub_file_list.append(n)
            elif search_string in n:
                sub_file_list.append(n)

    if len(sub_file_list):
        name_file = np.random.choice(sub_file_list)
    else:
        if len(name_file_list):
            name_file = np.random.choice(name_file_list)
        else:
            return ['Jon']

    with open(name_file_dir + name_file, mode='r') as infile:
        name_list = [line.strip() for line in infile if len(line)]
    name_list = name_list[:max_count]

    np.random.shuffle(name_list)

    if prefix_chance and prefixes:
        for i in range(len(name_list)):
            if np.random.random() < prefix_chance:
                prefix = np.random.choice(prefixes)
                if not name_list[i].startswith(prefix):
                    name_list[i] = prefix + " " + name_list[i]

    return name_list


def name_part_fuzzer(name_parts, modifications=4):
    if isinstance(name_parts,basestring):
        name_parts = name_parts.split(" ")
    if modifications:
        part_count = len(name_parts)
        function_names = ["name_nysiis", "name_vowel_switch", "name_chars_replace", "name_add_vowels"]
        for i in range(0, int(modifications)):
            idx_part = np.random.randint(part_count)
            name_part = name_parts[idx_part]

            func = np.random.choice(function_names, 1)[0]
            method_to_call = globals()[func]
            result = method_to_call(name_part)

            if len(name_part) > 3:
                name_parts[idx_part] = result

    return name_parts


def name_nysiis(word):
    if word:
        try:
            result = fuzzy.nysiis(word)
            if result:
                word = result
        except ValueError:
            result = word
    return word


def name_vowel_switch(word):
    if word:
        intab = "aeiouyAEIOUY"
        outtab = np.random.choice(["aaiuuyAAIUUY", "eeeuuyEEEUUY", "ieiouyIEIOUY",
                                   "aeaooyAEAOOY", "aeiuuiAEIUUI", "eeiooyEEIOOY"], 1)[0]
        if not intab == outtab:
            try:
                trantab = maketrans(intab, outtab)
                result = word
                result = result.translate(trantab)
            except Exception:
                result = word
            if result:
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
                result = word
                result = result.translate(trantab)
            except Exception:
                result = word
            if result:
                word = result

    return word


def name_add_vowels(word):
    if word:
        vowels = "aeiouyAEIOUY ,1234567890-/"
        vowels_lower = "a a e e i o o u u y".split()
        result = ""

        for idx, c in enumerate(word):
            char = c
            next = word[idx+1] if idx < len(word)-1 else ''
            result += c
            if char not in vowels and next not in vowels:
                if np.random.random() < .3:
                    result += np.random.choice(vowels_lower, 1)[0]
                if np.random.random() < .3:
                    result += np.random.choice(vowels_lower, 1)[0]

        if result:
            word = result
    return word