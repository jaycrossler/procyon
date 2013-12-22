from django.http import HttpResponse
import numpy as np
from procyon.starsystemmaker.math_helpers import *

try:
    import Image
    import ImageEnhance
    import ImageDraw
except ImportError:
    try:
        from PIL import Image
        from PIL import ImageEnhance
        from PIL import ImageDraw
    except ImportError:
        raise ImportError("The Python Imaging Library was not found.")


def generate_texture(request, image_format="PNG"):

    width = height = int(request.GET.get('size', 256))
    color_range = int(request.GET.get('color_range', 5))
    use_icecaps = str(request.GET.get('use_icecaps', 'true')).lower() == 'true'
    amount_ice_n = float(request.GET.get('amount_ice_n', 5))/100
    amount_ice_s = float(request.GET.get('amount_ice_s', 8))/100

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
            if row < (height*amount_ice_n) or row > height-(height*amount_ice_s):
                if row < (height*amount_ice_n):
                    from_edge = ((height*amount_ice_n)-row) / (height*amount_ice_n)
                else:
                    from_edge = (row - (height-(height*amount_ice_s))) / (height*amount_ice_n)

                white = (255, 255, 255, 255)
                blend_amount = np.random.random()+from_edge
                blend_amount = clamp(blend_amount)

                draw_color = color_blend(base_color=draw_color, new_color=white, amount=blend_amount)
        #TODO: Build into a data array, separate out into functions
        draw.line((0, row, width, row), fill=draw_color)

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