import numpy as np
from django.http import HttpResponse
import re

#--- Mathy functions for planetary things ----------------


def rand_range(low=0, high=1, weight=1, avg=0.5):

    if low == 0 and high == 1:
        return rand_weighted(avg, weight)

    #convert numbers to 0 - 1
    num_range = high-low
    if num_range <= 0:
        num_range = 1
    new_avg = (avg-low) / num_range

    rand = rand_weighted(new_avg, weight)

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


def bigger_makes_smaller(start=5, start_min=0, start_max=8, end=5000, end_min=1, end_max=12000, tries_to_adjust=2):
    # Used to inversely correlate two variables within a range
    # For example, the bigger stars are usually younger (as they'd burn out quicker)
    #   so if start is higher than average and end is higher than average, make end lower

    start_pct = clamp((start-start_min) / (start_max-start_min))
    end_pct = clamp((end-end_min) / (end_max-end_min))

    end_pct_guessed = rand_range(low=0, high=1, weight=tries_to_adjust, avg=(1-start_pct))
    end_pct = average_numbers_clamped(end_pct, end_pct_guessed)

    new_end = end_pct * (end_max-end_min)
    return new_end


def bigger_makes_bigger(start=5, start_min=0, start_max=10, end=5, end_min=0, end_max=10, tries_to_adjust=2):
    start_pct = clamp((start-start_min) / (start_max-start_min))
    end_pct = clamp((end-end_min) / (end_max-end_min))

    end_pct_guessed = rand_range(low=0, high=1, weight=tries_to_adjust, avg=start_pct)
    end_pct = average_numbers_clamped(end_pct, end_pct_guessed)

    new_end = end_pct * (end_max-end_min)
    return new_end


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