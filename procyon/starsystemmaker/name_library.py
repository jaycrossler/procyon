from procyon.starsystemmaker.math_helpers import *
import random
import os
import numpy as np


def list_of_names(name_file='', num_requested=20, use_prefix=True, prefix='New', prefix2='Old'):
    name_file_dir = 'procyon/fixtures/names/'
    if not name_file:
        name_file_list = os.listdir(name_file_dir)
        name_num = np.random.randint(len(name_file_list))
        name_file = name_file_list[name_num]
    if not name_file.endswith('txt'):
        name_file += '.txt'

    with open(name_file_dir + name_file, mode='r') as infile:
        name_list = [line.strip() for line in infile]

    np.random.shuffle(name_list)

    if use_prefix and prefix:
        for i in range(len(name_list)):
            if not name_list[i].startswith(prefix):
                if np.random.random() < 0.02:
                    name_list[i] = prefix+" "+name_list[i]
                elif np.random.random() < 0.02:
                    name_list[i] = prefix2+" "+name_list[i]

    return name_list