from django.http import HttpResponse
import numpy as np
from procyon.starsystemmaker.math_helpers import *

try:
    import Image
    import ImageEnhance
    import ImageDraw
    import ImageFilter
except ImportError:
    try:
        from PIL import Image
        from PIL import ImageEnhance
        from PIL import ImageDraw
        from PIL import ImageFilter
    except ImportError:
        raise ImportError("The Python Imaging Library was not found.")


def generate_texture(request, image_format="PNG"):

    width = height = int(request.GET.get('size', 256))
    color_range = int(request.GET.get('color_range', 5))
    use_icecaps = str(request.GET.get('use_icecaps', 'true')).lower() == 'true'
    ice_amount_n = float(request.GET.get('ice_amount_north_pole', .03))
    ice_amount_s = float(request.GET.get('ice_amount_south_pole', .03))
    ice_amount_total = float(request.GET.get('ice_amount_total', .04)) #TODO: Not yet used

    atmosphere_dust_amount = float(request.GET.get('atmosphere_dust_amount', 3))

    rand_seed = float(request.GET.get('rand_seed', np.random.random()))
    rand_seed_num = set_rand_seed(rand_seed)


    #TODO: Try to get/save file from cache

    im = Image.new('RGB', (width, height))

    draw = ImageDraw.Draw(im)
    color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255), 255)
    for row in xrange(0, height):
        rand = (np.random.randint(-color_range, color_range), np.random.randint(-color_range, color_range), np.random.randint(-color_range, color_range), 0)
        draw_color = color = tuple(map(sum, zip(color, rand)))

        if use_icecaps:
            if row < (height*ice_amount_n) or row > height-(height*ice_amount_s):
                if row < (height*ice_amount_n):
                    from_edge = ((height*ice_amount_n)-row) / (height*ice_amount_n)
                else:
                    from_edge = (row - (height-(height*ice_amount_s))) / (height*ice_amount_n)

                white = (255, 255, 255, 255)
                blend_amount = np.random.random()+from_edge
                blend_amount = clamp(blend_amount)

                draw_color = color_blend(base_color=draw_color, new_color=white, amount=blend_amount)
        #TODO: Build into a data array, separate out into functions
        draw.line((0, row, width, row), fill=draw_color)

    if atmosphere_dust_amount > 0:
        percent_dust = float(atmosphere_dust_amount / 1000)
        num_dust_pixels = clamp(int(percent_dust * height * width), 0, 6000)  #TODO: Really need to move to a data array
        for dust in xrange(0, num_dust_pixels):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            gray = (128, 128, 128, np.random.randint(100, 255))
            draw.point((x, y), fill=gray)

    #TODO: Add a custom horizontal blur, like in: http://stackoverflow.com/questions/5527809/whats-wrong-with-this-python-image-blur-function
    #im = im.filter(ImageFilter.BLUR)

    mime = "image/png"
    if image_format == "JPEG":
        mime = "image/jpeg"
    response = HttpResponse(mimetype=mime)
    im.save(response, image_format)

    return response


def color_blend(base_color=(255, 255, 255, 255), new_color=(0, 0, 255, 255), amount=.2):
    r = (base_color[0]*(1-amount)) + (new_color[0]*amount)
    g = (base_color[1]*(1-amount)) + (new_color[1]*amount)
    b = (base_color[2]*(1-amount)) + (new_color[2]*amount)
    a = (base_color[3]*(1-amount)) + (new_color[3]*amount)

    return int(r), int(g), int(b), int(a)