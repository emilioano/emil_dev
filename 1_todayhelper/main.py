from functions import fetchcoordinates, fetchforecast, AIprompt, fetchsong, musicapi

# To remove certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import requests
import json
import random
import asyncio

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
        inputlocation = input('Skriv en plats (engelsk benämning): ')
        currentlocation = inputlocation
        mood = input('Idag känner jag mig: ')
        music = input('Idag vill jag lyssna på: ')
        print('----------------------------------------------------------------------------------\n')
        #plats = 'Ludvika'
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
        #print(AIprompt(forecaststring,mood,music,location))
        #airesulttext=''
        airesult=AIprompt(forecaststring,mood,music,inputlocation)
        input('Tryck Enter för att fortsätta')
        nav+=1
    

    if nav == 4:
        # 4 = Make a song
        print(airesult)
        #print(fetchsong(airesulttext,music,location)) 
        fechsong=fetchsong(str(airesult),music,inputlocation)      





    nav = int(input('---------------------------------\nMeny:\n0. Börja om\n1. Hämta koordinater igen\n2. Hämta prognos igen\n3. Skicka till AI igen.\n4. Generera en sång igen.\n999. Avsluta\n---------------------------------'))
    


