
from functions import insertdbrecord,listdbrecords
from datetime import datetime


#    INSERT INTO requests (time, ip, location, mood, genre, airesult, musicresult)
#    VALUES ('{time}','{ip}','{location}','{mood}','{genre}','{airesult}','{musicresult}')

now=datetime.now()

insertdbrecord(now,'94.234.75.231','Kommun','Glad','Pop','Hej hej hej AI Result','URL till låt')

#listdbrecords()


'''
from datetime import date

import random
import time

m_or_f = True
date = date.today()

print (date)


rand = random.randint(0,1)
print(rand)


gender='f'
if rand == 1:
    gender='m'
else:
    gender='f'
print (gender)



def checkmusicstatus(taskid):
    status = self.get



'''
''''import requests
import time

class SunoAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.kie.ai/api/v1'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
 
    
    def wait_for_completion(self, task_id, max_wait_time=600):
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            status = self.get_task_status(task_id)
            
            if status['status'] == 'SUCCESS':
                print("All tracks generated successfully!")
                return status['response']
            elif status['status'] == 'FIRST_SUCCESS':
                print("First track generation completed!")
                return status['response']
            elif status['status'] == 'TEXT_SUCCESS':
                print("Lyrics/text generation successful!")
                return status['response']
            elif status['status'] == 'PENDING':
                print("Task is pending...")
            elif status['status'] == 'CREATE_TASK_FAILED':
                error_msg = status.get('errorMessage', 'Task creation failed')
                print(f"Error message: {error_msg}")
                raise Exception(error_msg)
            elif status['status'] == 'GENERATE_AUDIO_FAILED':
                error_msg = status.get('errorMessage', 'Audio generation failed')
                print(f"Error message: {error_msg}")
                raise Exception(error_msg)
            elif status['status'] == 'CALLBACK_EXCEPTION':
                error_msg = status.get('errorMessage', 'Callback process error')
                print(f"Error message: {error_msg}")
                raise Exception(error_msg)
            elif status['status'] == 'SENSITIVE_WORD_ERROR':
                error_msg = status.get('errorMessage', 'Content filtered due to sensitive words')
                print(f"Error message: {error_msg}")
                raise Exception(error_msg)
            else:
                print(f"Unknown status: {status['status']}")
                if status.get('errorMessage'):
                    print(f"Error message: {status['errorMessage']}")
            
            time.sleep(10)  # Wait 10 seconds
        
        raise Exception('Generation timeout')
    
    def get_task_status(self, task_id):
        response = requests.get(f'{self.base_url}/generate/record-info?taskId={task_id}',
                              headers={'Authorization': f'Bearer {self.api_key}'})
        result = response.json()
        
        if not response.ok or result.get('code') != 200:
            raise Exception(f"Status check failed: {result.get('msg', 'Unknown error')}")
        
        return result['data']

# Usage Example
def main():
    api = SunoAPI('YOUR_API_KEY')
    
    try:
        # Generate music with lyrics
        print('Starting music generation...')
        task_id = api.generate_music(
            'A nostalgic folk song about childhood memories',
            customMode=True,
            instrumental=False,
            model='V4_5',
            style='Folk, Acoustic, Nostalgic',
            title='Childhood Dreams'
        )
        
        # Wait for completion
        print(f'Task ID: {task_id}. Waiting for completion...')
        result = api.wait_for_completion(task_id)
        
        print('Music generated successfully!')
        print('Generated tracks:')
        for i, track in enumerate(result['sunoData']):
            print(f"Track {i + 1}:")
            print(f"  Title: {track['title']}")
            print(f"  Audio URL: {track['audioUrl']}")
            print(f"  Duration: {track['duration']}s")
            print(f"  Tags: {track['tags']}")
        
        # Extend the first track
        first_track = result['sunoData'][0]
        print('\nExtending the first track...')
        extend_task_id = api.extend_music(
            first_track['id'],
            defaultParamFlag=True,
            prompt='Continue with a hopeful chorus',
            style='Folk, Uplifting',
            title='Childhood Dreams Extended',
            continueAt=60,
            model='V4_5'
        )
        
        extend_result = api.wait_for_completion(extend_task_id)
        print('Music extended successfully!')
        print(f"Extended track URL: {extend_result['sunoData'][0]['audioUrl']}")
        
    except Exception as error:
        print(f'Error: {error}')

if __name__ == '__main__':
    main()'''