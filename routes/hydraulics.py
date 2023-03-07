from urllib.request import Request
from fastapi import APIRouter, Request
import json
from fastapi.responses import JSONResponse
import os
from services import pressureDrop
from services import energyplusConvert
router = APIRouter()
import json
import requests

@router.get("/")
async def root():
    return {"Message": "Frontpage"}


@router.post("/energyPlusConvert")
async def result(request:Request):
    convertedResults = energyplusConvert.results()
    headers = {'Content-Type': 'text/turtle'}    
    url = "http://localhost:3030/ny-db/data"
    response = requests.request("POST", url, headers=headers, data=convertedResults)    
    return response.text


@router.post("/pressureDropTees")
async def calculate_pipes(request: Request):
    data = await request.body()
    teeGraph = pressureDrop.tees(json.loads(data))
    return json.dumps(teeGraph)

@router.post("/pressureDropRest")
async def calculate_pipes(request: Request):
    data = await request.body()
    pipeGraph = pressureDrop.pipes(json.loads(data))
    return json.dumps(pipeGraph) 