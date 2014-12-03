import numpy as np

try:
    from django.http import HttpResponse
except:
    pass
import re
import random

# --- Mathy functions for planetary things ----------------
dice_parser = re.compile('[0-9]+[dD][0-9]+[e]{0,1}\s*[+-]{0,1}\s*[0-9]*(?![dD])')

VALUE_ARRAY = 'none tiny terrible poor mediocre average fair good great superb fantastic epic'.split(" ")


def rand_range(low=0, high=1, weight=1, avg=0.5):
    if low == 0 and high == 1:
        return rand_weighted(avg, weight)

    # convert numbers to 0 - 1
    num_range = high - low
    if num_range <= 0:
        num_range = 1
    new_avg = (avg - low) / num_range

    rand = rand_weighted(new_avg, weight)

    rand = low + (num_range * rand)
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
                    return rand_range(low * 0.5, low * 1.5, 3)
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
    for x in range(0, int(weight) - 1):
        tempnum = np.random.sample()
        if is_x_closer_to_mid_then_y(tempnum, closest, midpoint):
            closest = tempnum
    return closest


def is_x_closer_to_mid_then_y(x, y, mid):
    mid_to_x = abs(mid - x)
    mid_to_y = abs(mid - y)

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


def average_numbers_clamped(num_1=0, num_2=0):
    if num_1 and not num_2:
        return num_1
    if num_2 and not num_1:
        return num_2
    return float((num_1 + num_2) / 2)


def clamp(value, v_min=0, v_max=1):
    if value < v_min:
        return v_min
    if value > v_max:
        return v_max
    return value


def bigger_makes_smaller(start=5, start_min=0, start_max=8, end=5000, end_min=1, end_max=12000, tries_to_adjust=2):
    # Used to inversely correlate two variables within a range
    # For example, the bigger stars are usually younger (as they'd burn out quicker)
    # so if start is higher than average and end is higher than average, make end lower

    start_pct = clamp(float(start - start_min) / float(start_max - start_min), 0, 1)
    end_pct = clamp(float(end - end_min) / float(end_max - end_min), 0, 1)

    end_pct_guessed = rand_range(low=0, high=1, weight=tries_to_adjust, avg=(1 - start_pct))
    end_pct = average_numbers_clamped(end_pct, end_pct_guessed)

    new_end = (end_pct * (end_max - end_min)) + end_min
    return new_end


def bigger_makes_bigger(start=5, start_min=0, start_max=10, end=5, end_min=0, end_max=10, tries_to_adjust=2):
    start_pct = clamp((start - start_min) / (start_max - start_min))
    end_pct = clamp((end - end_min) / (end_max - end_min))

    end_pct_guessed = rand_range(low=0, high=1, weight=tries_to_adjust, avg=start_pct)
    end_pct = average_numbers_clamped(end_pct, end_pct_guessed)

    new_end = (end_pct * (end_max - end_min)) + end_min
    return new_end


def get_float_from_hash(options={}, var_name='', backup_val=0):
    try:
        val = float(options.get(var_name))
    except Exception:
        val = backup_val
    return val


def set_rand_seed(rand_seed=4815162342):
    try:
        rand_seed = float(rand_seed)
    except Exception as e:
        rand_seed = int(np.random.random() * 100000000)
    rand_seed_num = rand_seed
    if rand_seed < 1:
        rand_seed_num = rand_seed * 100000000

    try:
        rand_seed_num = int(rand_seed_num)
        np.random.seed(rand_seed_num)
    except ValueError as e:
        rand_seed_num = int(np.random.random() * 100000000)
        np.random.seed(rand_seed_num)

    return rand_seed_num


def randint(low, high, normalized_weighting=1):
    if low >= high:
        return high
    return np.random.randint(low, high)

    # TODO: Think about normalizing...
    # if normalized_weighting == 1 or high-low < 3:
    #     total = np.random.randint(low, high)
    # else:
    #     spread = high-low+1
    #     each = spread / normalized_weighting
    #     if each % 2 == 0: # It's even
    #         total = np.random.randint(low, low+each-1)
    #         total += np.random.randint(low, low+each) - 1
    #     else:


def parse_dice_text(text):
    matches = dice_parser.findall(text)
    for match in matches:
        val = str(roll_dice(match)) + " "
        text = text.replace(match, val)
    return text


def roll_dice(text='1d6', use_numpy=False):
    if not text or not isinstance(text, basestring):
        return text
    output = text
    d_spot = text.find('d')
    if d_spot > -1:
        num_dice = text[0:d_spot]
        dice_type = text[d_spot + 1:].strip()
        modifier_type = ''
        modifier_extra = ''

        if ' ' in dice_type:
            modifier_pos = dice_type.find(' ')
            dice_front = dice_type[0:modifier_pos].strip()
            modifier_extra = dice_type[modifier_pos:].strip()
            dice_type = dice_front + modifier_extra

        if '+' in dice_type:
            modifier_pos = dice_type.find('+')
            dice_front = dice_type[0:modifier_pos]
            modifier_extra = dice_type[modifier_pos + 1:].strip()
            dice_type = dice_front
            modifier_type = "+"
        elif '-' in dice_type:
            modifier_pos = dice_type.find('-')
            dice_front = dice_type[0:modifier_pos]
            modifier_extra = dice_type[modifier_pos + 1:].strip()
            dice_type = dice_front
            modifier_type = "-"

        num_dice = int(num_dice)
        dice_type = int(dice_type)
        result = 0
        rolls = []
        if num_dice > 0:
            for roll_num in range(0, num_dice):
                if use_numpy:
                    roll = np.random.randint(1, dice_type)
                else:
                    roll = random.randint(1, dice_type)
                rolls.append(roll)
            result += sum(rolls)

        if modifier_type:
            modifier_extra = int(modifier_extra)
            if modifier_type == "+":
                result += modifier_extra
            if modifier_type == "-":
                result -= modifier_extra

        output = result

    return output


def expand_array_to_16(source_array):
    # Take in any array, and expand it to 16 spots
    in_len = len(source_array)
    if in_len > 16:
        return source_array[:16]

    outs = [
        '',
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0',
        '0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1',
        '0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2',
        '0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3',
        '0,0,0,1,1,1,2,2,2,2,3,3,3,4,4,4',
        '0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5',
        '0,0,1,1,2,2,2,3,3,3,4,4,5,5,6,6',
        '0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7',
        '0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8',
        '0,1,2,2,3,3,4,4,5,5,6,6,7,7,8,9',
        '0,1,2,3,3,4,4,5,5,6,6,7,7,8,9,10',
        '0,1,2,3,3,4,4,5,5,6,6,7,8,9,10,11',
        '0,1,2,3,4,5,5,6,6,7,7,8,9,10,11,12',
        '0,1,2,3,4,5,6,6,7,7,8,9,10,11,12,13',
        '0,1,2,3,4,5,6,7,7,8,9,10,11,12,13,14',
        '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
    ]
    matched = outs[in_len].split(",")
    out = ['Normal'] * 16
    for idx, p in enumerate(matched):
        if p:
            val = source_array[int(p)]
            if val:
                out[idx] = val

    return out


def add_or_merge_dicts(dict1, dict2):
    d = {}
    for k, v in dict1.items():
        try:
            d[k] = float(v)
        except ValueError:
            d[k] = v

    for k, v in dict2.items():
        if k in d or k.lower() in d:
            try:
                v1 = float(d[k])
                v2 = float(v)
                d[k] = v1 + v2
            except ValueError:
                d[k] = str(d[k]) + "," + str(v)
        else:
            d[k] = v
    return d


def add_or_increment_dict_val(d, key, val):
    if isinstance(d, tuple):
        raise Exception("Tuple Exception inside of 'dict_add' method: " + str(d))

    if isinstance(d, list):
        found = False
        for d_item in d:
            if d_item.get("name", "") == key and d_item.get("value"):
                existing_val = d_item.get("value")
                try:
                    v1 = float(existing_val)
                    v2 = float(val)
                    d_item["name"] = v1 + v2
                except ValueError:
                    d_item["name"] = str(existing_val) + "," + str(val)
            found = True
        if not found:
            try:
                val = float(val)
            except ValueError:
                pass
            d.append({"name": key, "value": val})
    else:
        if key in d or key.lower() in d:
            try:
                v1 = float(d[key])
                v2 = float(val)
                d[key] = v1 + v2
            except ValueError:
                d[key] = str(d[key]) + "," + str(val)
        else:
            if isinstance(key, basestring):
                d[key] = val
            else:
                pass

    return d


def add_tags(tag_manager, category, *tag_list):
    tag_array = []
    for tag_words in tag_list:
        if not tag_words:
            continue
        if isinstance(tag_words, basestring):
            tag_array = tag_words.split(",")
        elif isinstance(tag_words, dict):
            for tag in tag_words.items():
                tag_array.append(tag[0])

    tags = [tag.lower().strip() for tag in tag_array if tag]

    existing_tags = tag_manager.get(category, [])
    tag_manager[category] = existing_tags + tags

    return tag_manager


def flatten_tags(tag_manager={}, max_tags=20):
    flattened = []
    for key, val in tag_manager.items():
        flattened += val

    if len(flattened) > max_tags:
        flattened = np.random.choice(flattened, max_tags)
    tags = ",".join(flattened)
    return tags


def value_of_variable(var):
    val = var
    if isinstance(var, basestring):
        var = var.lower().strip()
        if len(var) < 1:
            return var

        negative = False

        if var[0] == "-":
            negative = True
            var = var[1:]

        lookups = {'epic': 144.0, 'fantastic': 89.0, 'superb': 55.0, 'great': 34.0, 'good': 21.0, 'high': 13.0,
                   'fair': 8.0, 'average': 5.0, 'medium': 5.0, 'moderate': 5.0, 'mediocre': 3.0,
                   'low': 3.0, 'poor': 2.0, 'terrible': 1.0, 'tiny': 0.1, 'none': 0.0}
        if var in lookups:
            val = lookups[var]
        else:
            val = var

        try:
            val = float(val)
        except ValueError:
            pass

        if negative and isinstance(val, float):
            val = -val

    else:
        try:
            val = float(var)
        except ValueError:
            pass
        except TypeError:
            pass

    return val


def convert_string_to_properties_object(props):
    # lifespan +2, cost = poor, mother.profession = teacher, father.leaves, blessings
    properties = {}
    props = str(props)

    if len(props) < 3:
        return {}

    props_split = props.split(",")
    props_split = [req.strip() for req in props_split]

    for p in props_split:
        key = ""
        val = ""
        if "=" in p:
            p_parts = p.split("=")
            if len(p_parts) > 1:
                key = p_parts[0].strip()
                val = p_parts[1].strip()
        elif " " in p:
            # check for ending in number
            p_parts = p.rsplit(' ', 1)
            if len(p_parts) > 1:
                key = p_parts[0].strip()
                val = p_parts[1].strip()
        else:
            key = p
            val = 'exists'

        if key and val:
            try:
                val = float(val)
            except ValueError:
                pass
            key = key.lower()
            val = value_of_variable(val)
            if key in properties:
                old_val = properties[key]
                if isinstance(old_val, float) and isinstance(val, float):
                    val += old_val
                else:
                    val = str(old_val) + ", " + str(val)
            properties[key] = val

    return properties


def convert_string_to_req_object(requirements):
    reqs = str(requirements)

    if len(reqs) < 3:
        return []

    reqs = reqs.split(",")
    reqs = [req.strip() for req in reqs]

    output = []
    for req in reqs:
        if " >= " in req:
            req_part = req.split(" >= ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "exceeds": req_part[1].strip()})

        elif " <= " in req:
            req_part = req.split(" <= ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "below": req_part[1].strip()})

        elif " > " in req:
            req_part = req.split(" > ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), ">": req_part[1].strip()})

        elif " < " in req:
            req_part = req.split(" < ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "<": req_part[1].strip()})

        elif " has " in req:  # Check that it's not in quotes
            req_part = req.split(" has ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "has": req_part[1].strip()})

        elif " = " in req:
            req_part = req.split(" = ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "is": req_part[1].strip()})

        elif " == " in req:
            req_part = req.split(" == ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "is": req_part[1].strip()})

        elif " is " in req:  # TODO: Check that it's not in quotes
            req_part = req.split(" is ")
            if len(req_part) == 2:
                output.append({"requirement": req_part[0].strip(), "is": req_part[1].strip()})

        elif req.endswith(" none"):
            req_part = req.split(" none")
            output.append({"requirement": req_part[0].strip(), "empty": req_part[0].strip()})

        elif req.endswith(" empty"):
            req_part = req.split(" empty")
            output.append({"requirement": req_part[0].strip(), "empty": req_part[0].strip()})

        elif req.endswith(" doesn't exist"):
            req_part = req.split(" doesn't exist")
            output.append({"requirement": req_part[0].strip(), "empty": req_part[0].strip()})

        elif req.endswith(" exists"):
            req_part = req.split(" exists")
            output.append({"requirement": req_part[0].strip(), "exists": req_part[0].strip()})

        elif req.endswith(" exist"):
            req_part = req.split(" exist")
            output.append({"requirement": req_part[0].strip(), "exists": req_part[0].strip()})

        else:  # Assume that it's an exists check
            output.append({"requirement": req.strip(), "exists": req.strip()})

    return output

