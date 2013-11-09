import random
import numpy as np
from django.http import HttpResponse


def test_generate_rand_nums(request, mean):
    content = ""
    avg = 0
    times = 400
    for n in range(0, times):
        num = rand_weighted(float(mean) or .3)
        content += " {0}".format(num)
        avg += num

    content += "<p>Avg:{0}".format(avg/times)

    status_code = 200
    mimetype='text/html'

    return HttpResponse(content, status=status_code, mimetype=mimetype)


def test_generate_rand_nums_as_image(request, mean):
    times = 100
    nums = []
    for n in range(0, times):
        num = rand_weighted(float(mean) or .3)
        nums.append(num)

    return image_from_array(request, nums)


#--- Maths functions for planetary things ----------------


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


def image_from_array(request, list_to_plot):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import matplotlib.pyplot as plot

    list_to_plot.sort()

    plot.hist(list_to_plot, bins=20, normed=1)       # matplotlib version (plot)
    canvas = FigureCanvas(plot.figure(1))

    #from matplotlib.figure import Figure
    #fig=Figure()
    #ax=fig.add_subplot(111)
    #x=[]
    #y=[]
    #x_count=0
    #list_to_plot.sort()
    #for i in list_to_plot:
    #    x_count+=1
    #    x.append(x_count)
    #    y.append(i)
    #ax.plot_date(x, y, '-')
    #canvas=FigureCanvas(fig)

    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response