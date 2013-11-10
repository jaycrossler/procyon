from django.http import HttpResponse
from procyon.starsystemmaker.math_helpers import *
from procyon.starsystemmaker.space_helpers import *


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
    times = 1000
    nums = []
    for n in range(0, times):
        num = rand_weighted(float(mean) or .3)
        nums.append(num)

    return image_histogram_from_array(request, nums)

