from functions import fetchcoordinates, fetchforecast, AIprompt, fetchsong, musicapi

# To remove certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import requests
import json
import random
import asyncio


def terminalrun():
    nav = 0
    
    # ---- Navigation enums ------
    # 0 = input prompt
    # 1 = Get coordinates based on location
    # 2 = Get forecast based on coordinates
    # 3 = Talk to AI
    # 4 = Make a song
    # 999 = Exit
    
    while nav < 999:
    
        if nav == 0:
            # 0 = input prompt
            inputlocation = input('Skriv en plats: ')
            currentlocation = inputlocation
            mood = input('Idag känner jag mig: ')
            music = input('Idag vill jag lyssna på: ')
            print('----------------------------------------------------------------------------------\n')
            nav = +1
    
        if nav == 1:
            # 1 = Get coordinates based on location  
            print('Hämtar koordinater baserat på input:')    
            coordinatesstring,lat,lon=fetchcoordinates(currentlocation)
            print(coordinatesstring)
            input('Tryck Enter för att fortsätta')
            nav+=1
    
        if nav == 2:
            # 2 = Get forecast based on coordinates
            print('Hämtar väderparametrar baserat på koordinater:')
            forecaststring=fetchforecast(inputlocation,lat,lon)
            print(forecaststring) 
            input('Tryck Enter för att fortsätta')
            nav+=1        
    
        if nav == 3:
            # 3 = Talk to AI
            airesult=AIprompt(forecaststring,mood,music,inputlocation)
            #print(airesult)
            input('Tryck Enter för att fortsätta')
            nav+=1
        
    
        if nav == 4:
            # 4 = Make a song
            fetchmusic=fetchsong(str(airesult),music,inputlocation)
    
    
    
    
    
        nav = int(input('---------------------------------\nMeny:\n0. Börja om\n1. Hämta koordinater igen\n2. Hämta prognos igen\n3. Skicka till AI igen.\n4. Generera en sång igen.\n999. Avsluta\n---------------------------------'))
        
    


from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory='templates')

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse('index.html', {'request':request})


@app.get("/api/fetchcoordinates")
def fetchcoordinates1(inputlocation: str):
    coordinatesstring,lat,lon=fetchcoordinates(inputlocation)
    return JSONResponse(content={'coordinatesstring': coordinatesstring,'lat': lat,'lon': lon})

@app.get("/api/fetchforecast")
def fetchforecast1(inputlocation: str,lat: str, lon: str):
    forecaststring=fetchforecast(inputlocation,lat,lon)
    return JSONResponse(content={'forecaststring': forecaststring})

@app.get("/api/askai")
def askai1(forecaststring: str,mood: str, music: str, inputlocation: str):
    airesult=AIprompt(forecaststring,mood,music,inputlocation)
    return JSONResponse(content={'airesult': airesult})

@app.get("/api/music")
def fetchsong1(airesult: str, music: str, inputlocation: str):
    fetchmusic=fetchsong(airesult,music,inputlocation)
    return JSONResponse(content={'fetchmusic': fetchmusic})

'''
@app.get("api/coordinates")
    coordinatesstring,lat,lon=fetchcoordinates(currentlocation)
    print(coordinatesstring)
    return JSONResponse(content={'result':coordinatesstring})
'''
    
    
if __name__ == "__main__":
    terminalrun()