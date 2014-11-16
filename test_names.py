import numpy as np
import os


def list_of_names(file_sub_strings=[], prefix_chance=0, prefixes=['New', 'Old'], max_count=50):
    #TODO: Should this be list() not [] ?
    # Can limit names like file_sub_strings=['korean','male'] or ['avian'] or ['male','1980']

    name_file_dir = 'procyon/fixtures/names/'
    name_file_list = os.listdir(name_file_dir)

    for search_string in file_sub_strings:
        sub_file_list = []
        for n in name_file_list:
            if search_string == 'male':
                if 'male' in n and 'female' not in n:
                    sub_file_list.append(n)
            elif search_string in n:
                sub_file_list.append(n)
        name_file_list = sub_file_list

    name_file = np.random.choice(name_file_list)

    with open(name_file_dir + name_file, mode='r') as infile:
        name_list = [line.strip() for line in infile if len(line)]

    np.random.shuffle(name_list)

    if prefix_chance and prefixes:
        for i in range(len(name_list)):
            if np.random.random() < prefix_chance:
                prefix = np.random.choice(prefixes)
                if not name_list[i].startswith(prefix):
                    name_list[i] = prefix + " " + name_list[i]

    return name_list[:max_count]


def name():
    name_file_dir = 'procyon/fixtures/names/'
    name_file_list = os.listdir(name_file_dir)

    sub_file_list = []
    for n in name_file_list:
        if 'male' not in n \
                and 'female' not in n \
                and 'family' not in n \
                and '_things' not in n \
                and '_places' not in n \
                and not n.startswith(".") \
                and not n.startswith("_"):
            sub_file_list.append(n)


    name_file = sub_file_list[0]
    name_file = ".txt".join(name_file.split(".txt")[:-1]) #remove last .txt
    print(name_file)

    source_file = name_file_dir + name_file + ".txt"
    male_file = name_file_dir + name_file + "_male.txt"
    female_file = name_file_dir + name_file + "_female.txt"
    last_file = name_file_dir + name_file + "_family.txt"
    thing_file = name_file_dir + name_file + "_things.txt"
    source_file_done = name_file_dir + "_" + name_file + ".txt"

    if source_file and name_file:
        print("FILE NAME: "+source_file)
        infile = open(source_file, mode='r')
        out_male = open(male_file, mode='a')
        out_female = open(female_file, mode='a')
        out_last = open(last_file, mode='a')
        out_things = open(thing_file, mode='a')

        name_list = [line.strip() for line in infile]
        for name in name_list:
            user_input = raw_input("m/f/l/b/t: "+name + "? ")
            user_input = user_input.lower()

            if "m" in user_input or "b" in user_input:
                out_male.write(name+"\n")
            if "f" in user_input or "b" in user_input:
                out_female.write(name+"\n")
            if "l" in user_input:
                out_last.write(name+"\n")
            if "t" in user_input:
                out_things.write(name+"\n")

        out_female.close()
        out_things.close()
        out_male.close()
        out_last.close()
        infile.close()
        os.rename(source_file, source_file_done)
