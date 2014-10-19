from django.http import HttpResponse
import numpy as np
from procyon.starsystemmaker.math_helpers import *
import struct
import noise
import math

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


LAYER_TYPES = "minerals surface craters icecaps ice atmosphere noise"


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

    #TODO: Allow user to request just one specific layer (ice, dust, atmosphere, surface, minerals, water), or (surface, air) or all combined as one
    #TODO: Cache each of these images once drawn
    #TODO: Allow passing in system # and planet # (and maybe moon #) to generate the images instead of with all vars

    #Build the random starting variables
    set_rand_seed(rand_seed)

    #Parse out the colors of the planet
    surface_colors = colors_from_minerals(base_color=base_color,  minerals=minerals)

    #Create the image_layers
    image_layers = build_initial_image_layers()

    #Add gas streaks
    if surface_solidity < .9:
        image_layers['atmosphere'] = image_layer_streaks(height=height, width=width, c_range=color_range, colors=surface_colors)
    else:
        image_layers['surface'] = image_layer_surface(colors=surface_colors, width=width, height=height)

    #Add Ice Caps on north and south poles
    if ice_n > 0 or ice_s > 0:
        image_layers['icecaps'] = image_layer_icecaps(ice_n=ice_n, ice_s=ice_s, height=height, width=width)
    #Add Ice
    if ice_total:
        image_layers['ice'] = image_layer_ice(percent_ice=ice_total, height=height, width=width)
    # Add Dust
    if atmosphere_dust_amount > 0:
        image_layers['dust'] = image_layer_dust(dust_amount=atmosphere_dust_amount, height=height, width=width)

    #Add Craters
    if craterization > 0:
        image_layers['craters'] = image_layer_craters(craterization=craterization, width=width, height=height)

    #NOTE: Good land with white_min=-.25, white_range=10
    image_layers['noise'] = image_layer_noise(width=width, height=height, white_min=0, white_range=.2)

    return response_from_image_layers(width=width, height=height, image_layers=image_layers, image_format=image_format)


# ==== Image Building Functions ====
def image_layer_icecaps(ice_n=0.01, ice_s=0.01, height=256, width=256, octaves=64):
    image_data = []
    for i in range(0, width*height):
        image_data.append((0, 0, 0, 0))

    freq = 2.0 * octaves

    for row in range(0, height):
        from_edge = 0
        if row <= (height*ice_n):
            from_edge = ((height*ice_n)-row) / (height*ice_n)
        elif row >= height-(height*ice_s):
            from_edge = (row - (height-(height*ice_s))) / (height*ice_s)

        if from_edge > 0:
            for col in range(0, width):
                noise1 = noise.snoise2(col / freq, row / freq, octaves)
                noise2 = from_edge * 2
                noisenum = clamp(noise1 * noise2 + noise2)
                if noisenum > .5:
                    pixel = (row*width)+col
                    image_data[pixel] = (255, 255, 255, int(noisenum * 255.0))

    return image_data


def image_layer_craters(craterization=1.0, width=256, height=256):
    craterization = int(craterization*20)
    CRATER_VARIANCE = 2
    crater_size = int(float(width) / 20)

    foreground = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(foreground)

    for c in range(0, craterization):
        radius = randint(int(crater_size/10), crater_size)
        x = randint(radius+1, width-radius-1)
        y = randint(radius+1, height-radius-1)
        x_left = x-radius+randint(-CRATER_VARIANCE, CRATER_VARIANCE)
        x_right = x+radius+randint(-CRATER_VARIANCE, CRATER_VARIANCE)
        y_left = y-radius+randint(-CRATER_VARIANCE, CRATER_VARIANCE)
        y_right = y+radius+randint(-CRATER_VARIANCE, CRATER_VARIANCE)

        #TODO: Rotation?

        crater_rim_width = randint(0, 2)
        crater_rim_basewidth = randint(0, 3)

        crater_rim_brightness = randint(128, 120)
        bright = (crater_rim_brightness, crater_rim_brightness, crater_rim_brightness, crater_rim_brightness)
        dark = (0, 0, 0, randint(0, 80))
        mid = (0, 0, 0, randint(80, 100))

        offset = crater_rim_basewidth
        draw.ellipse((x_left-offset, y_left-offset, x_right+offset, y_right+offset), fill=dark)

        offset = crater_rim_width
        draw.ellipse((x_left-offset, y_left-offset, x_right+offset, y_right+offset), fill=bright)

        draw.ellipse((x_left, y_left, x_right, y_right), fill=bright)

        offset = -crater_rim_width
        draw.ellipse((x_left-offset, y_left-offset, x_right+offset, y_right+offset), fill=mid)

        offset = -crater_rim_width-1
        draw.ellipse((x_left-offset, y_left-offset, x_right+offset, y_right+offset), fill=dark)

    # image_new = Image.composite(foreground, image, foreground)
    return foreground


def image_layer_ice(percent_ice=0.01, width=256, height=256):
    #TODO: Make patchy using voronoi cells?

    num_pixels = width*height
    pixels_to_ice = range(0, num_pixels)
    np.random.shuffle(pixels_to_ice)  #TODO: Convert to noise and/or nrands(pixels_to_ice, dims=2)

    image_data = []
    for i in range(0, num_pixels):
        image_data.append((0, 0, 0, 0))

    num_to_ice = int(percent_ice * num_pixels)
    for ice in pixels_to_ice[:num_to_ice]:
        blur_amount = int((.7 + np.random.random()/3) * 255)
        image_data[ice] = (255, 255, 255, blur_amount)

    return image_data


def image_layer_dust(dust_amount=10, height=256, width=256):
    percent_dust = clamp(float(dust_amount) / 2000)

    num_pixels = height*width
    image_data = []
    for i in range(0, num_pixels):
        image_data.append((0, 0, 0, 0))

    pixels_to_dust = range(0, num_pixels)
    np.random.shuffle(pixels_to_dust)

    num_to_dust = int(percent_dust * num_pixels)
    for dust in pixels_to_dust[:num_to_dust]:
        blur_amount = int((.3 + np.random.random()/3)*255)
        image_data[dust] = (128, 128, 128, blur_amount)

    return image_data


def image_layer_streaks(height=256, width=256, c_range=5, colors=list()):

    len_colors = len(colors)
    if colors and len_colors > 0:
        color = colors[0]
    else:
        color = (255, 0, 0, 255)

    image_data = []
    for row in range(0, height):
        rand = (randint(-c_range, c_range), randint(-c_range, c_range), randint(-c_range, c_range), 0)
        if np.random.random() < .2:
            new_color = colors[randint(0, len_colors)]
            color = color_blend(color, new_color, 0.2)
        draw_color = color = tuple(map(sum, zip(color, rand)))
        for i in range(0, width):
            image_data.append(draw_color)

    return image_data


def image_layer_surface(width=256, height=256, colors=list()):

    len_colors = len(colors)
    if colors and len(colors) > 0:
        color = colors[0]
    else:
        color = (255, 0, 0, 255)

    image_data = []
    for i in range(0, width*height):
        # if np.random.random() < .01:
        #     new_color = colors[randint(0, len_colors)]
        #     color = color_blend(color, new_color, 0.05)

        image_data.append(color)
    return image_data


def image_layer_noise(width=256, height=256, white_min=0.5, white_range=None, octave=5):
    #Derived from http://gamedev.stackexchange.com/questions/23625/how-do-you-generate-tileable-perlin-noise

    #TODO: This is taking too long to calculate for larger images. Pre-generate and prestore?

    perm = range(width)
    np.random.shuffle(perm)

    perm += perm
    dirs = [(math.cos(a * 2.0 * math.pi / width), math.sin(a * 2.0 * math.pi / height)) for a in range(width)]

    def simplex_noise(x, y, per):
        def surflet(grid_x, grid_y):
            dist_x, dist_y = abs(x-grid_x), abs(y-grid_y)
            poly_x = 1 - 6*dist_x**5 + 15*dist_x**4 - 10*dist_x**3
            poly_y = 1 - 6*dist_y**5 + 15*dist_y**4 - 10*dist_y**3
            hashed = perm[perm[int(grid_x) % per] + int(grid_y) % per]
            grad = (x-grid_x)*dirs[hashed][0] + (y-grid_y)*dirs[hashed][1]
            return poly_x * poly_y * grad
        int_x, int_y = int(x), int(y)
        return (surflet(int_x+0, int_y+0) + surflet(int_x+1, int_y+0) +
                surflet(int_x+0, int_y+1) + surflet(int_x+1, int_y+1))

    def fractal_brownian(x, y, per, octaves):
        value = 0
        for o in range(octaves):
            value += 0.5**o * simplex_noise(x*2**o, y*2**o, per*2**o)
        return value

    size, freq, data = width, 1/32.0, []
    white_min *= 255.0
    if not white_range:
        white_range = 1-white_min
    white_range *= 255.0

    for row in range(size):
        for col in range(size):
            val = fractal_brownian(col*freq, row*freq, int(size*freq), octave)
            data.append((255, 255, 255, int(val*white_range + white_min)))

    return data


#==== Supporting function ====
def build_initial_image_layers():
    #Build multiple layers of images that will be combined into the final image
    image_layers = dict()
    for layer_name in LAYER_TYPES.split():
        image_layers[layer_name] = []
    return image_layers


def get_noise(octaves=42, width=256, height=256):
    freq = 16.0 * octaves
    output = []

    for y in range(height):
        for x in range(width):
            output.append(int(noise.snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0))
    return output


def response_from_image_layers(width=256, height=256, image_layers=None, image_format="PNG"):
    if not image_layers:
        image_layers = dict()

    im = Image.new('RGBA', (width, height))
    im = merge_image_layers(im, image_layers)

    mime = "image/png"
    if image_format == "JPEG":
        mime = "image/jpeg"
    response = HttpResponse(mimetype=mime)
    im.save(response, image_format)

    return response


def merge_image_layers(im, image_layers):
    if not image_layers:
        image_layers = dict()

    width, height = im.size

    for layer_name in LAYER_TYPES.split():
        layer = image_layers[layer_name]
        if type(layer) == list:
            if len(layer) == width*height:
                #It's a list of pixels, imagify and compose together
                foreground = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                foreground.putdata(layer)
                im = Image.composite(foreground, im, foreground)
        else:
            im = Image.composite(layer, im, layer)
    return im


def colors_from_minerals(base_color='ff0000',  minerals='Carbon Iron'):
    #Determine color based on minerals

    mineral_list = [
        {'name': 'Iron', 'element': 'Fe', 'col': '8d6039'},
        {'name': 'Carbon', 'element': 'C', 'col': '888888'},
        {'name': 'Lithium', 'element': 'Li', 'col': 'ff0000'},
        {'name': 'Strontium', 'element': 'Sr', 'col': 'ff0000'},
        {'name': 'Calcium', 'element': 'Ca', 'col': 'ff6666'},
        {'name': 'Sodium', 'element': 'Na', 'col': 'ffff00'},
        {'name': 'Barium', 'element': 'Ba', 'col': '99ff33'},
        {'name': 'Molybdenum', 'element': 'Mo', 'col': '99ff33'},
        {'name': 'Boron', 'element': 'B', 'col': '66ff66'},
        {'name': 'Thallium', 'element': 'Tl', 'col': '66ff66'},
        {'name': 'Phosphorus', 'element': 'P', 'col': '66ffcc'},
        {'name': 'Zinc', 'element': 'Zn', 'col': '66ffcc'},
        {'name': 'Tellurium', 'element': 'Te', 'col': 'ccffcc'},
        {'name': 'Antimony', 'element': 'Sb', 'col': 'ccffcc'},
        {'name': 'Lead', 'element': 'Pb', 'col': 'ccffcc'},
        {'name': 'Copper', 'element': 'Cu', 'col': '0066ff'},
        {'name': 'Copper-ammonium', 'element': 'CuNH', 'col': '0000ff'},
        {'name': 'Selenium', 'element': 'Se', 'col': '0066ff'},
        {'name': 'Indium', 'element': 'In', 'col': '0066ff'},
        {'name': 'Arsenic', 'element': 'As', 'col': '0066ff'},
        {'name': 'Potassium', 'element': 'K', 'col': 'ffccff'},
        {'name': 'Rubidium', 'element': 'Rb', 'col': 'ffccff'},
        {'name': 'Cesium', 'element': 'Cs', 'col': 'ffccff'},
    ]
    if base_color:
        color = color_array_from_hex(color=base_color)
    else:
        color = (randint(0, 255), randint(0, 255), randint(0, 255), 255)

    weighting = 1.0
    color_list = []
    for mineral_text in minerals.split():
        t = mineral_text.split(":")
        mineral = t[0] or "carbon"
        weighting /= 2
        mineral_weighting = weighting #TODO: Use this for random weighting?
        if len(t) > 1:
            mineral_weighting = t[1]

        for min_option in mineral_list:
            name = min_option.get('name')
            symbol = min_option.get('symbol')
            col = min_option.get('col')

            if name and name.lower() == mineral.lower():
                col = color_array_from_hex(col)
                color_list.append(col)
                break
            elif symbol and symbol.lower() == mineral.lower():
                col = color_array_from_hex(col)
                color_list.append(col)
                break

    color_list.append(color)

    return color_list


def color_blend(base_color=(255, 255, 255, 255), new_color=(0, 0, 255, 255), amount=.2):
    r = (base_color[0]*(1-amount)) + (new_color[0]*amount)
    g = (base_color[1]*(1-amount)) + (new_color[1]*amount)
    b = (base_color[2]*(1-amount)) + (new_color[2]*amount)
    a = (base_color[3]*(1-amount)) + (new_color[3]*amount)

    return int(r), int(g), int(b), int(a)


def color_array_from_hex(color='ff0000'):
    base_color = color.replace("%23", "")
    rgb_str = base_color.replace("#", "")

    color = struct.unpack('BBB', rgb_str.decode('hex'))
    color = (color[0], color[1], color[2], 255)

    return color


def image_with_random_color(image_format="PNG"):
    im = Image.new('RGBA', (256, 256), (randint(0, 255), randint(0, 255), randint(0, 255), 255))

    mime = "image/png"
    if image_format == "JPEG":
        mime = "image/jpeg"

    response = HttpResponse(mimetype=mime)
    im.save(response, image_format)
    return response


# ==== Not used ====

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


def image_layer_noise_old(width=256, height=256, white_min=0.5, white_range=None):
    #Add Noise
    #TODO: Make a function to generate different types of noise, some for blending colors, others for contrast, etc.

    x_start = 0
    y_start = 0

    # freq = 32.0 * octaves
    freq = width
    white_min *= 255.0
    if not white_range:
        white_range = 1-white_min
    white_range *= 255.0

    octaves = 42
    period = 128.0

    image_data = []
    for y in range(height):
        for x in range(width):
#            noisenum = noise.snoise2(x_start + (x / freq), y_start + (y / freq), octaves)
            noisenum = noise.snoise2(x/period, y/period, octaves)

            # noisenum = pnoise2(x * 16.0 / width, y * 16.0 / width, octaves=64, repeatx=64.0, repeaty=64.0)
            image_data.append((255, 255, 255, int(noisenum * white_range + white_min)))

    return image_data

