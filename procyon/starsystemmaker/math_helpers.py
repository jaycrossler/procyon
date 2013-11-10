import numpy as np
from django.http import HttpResponse

#--- Mathy functions for planetary things ----------------


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

    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plot.clf()

    return response


def parse_int(str):
    import re
    return int(re.match(r'\d+', str).group())