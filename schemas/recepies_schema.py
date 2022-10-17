from dataclasses import dataclass
from pydantic import BaseModel
from typing import List

class RecepieSchema(BaseModel):
    title : str
    photo : str
    desc : str
    calories : str
    description : str