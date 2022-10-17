from typing import Union
from fastapi import FastAPI,Depends
from fastapi.responses import RedirectResponse
from schemas.recipes_schema import RecipeSchema
from typing import List
import contentful
import json
import re
import os


app = FastAPI(docs_url="/api/docs")

@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='api/docs')

@app.get("/recipes",response_model=List[RecipeSchema])
def get_recipes():
    """
    This API returns the list of recipes : title and the image for the recipes
    """

    filteredData = list()
    client = contentful.Client('kk2bw5ojx476', '7ac531648a1b5e1dab6c18b0979f822a5aad0fe5f1109829b8a197eb2be4b84c') 
    entries = client.entries() 
    for entry in entries:
        if(getattr(entry, 'photo', '') != ''):
            entry.photo = entry.photo.url()
            if(getattr(entry, 'tags', '') != ''):
                entry.tag = ''
            
            title = re.sub(r"@\S+", "",entry.title)
            title = title.replace("\t", " ")
            print(title)
            recipe = {'title':title,'photo':entry.photo,'desc':entry.description,'calories':entry.calories,'description':entry.description}
            filteredData.append(recipe)

    if os.path.exists("data_formatted.json"):
        os.remove("./data_formatted.json")
    jsonString = json.dumps(filteredData)
    jsonFile = open("data_formatted.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    return filteredData


@app.get("/recipe_details",response_model=List[RecipeSchema])
def  get_recipe_detail(title:str):
    """
    This API returns the details for the recipes.
    """
    
    f = open('./data_formatted.json')
    data = json.load(f)
    details = list()
    for i, s in enumerate(data):
        if s["title"] == title:
            details = data[i]
       
    return details if details else None

