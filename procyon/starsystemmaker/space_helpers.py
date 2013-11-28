from procyon.starsystemmaker.models import *
from procyon.starsystemmaker.math_helpers import *
import csv
import re

#This loads a list of info into memory, maybe should be a DB table instead?
with open('procyon/fixtures/star_spectrums.csv', mode='rU') as infile:
    reader = csv.reader(infile,)
    STAR_DICT = {rows[0]: rows[1] for rows in reader if len(rows) == 2}


def get_star_type(stellar):
    star_a, star_b, star_c = "", "", ""
    if not stellar or len(stellar) < 1:
        return star_a, star_b, star_c

    stellar = stellar.lstrip('esd')

    parts = re.findall(r'(\w)([-+]?[0-9]*\.?[0-9]*)[ ]*([IV]*)', stellar)
    if parts and len(parts) > 0 and len(parts[0]) > 0:
        star_a = parts[0][0] or ""
        star_a = star_a.upper()
        star_b = parts[0][1] or 4
        star_b = parse_num(star_b, True)
        star_c = parts[0][2] or ""

    return star_a, star_b, star_c


def color_of_star(star_a, star_b, star_c):
    """
    Uses http://www.vendian.org/mncharity/dir3/starcolor/ to convert star
    spectrum values to likely web colors. Does a lot of cleanup
    """

    color = ""
    cleaned = '{0}{1}{2}'.format(star_a, star_b, star_c)
    for key in STAR_DICT:
        if key.startswith(cleaned):
            color = STAR_DICT.get(key)
            break
    if color == "" and star_a and star_b:
        cleaned = '{0}{1}'.format(star_a, star_b)
        for key in STAR_DICT:
            if key.startswith(cleaned):
                color = STAR_DICT.get(key)
                break
    if color == "" and star_a:
        cleaned = star_a
        for key in STAR_DICT:
            if key.startswith(cleaned):
                color = STAR_DICT.get(key)
                break
    return color


def color_by_spectrum(stellar):
    star_a, star_b, star_c = get_star_type(stellar)
    return color_of_star(star_a, star_b, star_c)