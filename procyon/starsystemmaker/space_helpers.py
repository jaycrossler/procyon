from procyon.starsystemmaker.models import *
from procyon.starsystemmaker.math_helpers import *
from procyon.starsystemmaker.name_library import *
from procyon.starcatalog.models import StarType, StarLuminosityType
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
    if color == "":
        color = "#ffc676"
    return color


def color_by_spectrum(stellar):
    star_a, star_b, star_c, star_d = get_star_type(stellar)
    return color_of_star(star_a, star_b, star_c)


def closest_stars(item, star_model, distance=10, goal_count=140):
    origin = item.location
    origin_array = numpy.array((origin.x, origin.y, origin.z))

    close_by_stars = star_model.objects.filter(location__distance_lte=(origin, D(m=distance))).distance(origin)
    close_by_stars = close_by_stars.order_by('distance')

    star_list = []
    for s in close_by_stars:
        location_array = numpy.array((s.location.x, s.location.y, s.location.z))

        #NOTE: Because Django doesn't support ST_DWithin, use this to method to pull more than we want (everything
        #      within x and y bounds, but too many within z bounds. Then, ignore those not within bounds mathematically
        #      Should use this, but not supported: http://postgis.net/docs/ST_3DDWithin.html

        dist = numpy.linalg.norm(origin_array - location_array)
        if dist > distance:
            continue

        star_handle = dict()
        if s == item:
            star_handle['centered'] = True
        star_handle['name'] = s.star.__unicode__()
        star_handle['id'] = s.star.id
        star_handle['spectrum'] = s.star.spectrum
        star_handle['web_color'] = color_by_spectrum(s.star.spectrum)
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


def star_variables(options={}):

    rand_seed = get_float_from_hash(options, 'rand_seed', numpy.random.random())
    rand_seed_num = set_rand_seed(rand_seed)

    forced_temp = get_float_from_hash(options, 'temp', 0)
    forced_mass = get_float_from_hash(options, 'mass', 0)
    forced_radius = get_float_from_hash(options, 'radius', 0)
    forced_age = get_float_from_hash(options, 'age', 0)

    temp = 0
    mass = 0
    radius = 0
    age = 0
    stellar = str(options.get('stellar', 'M3V'))

    star_type = options.get('star_type', None)
    star_l_type = options.get('luminosity_class', None)
    star_l_mod = options.get('luminosity_mod', None)
    star_color = ''

    if stellar and not star_type and not star_l_type and not star_l_mod:
        star_a, star_b, star_c, star_d = get_star_type(stellar)
        try:
            star_type = StarType.objects.get(symbol=star_a)
        except Exception:
            star_type = StarType.objects.get(symbol='M')
        star_color = color_of_star(star_a, star_b, star_c)
        try:
            star_l_type = StarLuminosityType.objects.get(symbol=star_c)
        except Exception:
            star_l_type = None
        star_l_mod = star_d

    star_type_name = ''
    if star_type:
        if star_type.surface_temp_range:
            temp = rand_range_from_text(star_type.surface_temp_range)
        if star_type.mass_range:
            mass = rand_range_from_text(star_type.mass_range)
        if star_type.radius_range:
            radius = rand_range_from_text(star_type.radius_range)
        if star_type.age:
            age = rand_range_from_text(star_type.age)
        star_type_name = str(star_type.name)

    star_l_type_name = ''
    if star_l_type:
        if star_l_type.temp_range:
            temp = average_numbers_clamped(temp, rand_range_from_text(star_l_type.temp_range))
        if star_l_type.mass_range:
            mass = (mass or 1) * rand_range_from_text(star_l_type.mass_range)
        if star_l_type.radius_range:
            radius = average_numbers_clamped(radius, rand_range_from_text(star_l_type.radius_range))
        star_l_type_name = str(star_l_type.short_name)

    if star_l_mod and mass:
        if star_l_mod == 'a-0':
            mass *= 15
        if star_l_mod == 'a':
            mass *= 5
        if star_l_mod == 'ab':
            mass *= 3
        if star_l_mod == 'b':
            mass *= 1

    age = bigger_makes_smaller(start=mass, start_min=0, start_max=10, end=age, end_min=1, end_max=11000,
                               tries_to_adjust=5)

    if forced_mass:
        mass = forced_mass
    if forced_temp:
        temp = forced_temp
    if forced_radius:
        radius = forced_radius
    if forced_age:
        age = forced_age

    return {'temp': temp, 'mass': mass, 'radius': radius, 'age': age, 'color': star_color,
            'rand': rand_seed_num, 'stellar': stellar, 'star_type_name': star_type_name,
            'luminosity_class': star_l_type_name, 'luminosity_mod': star_l_mod}


def planet_from_variables(settings={}):
    rand_seed = get_float_from_hash(settings, 'rand')
    set_rand_seed(rand_seed)

    mass = get_float_from_hash(settings, 'mass')
    planet_count_max = (1.5+mass)*(1.5+mass)
    planet_count_max = clamp(planet_count_max, 0, 20)
    planet_count = rand_range(low=0, high=planet_count_max, weight=3, avg=4)
    planet_count = int(planet_count)

    planets = []

    planet_name_list = list_of_names()

    settings['name'] = planet_name_list[0]
    settings['planets'] = planet_count
    for i in range(planet_count):
        planet_data = create_random_planet(settings, i+1, planet_name_list, rand_seed=rand_seed)
        planets.append(planet_data)
    settings['planet_data'] = planets

    return settings


def create_random_planet(settings={}, planet_num=1, planet_name_list=None, rand_seed=''):
    num_planets = settings['planets']
    if not planet_name_list:
        planet_name_list = list_of_names()

    if len(planet_name_list) > planet_num:
        name = planet_name_list[planet_num]
    else:
        name = "Planet {0}".format(planet_num)

    star_age = get_float_from_hash(settings, 'age', 5000)

    mass_max = 2 + (planet_num * 2)
#    mass_max *= (mass_max/2)
    mass = bigger_makes_bigger(start=star_age, start_min=0, start_max=12000,
                               end=1, end_min=0.01, end_max=mass_max, tries_to_adjust=7)
    radius = bigger_makes_bigger(start=mass, start_min=0.01, start_max=mass_max,
                                 end=2, end_min=0.002, end_max=8, tries_to_adjust=4)
    density = bigger_makes_bigger(start=mass, start_min=0.01, start_max=mass_max,
                                  end=5, end_min=0.6, end_max=10, tries_to_adjust=3)
    gravity = mass/(radius*radius)
    oblateness = rand_range(0, 0.1, 1, 0.04)
    tilt = rand_range(0, 180, 1, 20)
    albedo = rand_range(0, 1, 2, 0.2)
    length_days = rand_range(0, 80, 2, 24)

    craterization = 0
    surface_solidity = 0
    surface_ocean_amount = 0

    ice_amount_total = rand_range(0, .1, 1, 0.05)
    ice_amount_north_pole = rand_range(0, .1, 1, 0.01)
    ice_amount_south_pole = rand_range(0, .1, 1, 0.01)

    if (radius * mass) > 20:
        #Gas Giant
        craterization = 0
        ring_size = rand_range(0, 10, 2, 2)
        ring_numbers = bigger_makes_bigger(start=ring_size, start_min=0, start_max=10,
                                           end=4, end_min=1, end_max=12, tries_to_adjust=2)
        ring_numbers = int(ring_numbers)
        atmosphere_millibars = bigger_makes_bigger(start=gravity, start_min=0.01, start_max=5,
                                                   end=1, end_min=0.1, end_max=20000, tries_to_adjust=2)
        surface_temp_low = rand_range(-240, 200, 2, -100)
        surface_temp_low = bigger_makes_smaller(start=planet_num, start_min=0, start_max=num_planets,
                                                end=surface_temp_low, end_min=-220, end_max=200, tries_to_adjust=2)

        surface_temp_high = rand_range(surface_temp_low, 200, 2, surface_temp_low+20)
        surface_temperature_range = "{0} - {1}".format(surface_temp_low, surface_temp_high)

        magnetic_field = bigger_makes_bigger(start=mass, start_min=0.01, start_max=mass_max,
                                             end=1, end_min=0.1, end_max=20000, tries_to_adjust=2)

    else:
        if radius < 2.2:
            craterization = rand_range(0, 5, 1, 1)
            surface_ocean_amount = rand_range(0, 1, 2, 0.9)

            ice_amount_total = rand_range(0, 1, 1, 0.5)
            ice_space_left = 1 - ice_amount_total
            ice_amount_north_pole = rand_range(0, ice_space_left, 2, 0.01)
            ice_space_left -= ice_amount_north_pole
            ice_amount_south_pole = rand_range(0, ice_space_left, 2, 0.01)

        surface_solidity = 1
        ring_size = 0
        ring_numbers = 0
        atmosphere_millibars = bigger_makes_bigger(start=gravity, start_min=0.01, start_max=5,
                                                   end=1, end_min=0.1, end_max=50, tries_to_adjust=2)
        surface_temp_low = rand_range(-240, 200, 2, 0)
        surface_temp_low = bigger_makes_smaller(start=planet_num, start_min=0, start_max=num_planets,
                                                end=surface_temp_low, end_min=-220, end_max=200, tries_to_adjust=2)
        surface_temp_high = rand_range(surface_temp_low, 200, 2, surface_temp_low+30)

        magnetic_field = bigger_makes_bigger(start=mass, start_min=0.01, start_max=mass_max,
                                             end=1, end_min=0.1, end_max=100, tries_to_adjust=2)

    mineral_surface_early = rand_range(0, 0.95, 3, 0.9)
    space_left = 1 - mineral_surface_early
    mineral_surface_mid = rand_range(0, space_left, 1, space_left)
    space_left = 1 - mineral_surface_early + mineral_surface_mid
    mineral_surface_heavy = rand_range(0, space_left, 1, space_left)
    space_left = 1 - mineral_surface_early + mineral_surface_mid + mineral_surface_heavy
    mineral_surface_late = space_left
    minerals_specific = 'Hydrogen, Helium, Iron' #TODO: Randomize and make awesome

    solid_core_size = rand_range(0, 1, 2, .3)
    solid_core_type = 'Iron'
    plate_tectonics_amount = rand_range(0, 30, 2, 1)
    surface_ocean_chemicals = 'Salt Water'

    atmosphere_dust_amount = 0
    if surface_solidity > .9:
        atmosphere_dust_amount = int(rand_range(1, 1000, 2, 10))

    num_moons_max = 1 + (planet_num * 4)
    if planet_num > 6:
        num_moons_max = 1 + (planet_num * 2)

    num_moons = rand_range(0, num_moons_max, 7, 0)
    num_moons = bigger_makes_bigger(start=gravity, start_min=0.1, start_max=5,
                                    end=num_moons, end_min=0, end_max=num_moons_max, tries_to_adjust=1)
    num_moons = int(num_moons)

    rand_seed_planet = "{0}00{1}".format(int(rand_seed), planet_num)

    planet_data = {'name': name, 'position': planet_num, 'mass': mass, 'radius': radius,
                   'density': density, 'gravity': gravity, 'oblateness': oblateness,
                   'tilt': tilt, 'albedo': albedo, 'magnetic_field': magnetic_field,
                   'craterization': craterization, 'surface_solidity': surface_solidity,
                   'surface_ocean_amount': surface_ocean_amount,

                   'ice_amount_total': ice_amount_total,
                   'ice_amount_north_pole': ice_amount_north_pole,
                   'ice_amount_south_pole': ice_amount_south_pole,
                   'atmosphere_millibars': atmosphere_millibars, 'solid_core_size': solid_core_size,
                   'solid_core_type': solid_core_type, 'plate_tectonics_amount': plate_tectonics_amount,
                   'surface_ocean_chemicals': surface_ocean_chemicals, 'ring_size': ring_size,
                   'ring_numbers': ring_numbers, 'length_days': length_days,
                   'surface_temp_low': surface_temp_low,
                   'surface_temp_high': surface_temp_high,

                   'atmosphere_dust_amount': atmosphere_dust_amount,

                   'mineral_surface_early': mineral_surface_early,
                   'mineral_surface_mid': mineral_surface_mid,
                   'mineral_surface_heavy': mineral_surface_heavy,
                   'mineral_surface_late': mineral_surface_late,
                   'minerals_specific': minerals_specific,

                   'num_moons': num_moons, 'rand_seed': rand_seed_planet,
                   }
    #TODO: Loop through everything, and if a float, only return 4? decimal points of data

    moon_name_list = list_of_names()
    moons = []
    for i in range(num_moons):
        moon_data = create_random_moon(planet_data, i, moon_name_list)
        moons.append(moon_data)
    planet_data['moons'] = moons

    return planet_data


def create_random_moon(planet_data, moon_num, moon_name_list):
    if len(moon_name_list) > moon_num:
        name = moon_name_list[moon_num]
    else:
        name = "Moon {0}".format(moon_num)

    r = lambda: np.random.randint(0, 255)
    color = '#%02X%02X%02X' % (r(), r(), r())

    return {'name': name, 'moon_num': moon_num, 'color':color}