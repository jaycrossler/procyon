from procyon.starsystemmaker.math_helpers import *
import random
import os


def list_of_names(name_file='', num_requested=20, use_prefix=True, prefix='New'):
    name_file_dir = 'procyon/fixtures/names/'
    if not name_file:
        name_file = random.choice(os.listdir(name_file_dir))
    if not name_file.endswith('txt'):
        name_file += '.txt'

    with open(name_file_dir + name_file, mode='rU') as infile:
        name_list = [line.strip() for line in infile]

    name_list = random.sample(name_list, num_requested)

    if use_prefix and prefix:
        for i in range(len(name_list)):
            if not name_list[i].startswith(prefix):
                if random.random() < 0.2:
                    name_list[i] = prefix+" "+name_list[i]

    return name_list