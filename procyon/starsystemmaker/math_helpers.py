import numpy as np
from django.http import HttpResponse
import re

#--- Mathy functions for planetary things ----------------


def rand_range(low=0, high=1, weight=1):
    rand = rand_weighted(0.5, weight)
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
