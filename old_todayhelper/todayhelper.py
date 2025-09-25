# To remove certificate warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import requests
import json
import random
import asyncio

nav = 0

# ---- Navigation enums ------
# 0 = main menu
# 1 = Get coordinates based on location
# 2 = Get forecast based on coordinates
# 3 = Talk to AI
# 4 = Make a song
# 999 = Exit

while nav < 999:

    if nav == 0:
        plats = input('Skriv en plats (engelsk benämning): ')
        mood = input('Idag känner jag mig: ')
        music = input('Idag vill jag lyssna på: ')
        print('----------------------------------------------------------------------------------\n')
        #plats = 'Ludvika'
        nav = +1



### Fetch coordinates based om location entered

    if nav == 1:
        print('Hämtar koordinater baserat på input:')

        urlcordinates = 'https://geocoding-api.open-meteo.com/v1/search'
        cordinatesparameters = {'name':plats}

        cordinatesresponse = requests.get(urlcordinates, params=cordinatesparameters, verify=False)

        if cordinatesresponse.status_code==200:
            cordinatesdata = cordinatesresponse.json()
            #print(cordinatesdata)
            if cordinatesdata.get('results'):
                lat = cordinatesdata['results'][0]['latitude']
                lon = cordinatesdata['results'][0]['longitude']
                country = cordinatesdata['results'][0]['country']
                population = cordinatesdata['results'][0]['population']
                print('Koordinater för ',plats,' med ',population,' invånare, som ligger i ',country,' är latitude: ',lat,' och longitude: ',lon)
                print('----------------------------------------------------------------------------------\n')

            else: print('Ingen plats hittad')
        else:
            print(f'Fel vid API-anrop: {response.status_code}')

        nav = nav + 1

    input('Tryck <ENTER> för att fortsätta')


### Fetch forecast based on location

    if nav == 2:

        print('Hämtar väderparametrar baserat på koordinater:')

        forecasturl = 'https://api.open-meteo.com/v1/forecast'
        forecastparams = {
        'latitude':lat,
        'longitude':lon,
        'daily': ['weather_code', 'temperature_2m_max', 'temperature_2m_min','wind_speed_10m_max','sunrise','sunset','daylight_duration','rain_sum','showers_sum','snowfall_sum'],
        'forecast_days':1,
        'timezone':'CET',
        }
        forecastresponse = requests.get(forecasturl,params=forecastparams,verify=False)

        if forecastresponse.status_code==200:
            forecastdata = forecastresponse.json()
            #print(forecastdata)
            daily = forecastdata['daily']
            max_temp = daily['temperature_2m_max']
            min_temp = daily['temperature_2m_min']
            wind_speed_max = daily['wind_speed_10m_max']
            rain_sum = daily['rain_sum']
            snowfall_sum = daily['snowfall_sum']
            print('Maximal temperatur i ',plats,' idag blir ',max_temp,', lägsta temperatur blir ',min_temp,'. Högsta vindhastighet blir ',wind_speed_max,' m/s. Det väntas regna ',rain_sum,' mm. Det väntas snöa ',snowfall_sum,' cm.')
            print('----------------------------------------------------------------------------------\n')

            forecaststring = f'Maximal temperatur i {plats} idag blir {max_temp}, lägsta temperatur blir {min_temp}. Högsta vindhastighet blir {wind_speed_max} m/s. Det väntas regna {rain_sum} mm. Det väntas snöa {snowfall_sum} cm. '

        nav = nav + 1
    

        input('Tryck <ENTER> för att fortsätta')


### Prompt to AI
    if nav == 3:
        askprompt = 'Vädret idag är följande: '+forecaststring+'Jag känner mig '+mood+'. Jag vill lyssna på '+music+'. Ge mig råd för vad jag bäst kan hitta på i '+plats+' och hur jag baserat på allt sammantaget kan hantera dagen på ett optimalt sätt, och ge mig förslag på lämplig klädsel. Ge mig tre relevanta affirmationer baserat på tidigare data som hjälper mig ta mig genom dagen'
        askpromptstr = str(askprompt)


        print('Prompt till AI: ',askpromptstr)
        print('----------------------------------------------------------------------------------\nLaddar...')

        api_key = 'AIzaSyCLS7v6B-lTHfljnSY8TFUZzOij2qfg4E4'
        ai_endpoint = f'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={api_key}'


        headers = {
            "Content-Type": "application/json"
        }


        aiparams2 = {
            'contents':[{'parts':['text:aiprompt']}]
        }


        aidata = {'contents':[
            {'parts':[{'text':askpromptstr}
        ]}]}


        airesponse = requests.post(ai_endpoint,headers=headers,data=json.dumps(aidata),verify=False)

        if airesponse.status_code==200:
            #print('Status 200')
            airesult = airesponse.json()
            print(airesult['candidates'][0]['content']['parts'][0]['text'])
            print('----------------------------------------------------------------------------------\n')

        else:
            print('Fel ',airesponse.status_code,airesponse.text)

        nav = nav + 1

        input('Tryck <ENTER> för att fortsätta')


# Make a song out of it

    if nav == 4:

#        rand = random.randint(0,1)
#        #print(rand)
#        gender='f'
#        if rand == 1:
#            gender='m'
#        else:
#            gender:'f'

        def getgender():
            return 'm' if random.randint(0,1) == 1 else 'f'
        gender = getgender()

        musicurl = "https://api.kie.ai/api/v1/generate"
               
        musicpayload = {
            'prompt': airesult['candidates'][0]['content']['parts'][0]['text'],
            'style': music,
            'title': 'En dag i '+plats,
            'customMode': True,
            'instrumental': False,
            'model': "V3_5",
            'callBackUrl': "https://api.example.com/callback",
            'negativeTags': music,
            'vocalGender': gender,
            'styleWeight': 0.65,
            'weirdnessConstraint': 0.65,
            'audioWeight': 0.65
        }
        
        musicheaders = {
            'Authorization': 'Bearer 3a38a9b6947b15de8626ee337a06bd4a',
            'Content-Type': 'application/json'
        }

        musicresponse = requests.post(musicurl,json=musicpayload,headers=musicheaders,verify=False)

        print('Genererar en låt!')

        print('Svar från API: ',musicresponse.json())
        musicresponsejson = musicresponse.json()

        async def fetch_song(waittime):

            taskid1 = musicresponsejson['data']
            taskid = taskid1.get('taskId','taskid saknas')
   
            print('Task id är:', taskid)

            print('Nu tar det en stund!')

            checkurl = 'https://api.kie.ai/api/v1/generate/record-info?taskId='+taskid
            strcheckurl=str(checkurl)

            while True:
                statusresponse = requests.get(strcheckurl,headers=musicheaders,verify=False)
                taskstatusdata = statusresponse.json()
                taskstatusdataresponse = taskstatusdata['data']['status']

                if taskstatusdataresponse=='PENDING':
                    print(f'Status är {taskstatusdataresponse}, låt kommer börja genereras, väntar {waittime} sekunder och kollar igen. Vänligen vänta.')
                    await asyncio.sleep(waittime)
                elif taskstatusdataresponse=='TEXT_SUCCESS':
                    print(f'Status är {taskstatusdataresponse}, textgenerering lyckades, väntar {waittime} sekunder och kollar igen. Vänligen vänta.')
                    await asyncio.sleep(waittime)
                elif taskstatusdataresponse=='FIRST_SUCCESS':
                    print(f'Status är {taskstatusdataresponse}, track generering lyckades, väntar {waittime} sekunder och kollar igen. Vänligen vänta.')
                    await asyncio.sleep(waittime)
                elif taskstatusdataresponse=='SUCCESS':
                    audio_sunoData = taskstatusdata['data']['response']['sunoData']
                    audioUrl = (audio_sunoData[0].get('audioUrl',''))
                    print(f'Låt genererad! Länk: {audioUrl}')
                    break
                else:
                    print(f'Status är: {taskstatusdataresponse}. Vill du vänta {waittime} sekunder och kollar igen eller avsluta?')
                    quitorstay = input('Q för quit, Enter för att stanna')
                    if quitorstay=="Q":
                        break
                    else:
                        await asyncio.sleep(waittime)

        asyncio.run(fetch_song(5))







        

        

        #print('Response är: ',taskstatusdata['data']['response'][0]['audioUrl'])



        #print(taskstatusdata['data'][0]['audioUrl'])


        



#        print (musicpayload)

#https://api.kie.ai/api/v1/generate/record-info?taskId=1829714c3252ebc193387ff174ceced0




    nav = int(input('---------------------------------\nMeny:\n0. Börja om\n1. Hämta koordinater igen\n2. Hämta prognos igen\n3. Skicka till AI igen.\n4. Generera en sång igen.\n999. Avsluta\n---------------------------------'))
    


