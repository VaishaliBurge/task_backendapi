from dataclasses import dataclass
from pydantic import BaseModel
from typing import List


#Base model for Recipe : Same model is getting returned to the user as the API response.
class RecipeSchema(BaseModel):
    title : str
    photo : str
    desc : str
    calories : str
    description : str