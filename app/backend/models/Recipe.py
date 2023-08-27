from pydantic import BaseModel
from typing import List

class Recipe(BaseModel):
    name: str
    #ingredients: List(dict)
