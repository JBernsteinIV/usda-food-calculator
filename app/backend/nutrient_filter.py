# FDC allows an optional filter of up to 25 nutrients. Since we need more than that, this is a custom filter to rule out things deemed unnecessary.
# e.g. 'Energy' in the form of kilojoules (Calories will be used instead).
def nutrient_filter(nutrient):
    # Edge case for Energy in kilojoules.
    if 'kJ' in nutrient['unit']:
        return False
    keep = [
        'Water', 'Energy', 'Protein', 'Sucrose', 'Fructose', 'Lactose', 'Galactose', 'Maltose', 'Dextrose', 'Glucose',
        'Calcium, Ca', 'Iron, Fe', 'Phosphorus, P', 'Potassium, K', 'Sodium, Na', 'Zinc, Zn', 'Copper, Cu', 'Magnesium, Mg', 'Selenium, Se', 'Manganese, Mn',
        'Fluoride, F', 'Vitamin C, total ascorbic acid', 'Thiamin', 'Riboflavin', 'Niacin', 'Pantothenic acid', 'Vitamin B-6', 'Biotin',
        'Vitamin B-12', 'Vitamin A (RAE)', 'Folate, total', 'Vitamin E (alpha-tocopherol)', 'Vitamin D (D2 + D3)', 'Vitamin K (phylloquinone)', 
        'Cholesterol', 'Tryptophan', 'Threonine', 'Leucine', 'Isoleucine', 'Taurine', 'Lysine', 'Methionine', 'Cystine', 'Phenylalanine',
        'Tyrosine', 'Valine', 'Arginine', 'Histidine', 'Alanine', 'Aspartic acid', 'Glutamic acid', 'Glycine', 'Proline',  'Serine', 'Caffeine',
        'Total lipid (fat)', 'Carbohydrate, by difference', 'Fiber, total dietary', 'Sugars, total including NLEA',
        'PUFA 2:5 n-3 (EPA)', 'PUFA 22:6 n-3 (DHA)', 'PUFA 18:3 n-3 c,c,c (ALA)', 'Fatty acids, total saturated', 'Fatty acids, total monounsaturated',
        'Fatty acids, total polyunsaturated', 'Fatty acids, total trans', 
    ]
    if nutrient['name'] not in keep:
        return False
    return True