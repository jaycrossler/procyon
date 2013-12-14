import numpy as np
from django.http import HttpResponse
import re

#--- Mathy functions for planetary things ----------------


def rand_range(low=0, high=1, weight=1, avg=0.5):
    rand = rand_weighted(avg, weight)
    if low == 0 and high == 1:
        return rand

    num_range = high-low
    rand = low + (num_range*rand)
    return rand


def rand_range_from_text(rand_text=""):
    if rand_text:
        parts = re.findall(r'([0-9.]*)[ -]*([0-9.]*)', str(rand_text))
        if parts and len(parts) > 0 and len(parts[0]) > 0:
            low = parse_num(parts[0][0])
            high = parse_num(parts[0][1])
            if low:
                if high:
                    return rand_range(low, high, 2)
                else:
                    return rand_range(low*0.5, low*1.5, 3)
    return rand_range()


def rand_weighted(midpoint=0.5, weight=3):
    """
    Returns a random number between 0 and 1, weighted to be closer to 'goal'.
    'weight' determines how heavily the number is weighted towards the goal.

    Note that the entire returned range will be 0 < x < 1, but that multiple
    returns averaged together will be closer to .5 (so 1000 tries at midpoint
    .9 will average to .75, not to .9... even though higher ones are returned)
    """

    closest = np.random.sample()
    for x in range(0, int(weight)-1):
        tempnum = np.random.sample()
        if is_x_closer_to_mid_then_y(tempnum, closest, midpoint):
            closest = tempnum
    return closest


def is_x_closer_to_mid_then_y(x, y, mid):
    mid_to_x = abs(mid-x)
    mid_to_y = abs(mid-y)

    is_x_closer = False
    if mid_to_x < mid_to_y:
        is_x_closer = True
    return is_x_closer


def image_histogram_from_array(request, list_to_plot, bins=50):
    """
    Builds a png image from a list passed into it, shown as a histogram
    """
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.pyplot as plot

    list_to_plot.sort()
    plot.hist(list_to_plot, bins=bins, normed=1)
    canvas = FigureCanvas(plot.figure(1))

    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plot.clf()

    return response


def parse_int(str):
    import re
    return int(re.match(r'\d+', str).group())


def parse_num(s, force_int=False):
    try:
        return int(s)
    except ValueError:
        if force_int:
            return 0
        try:
            return float(s)
        except Exception:
            return 0


def average_numbers_clamped(num_1=0, num_2=0):
    if num_1 and not num_2:
        return num_1
    if num_2 and not num_1:
        return num_2
    return float((num_1+num_2) / 2)


def clamp(value, v_min=0, v_max=1):
    if value < v_min:
        return v_min
    if value > v_max:
        return v_max
    return value


def bigger_makes_smaller(mass=5, mass_min=0, mass_max=8, age=5000, age_min=1, age_max=12000, tries_to_adjust=2):
    # Used to inversely correlate two variables within a range
    # For example, the bigger stars are usually younger (as they'd burn out quicker)
    #   so if mass is higher than average and age is higher than average, make age lower

    mass_pct = clamp(mass / (mass_max-mass_min))
    age_pct = clamp(age / (age_max-age_min))

    age_pct_guessed = rand_range(low=0, high=1, weight=tries_to_adjust, avg=(1-mass_pct))
    age_pct = average_numbers_clamped(age_pct, age_pct_guessed)

    new_age = age_pct * (age_max-age_min)
    return new_age


def get_float_from_hash(options={}, var_name='', backup_val=0):

    try:
        val = float(options.get(var_name))
    except Exception:
        val = backup_val

    return val


def set_rand_seed(rand_seed=4815162342):
    try:
        rand_seed = float(rand_seed)
    except Exception as e:
        rand_seed = np.random.random()
    rand_seed_num = rand_seed
    if rand_seed < 1:
        rand_seed_num = rand_seed * 100000000
    rand_seed_num = int(rand_seed_num)
    np.random.seed(rand_seed_num)

    return rand_seed_num