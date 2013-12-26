from django.http import HttpResponse
import numpy as np
from procyon.starsystemmaker.math_helpers import *
import struct
from noise import snoise2

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

    rand_seed = float(request.GET.get('rand_seed', np.random.random()))
    width = height = int(float(request.GET.get('size', 256) or 256))
    color_range = int(float(request.GET.get('color_range', 5) or 5))
    ice_n = float(request.GET.get('ice_north_pole', .03) or .03)
    ice_s = float(request.GET.get('ice_south_pole', .03) or .03)
    ice_total = float(request.GET.get('ice_total', .02) or .02)
    base_color = str(request.GET.get('base_color', '') or '')
    surface_solidity = float(request.GET.get('surface_solidity', 0) or 0)
    craterization = float(request.GET.get('craterization', .02) or .02)
    atmosphere_dust_amount = int(float(request.GET.get('atmosphere_dust_amount', 3)))
    minerals = str(request.GET.get('minerals_specific', '') or 'Carbon Iron Hydrogen Nitrogen Oxygen')

    #TODO: Build multiple image and data layers for each planetoid, all related
    #TODO: Allow user to request just one specific layer (ice, dust, atmosphere, surface, minerals, water), or (surface, air) or all combined as one
    #TODO: Cache each of these images once drawn
    #TODO: Allow passing in system # and planet # (and maybe moon #) to generate the images instead of with all vars

    #TODO: Use Blur?
    blur_radius = 1

    set_rand_seed(rand_seed)

    surface_color = get_surface_color(base_color=base_color,  minerals=minerals)

    #Set base color
    image_data = []
    for i in range(0, width*height):
        image_data.append(surface_color)

    #Add gas streaks
    if surface_solidity < .9:
        add_streaks(image_data, height=height, width=width, color_range=color_range, color=surface_color)

    #Add Ice Caps on north and south poles
    if ice_n > 0 or ice_s > 0:
        image_data = add_icecaps(image_data, ice_n=ice_n, ice_s=ice_s, height=height, width=width)
    #Add Ice
    if ice_total:
        image_data = add_ice(image_data, percent_ice=ice_total)
    # Add Dust
    # if atmosphere_dust_amount > 0:
    #     image_data = add_dust(image_data, dust_amount=atmosphere_dust_amount)
    #Blur
    if blur_radius > 0:
        image_data = blur_image(image_data, height=height, width=width, radius=blur_radius)


    #Add Noise
    noise_map = get_noise(width=width, height=height)
    #TODO: Make this tileable perlin noise.
    #TODO: Make a function to generate different types of noise, some for blending colors, others for contrast, etc.
    for i in range(0, len(noise_map)):
        col = image_data[i]
        image_data[i] = ((col[0]+noise_map[i])/2, (col[1]+noise_map[i])/2, (col[2]+noise_map[i])/2, 255)


    im = Image.new('RGBA', (width, height))
    im.putdata(image_data)

    #Add Craters
    if craterization > 0:
        im = add_craters(im, craterization=craterization, width=width, height=height)


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


def add_craters(image, craterization=1.0, width=256, height=256):
    craterization = int(craterization*20)
    CRATER_VARIANCE = 2
    crater_size = int(float(width) / 20)

    foreground = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(foreground)

    for c in range(0, craterization):
        x = randint(10, width-10)
        y = randint(10, height-10)
        radius = randint(int(crater_size/10), crater_size)
        x_left = x-radius+randint(-CRATER_VARIANCE, CRATER_VARIANCE)
        x_right = x+radius+randint(-CRATER_VARIANCE, CRATER_VARIANCE)
        y_left = y-radius+randint(-CRATER_VARIANCE, CRATER_VARIANCE)
        y_right = y+radius+randint(-CRATER_VARIANCE, CRATER_VARIANCE)

        #TODO: Rotation?

        crater_rim_width = randint(0, 2)
        crater_rim_basewidth = randint(0, 3)

        crater_rim_brightness = randint(128, 200)
        bright = (crater_rim_brightness, crater_rim_brightness, crater_rim_brightness, crater_rim_brightness)
        dark = (0, 0, 0, randint(0, 128))
        mid = (0, 0, 0, randint(80, 160))

        offset = crater_rim_basewidth
        draw.ellipse((x_left-offset, y_left-offset, x_right+offset, y_right+offset), fill=dark)

        offset = crater_rim_width
        draw.ellipse((x_left-offset, y_left-offset, x_right+offset, y_right+offset), fill=bright)

        draw.ellipse((x_left, y_left, x_right, y_right), fill=bright)

        offset = -crater_rim_width
        draw.ellipse((x_left-offset, y_left-offset, x_right+offset, y_right+offset), fill=mid)

        offset = -crater_rim_width-1
        draw.ellipse((x_left-offset, y_left-offset, x_right+offset, y_right+offset), fill=dark)

    image_new = Image.composite(foreground, image, foreground)
    return image_new


def add_ice(image_data, percent_ice=0.01):
    #TODO: Make patchy?
    ice_color = (255, 255, 255, 255)

    num_pixels = len(image_data)
    pixels_to_ice = range(0, num_pixels)
    np.random.shuffle(pixels_to_ice)

    num_to_ice = int(percent_ice * num_pixels)
    for ice in pixels_to_ice[:num_to_ice]:
        blur_amount = .7 + np.random.random()/3
        image_data[ice] = color_blend(image_data[ice], ice_color, blur_amount)

    return image_data


def add_dust(image_data, dust_amount=10):
    dust_color = (128, 128, 128, 128)
    percent_dust = clamp(float(dust_amount) / 2000)

    num_pixels = len(image_data)
    pixels_to_dust = range(0, num_pixels)
    np.random.shuffle(pixels_to_dust)

    num_to_dust = int(percent_dust * num_pixels)
    for dust in pixels_to_dust[:num_to_dust]:
        blur_amount = .3 + np.random.random()/3
        image_data[dust] = color_blend(image_data[dust], dust_color, blur_amount)

    return image_data


def add_streaks(image_data, height=256, width=256, color_range=5, color=(255, 0, 0, 255)):

    for row in xrange(0, height):
        rand = (randint(-color_range, color_range), randint(-color_range, color_range), randint(-color_range, color_range), 0)
        draw_color = color = tuple(map(sum, zip(color, rand)))
        for i in range(0, width):
            pixel = (row*width) + i
            image_data[pixel] = draw_color

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


def get_noise(octaves=42, width=256, height=256):
    freq = 16.0 * octaves
    output = []

    for y in range(height):
        for x in range(width):
            output.append(int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0))
    return output


def get_surface_color(base_color='ff0000',  minerals='Carbon Iron'):

    #TODO: Determine color based on minerals and atmosphere
    if base_color:
        color = color_array_from_hex(color=base_color)
    else:
        color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)

    return color


def build_color_layer(color='ff0000', width=256, height=256, rand_seed=42):
    image_data = []
    for i in range(0, width*height):
        image_data.append(color)
#Add noise with rand_seed

    return image_data


def color_array_from_hex(color='ff0000'):
    base_color = color.replace("%23", "")
    rgb_str = base_color.replace("#", "")

    color = struct.unpack('BBB', rgb_str.decode('hex'))
    color = (color[0], color[1], color[2], 255)

    return color