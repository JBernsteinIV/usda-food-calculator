from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request, status
from fastapi.responses import JSONResponse
from dotenv import dotenv_values
import json
from models import Recipe

config = dotenv_values(".env")
DB_URI = config.get("DATABASE_URI")
DB_PORT= config.get("DATABASE_PORT")

client = AsyncIOMotorClient(f"mongodb://{DB_URI}:{DB_PORT}")

db          = client['ingredients']
ingredients = db['ingredients']

async def create_ingredient(request: Request, ingredient: dict):
    result  = await db.ingredients.insert_one({
        '_id'      : ingredient['id'], 
        'document' : ingredient})
    created = await db.ingredients.find_one({
        '_id' : ingredient['id']
    })
    return created

async def find_documents(request: Request, ingredient_name: str):
    cursor = db.ingredients.find({'$text': { 
            '$search': f'/{ingredient_name}/i'
        }
    }, {"_id" : False})
    documents = await cursor.to_list(length=25)
    return documents

# Search database for any ingredients by string name. If one is found, return it. Otherwise, call the fdc_search_by_string function from fdc.py.
async def read_ingredient_by_string(request: Request, ingredient_name: str):
    documents = []
    results = await find_documents(request, ingredient_name)
    for document in results:
        documents.append(document)
    return documents

# Search database for any ingredients by string name. If one is found, return it. Otherwise, call the fdc_search_by_id function from fdc.py.
async def read_ingredient_by_id(request: Request, ingredient_id: int):
    document = await db.ingredients.find_one({'_id': ingredient_id}, {"_id": False})
    #document = document.pop("_id")
    return document