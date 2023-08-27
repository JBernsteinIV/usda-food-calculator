from dotenv.main import rewrite
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict

# Query USDA Food Data Central API if ingredient not found.
from fdc import (
    fdc_search_by_string,
    fdc_search_by_id,
)
# Query MongoDB for ingredient (if it exists in the database)
from database import (
    read_ingredient_by_id,
    read_ingredient_by_string,
    create_ingredient
)
# Handy functions to structure results into a nice "shape".
from housekeeping import (
    unit_to_grams,
    is_unit_of_measurement,
    transform_data
)

class Recipe(BaseModel):
    name: str              
    ingredients: list

app = FastAPI()

origins = [
    'http://localhost:27017',
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
def read_root():
    return {"Ping" : "Pong"}

@app.post("/")
async def make_recipe(request: Request, recipe: Recipe):
    results_list    = []
    ingredient_list = recipe.ingredients
    for ingredient in ingredient_list:
        #measurement     = ingredient["measurement"]
        ingredient_name = ingredient["name"]
        results         = await get_ingredients(request=request, ingredient=ingredient_name)
        results_list.append(results)
    return results_list

@app.get("/ingredient/")
async def get_ingredients(request: Request, ingredient: str):
    # Parse the request for any measurements, instructions, etc. and separate out into a new object.
    requested_ingredient = {
        'multiple'       : None, # How much to multiply the data by (by converting units to grams).
        'measurement'    : None,
        'unit'           : None,
        'instructions'   : None,
        'ingredient'     : None
    }
    unit = None
    for word in ingredient.split(" "):
        if word.isdigit():
            requested_ingredient['measurement'] = float(word)
        elif '/' in word or '.' in word:
            requested_ingredient['measurement'] = word
        elif is_unit_of_measurement(word):
            requested_ingredient['unit'] = word
        else:
            if requested_ingredient['ingredient']:
                requested_ingredient['ingredient'] += word + " "
            else:
                requested_ingredient['ingredient'] = word
    # After the measurement and unit keys are populated, capture the unit to grams equivalent in the amount key.
    if not requested_ingredient['measurement']:
        requested_ingredient['measurement'] = 1
    # If the unit isn't defined, this means the user probably passed in "4 onions" instead of "4 cups onions".
    if not requested_ingredient['unit']:
        # TODO: Since countable quantities have different weights for different items, this edge case needs a lookup to known weights. Then transform.
        requested_ingredient['measurement'] = requested_ingredient['measurement'] * 100
        requested_ingredient['unit'] = 'grams'

    requested_ingredient['multiple'] = unit_to_grams(str(requested_ingredient['measurement']) + " " + requested_ingredient['unit'])

    # TODO: Reimplement to check for substrings. Currently only works for exact match (e.g. Avocados instead of just 'Avocado')
    response = None
    found = await read_ingredient_by_string(request, requested_ingredient['ingredient'])
    if found:
        response = found
    else:
        response = fdc_search_by_string(requested_ingredient['ingredient'])

    if response:
        for element in response:
            if "document" in element:
                element = transform_data(element['document'], requested_ingredient['multiple'])
        
        return response
    raise HTTPException(404, f"Ingredient {ingredient} not found")

@app.get("/ingredient/{ingredient}")
async def get_ingredient(request: Request, ingredient: int):
    found = await read_ingredient_by_id(request, ingredient)
    if found:
        response = found
    else:
        response = fdc_search_by_id(ingredient)
        if response:
            # Save the result to the database.
            response = await create_ingredient(request, response)
    
    if response:
        return response['document']
    raise HTTPException(404, f"Ingredient {ingredient} not found")

@app.get("/api/v1/test/")
async def test(request: Request, ingredient: str):
    response = None
    found = await read_ingredient_by_string(request, ingredient)
    if found:
        response = found
    if response:
        return response
    raise HTTPException(404, f'Test failed')