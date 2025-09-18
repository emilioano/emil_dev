# Make a song out of it
import random
import requests
import json
import asyncio

from dotenv import load_dotenv
import os

load_dotenv()


def fetchsong(airesult,music,inputlocation):

#        rand = random.randint(0,1)
#        #print(rand)
#        gender='f'
#        if rand == 1:
#            gender='m'
#        else:
#            gender:'f
    def getgender():
        return 'm' if random.randint(0,1) == 1 else 'f'
    gender = getgender()

    musicurl = "https://api.kie.ai/api/v1/generate"

    musicpayload = {
        'prompt': airesult,
        'style': music,
        'title': 'En dag i '+inputlocation,
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
        'Authorization': os.getenv('suno_api_key'),
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
                #returnstring = f'Låt genererad! Länk: {audioUrl}'
                return audioUrl
            else:
                print(f'Status är: {taskstatusdataresponse}. Vill du vänta {waittime} sekunder och kollar igen eller avsluta?')
                quitorstay = input('Q för quit, Enter för att stanna')
                if quitorstay=="Q":
                    break
                else:
                    await asyncio.sleep(waittime)
    
    result=asyncio.run(fetch_song(5))
    return result

#print('Response är: ',taskstatusdata['data']['response'][0]['audioUrl']
#print(taskstatusdata['data'][0]['audioUrl']

#      print (musicpayload
#https://api.kie.ai/api/v1/generate/record-info?taskId=1829714c3252ebc193387ff174ceced
