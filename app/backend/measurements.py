"""
    Convert ingredient amounts returned from the database (or FDC API) based on user's input.
    This uses vizigr0u's "sugarcube" library to do a lot of the heavy lifting.
"""
from sugarcube import Volume, Mass, Flour

def convert_to_cup(measurement: str, result: dict):
    ingredient = 250 * Mass.gram * Flour
    doc = result['document']
    for k,v in doc:
        continue
    return str("%s = %s" % (ingredient, ingredient.to(Volume.cup)))