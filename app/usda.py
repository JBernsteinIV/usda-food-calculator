#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse   # For creating a CLI parser.
import json       # For parsing JSON output of FoodData Central API.
import requests   # For submitting HTTP/HTTPS requests.

"""
    usda.py - Queries USDA's FoodData Central API for nutritional information.
     * Two APIs supported by FoodData Central:
       1. Search - Returns a list of result names & FoodData Central ID 'fdcId'.
       2. 'Food Details' - Search by fdcId. Returns results for that fdcId.
    ---
    How usda.py works:
     * Search for results by keywords given by user.
     * * If keyword exists in known_foods.csv, then return fdcId for entry.
     * * Else present FDC search result to user; let user decide choice to add.
     * * * Add newly found item to known_foods.csv file for later searches.
     * If multiple items are given by user, sum up the results for each nutrient.
"""
# Get API key for FDC API. API Key is required!
def api_key(filename):
    with open(filename) as file:
        key = file.read().rstrip()
    return key

# Wrapper function for submitting requests to Food Data Central.
def get_request(search_term, KEY):
    payload = {
        'Content-Type'       : 'application/json',
        'query'              : search_term,
    }

    request = requests.post(f'https://api.nal.usda.gov/fdc/v1/search?api_key={KEY}', json=payload)
    json_placeholder = request.json()
    #json_placeholder = placeholder.dumps()
    # 'foods' returns a list. Iterate the list to get the relevant data.
    items = []
    for item in json_placeholder['foods']:
        id   = item['fdcId']
        desc = item['description']
        id_and_desc = {
            'id'   : id,
            'desc' : desc
        }
        items.append(id_and_desc)
    #return request.json()
    return items

def get_ingredient(fdcId, KEY):
    request = requests.get(f'https://api.nal.usda.gov/fdc/v1/food/{fdcId}?api_key={KEY}')
    print(request)
    return request.json()

if __name__ == '__main__':
    key = api_key('../apikey.txt')

    parser = argparse.ArgumentParser('USDA Food Data Central API in Python')
    parser.add_argument('-s', '--search', help='Search for given item', required=True)

    args = parser.parse_args()

    query = args.search
    response = get_request(query, key)
    for items in response:
        print(f'FDCID: {items["id"]}')
        print(f'DESC: {items["desc"]}')

    for item in response['foods']:
        if item['dataType'] == 'SR Legacy':
            fdcId = item['fdcId']
            nutrients = get_ingredient(fdcId, key)
            print(json.dumps(nutrients, indent=4))
            print(json.dumps(item, indent=4))

    print(json.dumps(response, indent=4))
