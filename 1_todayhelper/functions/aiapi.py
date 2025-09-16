import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

### Prompt to AI

def AIprompt(forecaststring,mood,music,inputlocation):

    askprompt = f'Vädret idag är följande: {forecaststring}. Jag känner mig {mood}. Jag vill lyssna på {music}. Ge mig råd för vad jag bäst kan hitta på i {inputlocation} och hur jag baserat på allt sammantaget kan hantera dagen på ett optimalt sätt, och ge mig förslag på lämplig klädsel. Ge mig tre relevanta affirmationer baserat på tidigare data som hjälper mig ta mig genom dagen'
    print('Prompt till AI: ',askprompt)
    print('----------------------------------------------------------------------------------\nLaddar...')
    gemini_api_key = os.getenv('gemini_api_key')
    ai_endpoint = f'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={gemini_api_key}'
    headers = {
        "Content-Type": "application/json"
    }
    aiparams2 = {
        'contents':[{'parts':['text:aiprompt']}]
    }
    aidata = {'contents':[
        {'parts':[{'text':askprompt}
    ]}]}
    airesponse = requests.post(ai_endpoint,headers=headers,data=json.dumps(aidata),verify=False)
    if airesponse.status_code==200:
        #print('Status 200')
        airesult = airesponse.json()
        airesulttext = airesult['candidates'][0]['content']['parts'][0]['text']
        print(airesulttext)
        return airesulttext
    else:
        print('Fel ',airesponse.status_code,airesponse.text)
        return 'Fel'
    