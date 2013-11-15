import csv
import re
from procyon.starsystemmaker.math_helpers import *

with open('procyon/fixtures/star_spectrums.csv', mode='rU') as infile:
    reader = csv.reader(infile,)
    STAR_DICT = {rows[0]:rows[1] for rows in reader if len(rows) == 2}


def get_star_type(stellar):
    star_a, star_b, star_c = "", "", ""
    if not stellar or len(stellar) < 2:
        return star_a, star_b, star_c

    parts = re.findall(r'd*(\w)([-+]?[0-9]*\.?[0-9]+)[ ]*([IV]*)', stellar)
    if parts and len(parts) > 0 and len(parts[0]) > 0:
        star_a = parts[0][0] or "K"
        star_a = star_a.upper()
        star_b = parts[0][1] or ""
        star_b = int(float(star_b))
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
        if cleaned.startswith(key):
            color = STAR_DICT.get(key)
            break
    return color

