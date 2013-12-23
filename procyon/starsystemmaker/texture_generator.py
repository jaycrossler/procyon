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
    ice_amount_total = float(request.GET.get('ice_amount_total', .02)) #TODO: Not yet used
    blur_radius = 0

    atmosphere_dust_amount = int(float(request.GET.get('atmosphere_dust_amount', 3)))

    rand_seed = float(request.GET.get('rand_seed', np.random.random()))
    rand_seed_num = set_rand_seed(rand_seed)

    #TODO: Try to get/save file from cache

    image_data = []

    white = (255, 255, 255, 255)

    #TODO: Determine based on minerals and atmosphere
    color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255), 255)
    for row in xrange(0, height):
        rand = (np.random.randint(-color_range, color_range), np.random.randint(-color_range, color_range), np.random.randint(-color_range, color_range), 0)
        draw_color = color = tuple(map(sum, zip(color, rand)))

        #Add Icecaps
        if use_icecaps and row < (height*ice_amount_n) or row > height-(height*ice_amount_s):
            if row < (height*ice_amount_n):
                from_edge = ((height*ice_amount_n)-row) / (height*ice_amount_n)
            else:
                from_edge = (row - (height-(height*ice_amount_s))) / (height*ice_amount_n)

            for i in range(0, width):
                if np.random.random() < (from_edge+.1):
                    blend_amount = clamp(np.random.random()+from_edge)
                    ice_draw_color = color_blend(base_color=draw_color, new_color=white, amount=blend_amount)
                    image_data.append(ice_draw_color)
                else:
                    image_data.append(draw_color)

        else:
            for i in range(0, width):
                image_data.append(draw_color)

    # Add Dust
    if atmosphere_dust_amount > 0:
        image_data = add_dust(image_data, dust_amount=atmosphere_dust_amount)

    if blur_radius > 0:
        image_data = blur_image(image_data, height=height, width=width, radius=blur_radius)

    im = Image.new('RGB', (width, height))
    im.putdata(image_data)

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


def add_dust(image_data, dust_amount=10):
    percent_dust = float(dust_amount) / 2000
    pixel_count = len(image_data)
    num_dust_pixels = clamp(int(percent_dust * pixel_count), 0, 10000)

    white = (255, 255, 255, 255)
    for dust in xrange(0, num_dust_pixels):
        x = np.random.randint(0, pixel_count)
        blur_amount = .3 + np.random.random()/3
        image_data[x] = color_blend(image_data[x], white, blur_amount)

    return image_data


def color_from_mineral(mineral_name='Iron'):
    return 200, 0, 0, 255


def blur_image(image_data, blur_horizontal=True, blur_vertical=True, height=256, width=256, radius=1):
    #TODO: Modify to support partial pixel blending

    # blur window length in pixels
    blur_window = radius*2+1

    out_image_data = image_data

    # blur horizontal row by row, and wrap around edges
    if blur_horizontal:
        for row in range(height):
            for column in range(0, width):
                total_red = 0
                total_green = 0
                total_blue = 0

                for rads in range(-radius, radius+1):
                    pixel = (row*width) + ((column+rads) % width)
                    total_red += image_data[pixel][0]/blur_window
                    total_green += image_data[pixel][1]/blur_window
                    total_blue += image_data[pixel][2]/blur_window

                out_image_data[row*width + column] = (total_red, total_green, total_blue, 255)
        image_data = out_image_data

    # blur vertical, but no wrapping
    if blur_vertical:
        for column in range(width):
            for row in range(0, height):
                total_red = 0
                total_green = 0
                total_blue = 0

                blur_window = 0
                for rads in range(-radius, radius+1):
                    if rads in range(0, height):
                        blur_window += 1

                for rads in range(-radius, radius+1):
                    row_mod = row+rads
                    if row_mod in range(0, height):
                        pixel = (row_mod*width) + column
                        total_red += image_data[pixel][0]/blur_window
                        total_green += image_data[pixel][1]/blur_window
                        total_blue += image_data[pixel][2]/blur_window

                out_image_data[row*width + column] = (total_red, total_green, total_blue, 255)
        image_data = out_image_data

    return image_data