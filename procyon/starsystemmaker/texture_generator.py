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
    ice_n = float(request.GET.get('ice_north_pole', .03))
    ice_s = float(request.GET.get('ice_south_pole', .03))
    ice_total = float(request.GET.get('ice_total', .02))

    atmosphere_dust_amount = int(float(request.GET.get('atmosphere_dust_amount', 3)))

    #TODO: Use Blur?
    blur_radius = 0

    rand_seed = float(request.GET.get('rand_seed', np.random.random()))
    set_rand_seed(rand_seed)

    #TODO: Try to get/save file from file cache

    image_data = []

    #TODO: Determine based on minerals and atmosphere
    color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)
    for row in xrange(0, height):
        rand = (randint(-color_range, color_range), randint(-color_range, color_range), randint(-color_range, color_range), 0)
        draw_color = color = tuple(map(sum, zip(color, rand)))
        for i in range(0, width):
            image_data.append(draw_color)

    #Add Ice
    if use_icecaps:
        image_data = add_icecaps(image_data, ice_n=ice_n, ice_s=ice_s, height=height, width=width)        
    if ice_total:
        image_data = add_ice(image_data, ice=ice_total)

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


def add_icecaps(image_data, ice_n=0.01, ice_s=0.01, height=256, width=256):
    ice_color = (255, 255, 255, 255)
    ice_buffer = 0

    for row in range(0, height):
        if row < (height*ice_n) or row > height-(height*ice_s):
            if row < (height*ice_n):
                from_edge = ((height*ice_n)-row) / (height*ice_n)
            else:
                from_edge = (row - (height-(height*ice_s))) / (height*ice_s)

            for i in range(0, width):
                if np.random.random() < (from_edge+ice_buffer):
                    blend_amount = clamp(np.random.random()+from_edge)
                    pixel = (row*width)+i
                    draw_color = image_data[pixel]

                    image_data[pixel] = color_blend(base_color=draw_color, new_color=ice_color, amount=blend_amount)

    return image_data


def add_ice(image_data, ice=0.01):
    #TODO: Make patchy?
    ice_color = (255, 255, 255, 255)

    pixel_count = len(image_data)
    num_ice_pixels = clamp(int(ice * pixel_count), 0, 10000)
    for ice_pixel in xrange(0, num_ice_pixels):
        x = randint(0, pixel_count)
        blur_amount = .7 + np.random.random()/3
        image_data[x] = color_blend(image_data[x], ice_color, blur_amount)

    return image_data


def add_dust(image_data, dust_amount=10):
    percent_dust = float(dust_amount) / 2000
    pixel_count = len(image_data)
    num_dust_pixels = clamp(int(percent_dust * pixel_count), 0, 10000)

    white = (255, 255, 255, 255)
    for dust in xrange(0, num_dust_pixels):
        x = randint(0, pixel_count)
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