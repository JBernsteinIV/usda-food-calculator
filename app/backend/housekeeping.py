# Housekeeping function to group together nutrients that are similar to each other.
# For example, 'Lysine' and 'Methionine' are both amino acids.
# This is also performed so that the data is better structured instead of being a one-dimensional array.
#from inspect import currentframe

def group_by_type(nutrient, structured_nutrient=None):
    if structured_nutrient is None:
        structured_nutrient = {
            'id'           : 0,
            'measurement'  : '100 g',
            'description'  : '',
            'Calories'     : '0.0 kcal',
            'Protein'      : '0.0 g',
            'Aminos'       : {
                'essential'    : [],
                'nonessential' : []
            },
            'Carbohydrates': '0.0 g',
            'Fiber'        : '0.0 g',
            'Sugars'       : [],
            'Fat'          : '0.0 g',
            'Cholesterol'  : '0.0 g',
            'Lipids'       : {
                'Monounsaturated' : '0.0 g',
                'Polyunsaturated' : '0.0 g',
                'Saturated'       : '0.0 g',
                'Trans'           : '0.0 g',
                'Omega-3s'        : []
            },
            'Water'        : '0.0 g',
            'Minerals'     : [],
            'Vitamins'     : []
        }
    # Destructure the amount and unit into a single string.
    name   = nutrient['name'].lower()
    amount = { 'amount' : nutrient['amount'], 'unit' : nutrient['unit'] }
    if 'energy' in name:
        structured_nutrient['Calories'] = amount
    elif 'protein' in name:
        structured_nutrient['Protein'] = amount
    elif 'carbohydrate' in name:
        structured_nutrient['Carbohydrates'] = amount
    elif 'total lipid (fat)' in name:
        structured_nutrient['Fat'] = amount
    elif 'caffeine' in name:
        structured_nutrient['Caffeine'] = amount
    elif 'water' in name:
        structured_nutrient['Water'] = amount
    elif 'fiber' in name:
        structured_nutrient['Fiber'] = amount
    elif 'cholesterol' in name:
        structured_nutrient['Cholesterol'] = amount
    else:
        obj = {
            'name'  : name,
            'amount': nutrient['amount'],
            'unit'  : nutrient['unit']
        }
        obj['name'] = rename(name)

        if name.endswith('in') or 'vitamin' in name or 'pantothenic' in name or 'folate' in name or 'folic acid' in name:
            structured_nutrient['Vitamins'].append(obj)
        elif name.endswith('ine') or name.endswith('phan') or name.endswith('acid') or 'glutamate' in name or 'asparate' in name:
            if name in ['histidine', 'isoleucine', 'leucine', 'lysine', 'methionine', 'phenylalanine', 'threonine', 'tryptophan', 'valine']:
                structured_nutrient['Aminos']['essential'].append(obj)
            else:
                structured_nutrient['Aminos']['nonessential'].append(obj)
        elif name.endswith('ose') or 'sugars' in name:
            structured_nutrient['Sugars'].append(obj)
        elif 'fat' in name or name.endswith('a)'):
            if obj['name'].endswith('acid)'):
                structured_nutrient['Lipids']['Omega-3s'].append(obj)
            elif 'mono' in name:
                structured_nutrient['Lipids']['Monounsaturated'] = obj
            elif 'poly' in name:
                structured_nutrient['Lipids']['Polyunsaturated'] = obj
            elif 'trans' in name:
                structured_nutrient['Lipids']['Trans']           = obj
            else:
                structured_nutrient['Lipids']['Saturated']       = obj
        else:
            structured_nutrient['Minerals'].append(obj)
    return structured_nutrient

# Rename some of the keys so they are more clear for a generalized audience.
def rename(name):
    if '(ala)' in name:
        new_name = 'ALA (alpha-linoleic acid)'
    elif '(epa)' in name:
        new_name = 'EPA (eicosapentaenoic acid)'
    elif '(dha)' in name:
        new_name = 'DHA (docosahexaenoic acid)'
    elif 'sugars' in name:
        new_name = 'Total sugar'
    elif 'thiamin' in name:
        new_name = 'Vitamin B1 (Thiamin)'
    elif 'riboflavin' in name:
        new_name = 'Vitamin B2 (Riboflavin)'
    elif 'niacin' in name:
        new_name = 'Vitamin B3 (Niacin)'
    elif 'pantothenic' in name:
        new_name = 'Vitamin B5 (Pantothenic Acid)'
    elif 'biotin' in name or 'b-7' in name:
        new_name = 'Vitamin B7 (Biotin)'
    elif 'fol' in name:
        new_name = 'Vitamin B9 (Folic Acid)'
    # These next ones are mainly just to conform all vitamins to being capitalized for consistency.
    elif 'b-6' in name:
        new_name = 'Vitamin B6'
    elif 'b-12' in name:
        new_name = 'Vitamin B12'
    elif 'vitamin c' in name:
        new_name = 'Vitamin C'
    elif 'vitamin d' in name:
        new_name = 'Vitamin D'
    elif 'vitamin e' in name:
        new_name = 'Vitamin E'
    elif 'vitamin k' in name:
        new_name = 'Vitamin K'
    # This is just to handle renaming a few oddball entries (e.g. Avocado Oil is 'oil, avocado').
    # Or e.g. "Avocados, raw, all commercial varities".
    else:
        new_name = name
    return new_name

""" Parse the user's request for keywords. """

# Check if the keyword is a unit of measurement.
def is_unit_of_measurement(request):
    valid_measurements = [
        'teaspoon', 'tsp', 'tsp.',
        'tablespoon', 'tbsp', 'T', 'tbsp.',
        'cup', 'cups',
        'ounce', 'ounces', 'oz',
        'fluid ounce', 'fl',
        'pound', 'pounds', 'lbs',
        'gram', 'grams', 'g'
    ]
    if request in valid_measurements:
        return True
    else:
        return False

# Convert 'lbs' to 'pounds', 'tbsp' to 'tablespoon', etc.
def convert_to_generalized_measurement(measurement : str, liquid: bool):
    if 'teaspoon' in measurement.lower() or 'tsp' in measurement.lower():
        return 'teaspoon'
    elif 'tablespoon' in measurement.lower() or 'tbsp' in measurement or ' T ' in measurement:
        return 'tablespoon'
    elif 'ounce' in measurement.lower() or 'ounces' in measurement.lower() or 'oz' in measurement.lower():
        if liquid:
            return 'fluid_ounce'
        else:
            return 'dry_ounce'
    elif 'cup' in measurement.lower() or 'cups' in measurement.lower():
        if liquid:
            return 'liquid_cup'
        else:
            return 'dry_cup'
    elif 'pound' in measurement.lower() or 'lbs' in measurement.lower():
        return 'pounds'
    elif 'gram' in measurement.lower() or 'g' in measurement.lower():
        return 'grams'
    else:
        return None

# To handle converting between dry measure and 'wet' measure, check if the ingredient is a liquid.
def is_liquid(measurement):
    valid_liquids = [
        'water', 'milk', 'oil', 'alcohol', 'syrup'
    ]
    if measurement in valid_liquids:
        return True
    else:
        return False

# Since FDC reports back with results in 100 grams, we need to change the user's unit into grams to transform FDC results correctly.
def unit_to_grams(measurement: str):
    result = {
        'qty'    : 0,
        'liquid' : False,
        'amount' : ""
    }

    for word in measurement.split(" "):
        if '/' in word:
            left_hand  = word.split('/')[0]
            right_hand = word.split('/')[1]
            result['qty'] = int(left_hand) / int(right_hand)
        elif '.' in word:
            result['qty'] = word
        elif word.isdigit():
            result['qty'] = word
        elif is_liquid(word):
            result['liquid'] = True
        else:
            if result['amount'] == "":
                result['amount'] += word
            else:
                result['amount'] += word + " "
        
    if is_unit_of_measurement(result["amount"].strip()):
        for word in result['amount'].split():
            if word.isdigit():
                continue
            normalized = convert_to_generalized_measurement(word, result['liquid'])
            temp = ""
            if normalized:
                temp = normalized
            if temp != "":
                result['amount'] = temp

        # Since 100 grams will be our base quantity, we'll normalize 
        unit = {
            'grams'          : 0.01,    # 1 grams
            'tablespoon'     : 0.15,    # 15 grams
            'teaspoon'       : 0.042,   # 4.2 grams
            'dry_cup'        : 1.28,    # 1 dry cup = 128 grams
            'liquid_cup'     : 2.40,    # 1 cup (water) = 240 milliliters = 240 grams
            'dry_ounce'      : 0.2835,  # 1 oz = 28.35 grams
            'fluid_ounce'    : 0.2957,  # 1 fl. oz = 29.57 grams
            'pounds'         : 4.536,   # 1 pound = 453.6 grams
        }
        if unit[result['amount']]:
            return float(result["qty"]) * unit[result['amount']]
    else:
        return None

def modify_value(current_object, scalar):
    return current_object

# Take the result from MongoDB and multiply it. Return the transformed data.
def transform_data(document: dict, scalar: float):
    for key in document:
        if key == 'id' or key == 'description':
            continue
        elif type(document[key]) == list:
            for sub_key in document[key]:
                if type(sub_key) == dict:
                    transformed       = modify_value(sub_key, scalar)
                    sub_key['amount'] = str(transformed) 
        elif type(document[key]) == dict:
            for sub_key in document[key]:
                if type(document[key][sub_key]) == list:
                    temp = []
                    for item in document[key][sub_key]:
                        new_obj = {
                            'name'   : item['name'],
                            'amount' : modify_value(item['amount'], scalar)
                        }
                        temp.append(new_obj)
                    document[key][sub_key] = temp
                else:
                    document[key][sub_key] = modify_value(document[key][sub_key], scalar)
        else:
            document[key] = modify_value(document[key], scalar)
    return document