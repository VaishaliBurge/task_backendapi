from typing import Union
from fastapi import FastAPI,Depends
from fastapi.responses import RedirectResponse
from schemas.recepies_schema import RecepieSchema
from typing import List
import contentful
import json
import re
import os


app = FastAPI(docs_url="/api/docs")

@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='api/docs')

@app.get("/Recepies",response_model=List[RecepieSchema])
def get_recepies():
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
            receipe = {'title':title,'photo':entry.photo,'desc':entry.description,'calories':entry.calories,'description':entry.description}
            filteredData.append(receipe)

    if os.path.exists("data.json"):
        os.remove("./data.json")
    jsonString = json.dumps(filteredData)
    jsonFile = open("data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    return filteredData


@app.get("/RecepieDetail",response_model=List[RecepieSchema])
def  get_recepie_detail(title:str):
    f = open('./data.json')
    data = json.load(f)
    details = list()
    for i, s in enumerate(data):
        if s["title"] == title:
            details = data[i]
       
    return details if details else None

