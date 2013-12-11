from procyon.starsystemmaker.models import *
from procyon.starsystemmaker.math_helpers import *
import csv
import re
import numpy

#This loads a list of info into memory, maybe should be a DB table instead?
with open('procyon/fixtures/star_spectrums.csv', mode='rU') as infile:
    reader = csv.reader(infile,)
    STAR_DICT = {rows[0]: rows[1] for rows in reader if len(rows) == 2}


def get_star_type(stellar):
    star_a, star_b, star_c, star_d = "", "", "", ""
    if not stellar or len(stellar) < 1:
        return star_a, star_b, star_c, star_d

    stellar = stellar.lstrip('esd')

    parts = re.findall(r'(\w)([-+]?[0-9]*\.?[0-9]*)[ ]*([IV]*)([a]?[b]?(\-0)?)', stellar)
    if parts and len(parts) > 0 and len(parts[0]) > 0:
        star_a = parts[0][0] or ""
        star_a = star_a.upper()
        star_b = parts[0][1] or 4
        star_b = parse_num(star_b, True)
        star_c = parts[0][2] or ""
        star_d = parts[0][3] or ""

    return star_a, star_b, star_c, star_d


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


def closest_stars(item, star_model, distance=10, goal_count=140):
    origin = item.location
    origin_array = numpy.array((origin.x, origin.y, origin.z))

    close_by_stars = star_model.objects.filter(location__distance_lte=(origin, D(m=distance))).distance(origin).order_by('distance')

    star_list = []
    for s in close_by_stars:
        location_array = numpy.array((s.location.x, s.location.y, s.location.z))

        #NOTE: Because Django doesn't support ST_DWithin, use this to method to pull more than we want (everything within
        #      x and y bounds, but too many within z bounds. Then, ignore those not within bounds mathematically
        #      Should use this, but not supported: http://postgis.net/docs/ST_3DDWithin.html

        dist = numpy.linalg.norm(origin_array - location_array)
        if dist > distance:
            continue

        star_handle = dict()
        if s == item:
            star_handle['centered'] = True
        star_handle['name'] = s.star.__unicode__()
        star_handle['id'] = s.star.id
        star_handle['web_color'] = s.star.web_color()
        star_handle['x'] = s.location.x
        star_handle['y'] = s.location.y
        star_handle['z'] = s.location.z
        star_handle['mass'] = s.guessed_mass or 0
        star_handle['mag'] = s.star.mag or 0
        star_handle['abs_mag'] = s.star.abs_mag or 0
        star_handle['dist'] = dist
        star_list.append(star_handle)

    #NOTE: If not enough were found, expand the search distance
    len_star_list = len(star_list)
    if len_star_list < goal_count and distance < 40:
        star_list = closest_stars(item, star_model, distance*2, goal_count)

    star_list = sorted(star_list, key=lambda k: k['dist'])

    return star_list