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


def dict_round_floats(source_dict={}, places=2):
    for key, val in source_dict.iteritems():
        if isinstance(val, float):
            source_dict[key] = round(val, places)

    return source_dict


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


def percent_range(value=1500, start_min=1000, start_max=2000, end_min=14, end_max=22):
    try:
        value = float(value)
    except ValueError:
        value = end_min + (np.random.random()*(end_max-end_min))

    start_pct = clamp(float(value - start_min) / float(start_max - start_min))
    return (float(start_pct) * float(end_max - end_min)) + float(end_min)


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
                break
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
    tag_manager[category] = list(set(existing_tags + tags))

    return tag_manager


def flatten_tags(tag_manager={}, max_tags=20, area=None):
    flattened = []
    if not area:
        for key, val in tag_manager.items():
            flattened += val
    else:
        if area in tag_manager:
            flattened += tag_manager[area]

    if len(flattened) > max_tags:
        flattened = np.random.choice(flattened, max_tags)
    tags = ",".join(flattened)
    return tags


VALUE_LOOKUPS = {'epic': 144.0, 'fantastic': 89.0, 'superb': 55.0, 'great': 34.0, 'good': 21.0, 'high': 13.0,
                 'fair': 8.0, 'average': 5.0, 'medium': 5.0, 'moderate': 5.0, 'mediocre': 3.0,
                 'low': 3.0, 'poor': 2.0, 'terrible': 1.0, 'tiny': 0.1, 'none': 0.0}


def word_from_value(value):
    word = 'tiny'
    value = float(value_of_variable(value))
    dist_to_upper = 1000

    for key, val in VALUE_LOOKUPS.iteritems():
        if abs(val-value) < dist_to_upper:
            word = key
            dist_to_upper = abs(val-value)
    return word


def value_of_variable(orig_var):
    val = orig_var
    was_changed = False
    if isinstance(val, basestring):
        var = val.lower().strip()
        if len(var) < 1:
            return var

        negative = False
        if var[0] == "-":
            negative = True
            var = var[1:]

        if var in VALUE_LOOKUPS:
            val = VALUE_LOOKUPS[var]
            was_changed = True
        else:
            val = var

        try:
            val = float(val)
            was_changed = True
        except ValueError:
            pass

        if negative and isinstance(val, float):
            val = -val

    else:
        try:
            val = float(orig_var)
            was_changed = True
        except ValueError:
            pass
        except TypeError:
            pass

    if not was_changed:
        val = orig_var

    return val


def extend(dict_source={}, *list_of_dict_updates):
    dict_new = dict_source.copy()
    for dict_update in list_of_dict_updates:
        if dict_update is not None:
            dict_new.update(dict_update)

    return dict_new


def set_val(dict_in, val, amount, use_words=False):
    if use_words:
        amount = word_from_value(amount)

    val_parts = val.split(".")
    if dict_in is None:
        dict_in = {}
    pointer = dict_in

    for idx, value in enumerate(val_parts[:-1]):
        if isinstance(pointer, dict):
            if value in pointer:
                pointer = pointer.get(value)
            else:
                pointer[value] = {}
                pointer = pointer.get(value)

    last = val_parts[-1]
    pointer[last] = amount


def get_val(dict_in, val='', default='', random_number=False, mid=0.3, min=0.0, max=120.0, weight=4,
            set_if_blank=True, use_words=False):
    if not isinstance(val, str):
        return dict_in

    val_parts = val.split(".")
    pointer = dict_in
    all_found = True
    for value in val_parts:
        if isinstance(pointer, dict) and value in pointer:
            pointer = pointer.get(value)
        else:
            all_found = False
            break

    if set_if_blank:
        reset = False
        if pointer is None:
            if random_number:
                pointer = min + rand_weighted(midpoint=mid, weight=weight) * (max-min)
                reset = True
            elif default is not None:
                pointer = default
                reset = True
        elif not all_found:
            pointer = default
            reset = True
        if reset:
            set_val(dict_in, val, amount=pointer)

    if isinstance(pointer, basestring):
        pointer = value_of_variable(pointer)
        if use_words:
            pointer = word_from_value(pointer)

    return pointer


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


def get_name_from_array(arr_list=list(), key='first', default=''):
    val = ''
    found = False
    for item in arr_list:
        if item.get("name", "") == key and item.get("value"):
            val = item.get("value")
            found = True
            break
    if not found:
        val = default

    return val


def get_formula_from_obj(obj={}, formula='A+,B--', min=None, max=None):
    val = 0.0

    for part in [part.strip() for part in formula.split(",")]:
        mod_num = part.count('+') - part.count('-')
        if mod_num is 0:
            mod_num = 1
        mod_name = part.replace('+', '').replace('-', '')

        if isinstance(obj, dict):
            if mod_name and mod_name in obj:
                amount = obj.get(mod_name) * mod_num
                val += float(amount)
        else:
            amount = get_name_from_array(obj, key=mod_name, default=0) * mod_num
            val += float(amount)

    if min is not None and max is not None:
        val = clamp(val, min, max)

    return val


def weighted_number(mid=0.3, max=120.0, weight=4):
    return rand_weighted(midpoint=mid, weight=weight)*max


def check_requirements(requirements, world_data):
    # Allow: [{concept:person,name:age,exceeds:20},{concept:world,name:magic,below:poor}]
    # Allow: 'magic > low, building has Church'
    # Allow: 'person.age > 20, world.magic < poor, person.business exists, person.siblings empty'
    # TODO: Work with 'family.*.profession sailor'

    if not requirements:
        return True

    checks = []
    if isinstance(requirements, basestring):
        if len(requirements) < 4:
            return True
        else:
            requirements = convert_string_to_req_object(requirements)

    if isinstance(requirements, list):
        for req in requirements:
            concept = req.get('concept', '')
            name = req.get('name', '')
            requirement = req.get('requirement', '')
            req_array = []
            if requirement and isinstance(requirement, list):
                req_array = requirement
            elif requirement and isinstance(requirement, basestring):
                req_array = requirement.split(".")
            elif concept and name:
                req_array = [concept, name]
            elif name:
                req_array = [name]

            r_is = req.get('is', '')
            r_exists = req.get('exists', '')
            r_has = req.get('has', '')
            r_exceeds = req.get('exceeds', '')
            r_empty = req.get('empty', '')
            r_below = req.get('below', '')
            r_gt = req.get('>', '')
            r_lt = req.get('<', '')

            if req_array:
                to_check = get_info_from_name_array(req_array, world_data)

                if not to_check:
                    if r_empty:
                        checks.append(True)
                    else:
                        checks.append(False)
                else:
                    if r_has and isinstance(to_check, list):
                        checks.append(r_has in to_check)  # TODO: Check for lower case and plural

                    elif r_exceeds or r_below or r_is or r_gt or r_lt or r_exists or r_empty:
                        try:
                            to_check = value_of_variable(to_check)
                            if r_exceeds:
                                r_exceeds = value_of_variable(r_exceeds)
                                checks.append(r_exceeds <= to_check)
                            if r_gt:
                                r_gt = value_of_variable(r_gt)
                                checks.append(r_gt < to_check)
                            if r_lt:
                                r_lt = value_of_variable(r_lt)
                                checks.append(r_lt > to_check)
                            if r_below:
                                r_below = value_of_variable(r_below)
                                r_below = float(r_below)
                                checks.append(r_below >= to_check)
                            if r_is:
                                try:
                                    temp = value_of_variable(r_is)
                                    r_is = float(temp)
                                    checks.append(r_is == to_check)
                                except ValueError:
                                    if isinstance(r_is, basestring) and isinstance(to_check, basestring):
                                        checks.append(r_is.lower() == to_check.lower())
                                    else:
                                        checks.append(r_is == to_check)

                            if r_exists:
                                checks.append(to_check is not False)

                        except Exception:
                            checks.append(False)
    else:
        return False

    is_valid = False
    if checks:
        is_valid = all(item for item in checks)

    return is_valid


def get_info_from_name_array(req_array, data_array, return_closest_match=False):
    pointer = data_array
    for req in req_array:
        if req.lower() == 'count' and isinstance(pointer, list):
            pointer = len(pointer)
        elif req.lower() == 'length' and isinstance(pointer, list):
            pointer = len(pointer)
        elif req in pointer:
            pointer = pointer.get(req)
        else:
            if return_closest_match:
                pass
            else:
                return False
    # TODO, Handle if arrays and * is passed in
    return pointer