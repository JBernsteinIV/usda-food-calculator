import requests
from dotenv import dotenv_values
# Removes any irrelevant information (e.g. "Ash")
import nutrient_filter
# Handles transforming data into a consistent shape for the database (also renames some nutrients to more familiar names)
import housekeeping

config         = dotenv_values(".env")
API_KEY        = config.get("USDA_FDC_API_KEY")

# Query Food Data Central API.
def fdc_search_by_string(search_term):
    payload = {
        'Content-Type': 'application/json',
        'query'       : search_term,
        'pageSize'    : 10,
        'sortBy'      : 'fdcId'
    }
    request = requests.post(f'https://api.nal.usda.gov/fdc/v1/search?api_key={API_KEY}', json=payload).json()
    results = []
    for result in request['foods']:
        obj = {
            'id'          : result['fdcId'],
            'description' : result['lowercaseDescription'],
            'database'    : result['dataType'],
            'category'    : result['foodCategory'] 
        }
        results.append(obj)
    return results

def fdc_search_by_id(fdcId):
    request = requests.get(f'https://api.nal.usda.gov/fdc/v1/food/{fdcId}?api_key={API_KEY}').json()
    structured_nutrient = None
    # We only really need the name and amount for each nutrient. Keep track of unit just in the off chance the result returns not in grams.
    # In that edge case we will need to perform a transformation to 100 grams to normalize any additional transformations.
    for result in request['foodNutrients']:
        # Edge case for child objects that do not contain the key 'amount' (e.g. "proximates").
        temp = result.get('amount')
        if temp is None:
            continue
        nutrient = {
            'name'  : result['nutrient']['name'],
            'amount': result['amount'],
            'unit'  : result['nutrient']['unitName'] 
        }
        keep = nutrient_filter.nutrient_filter(nutrient)
        if keep:
            structured_nutrient = housekeeping.group_by_type(nutrient, structured_nutrient)
    # The last thing we need to do is keep track of the ID (which will be used as the ID for our database) and the description.
    desc = housekeeping.rename(request['description'])
    structured_nutrient['id']          = request['fdcId']
    structured_nutrient['description'] = desc
    return structured_nutrient