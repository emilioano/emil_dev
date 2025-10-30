import requests

### Fetch forecast based on location



def fetchforecast(currentlocation,lat,lon,language):
    

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
        #print('Maximal temperatur i ',location,' idag blir ',max_temp,', lägsta temperatur blir ',min_temp,'. Högsta vindhastighet blir ',wind_speed_max,' m/s. Det väntas regna ',rain_sum,' mm. Det väntas snöa ',snowfall_sum,' cm.')
        #print('----------------------------------------------------------------------------------\n')
        
        if language == 'SE':
            forecaststring = f'Maximal temperatur i {currentlocation} idag blir {max_temp} C, lägsta temperatur blir {min_temp} C. Högsta vindhastighet blir {wind_speed_max} m/s. Det väntas regna {rain_sum} mm. Det väntas snöa {snowfall_sum} cm.'
        else:    
            forecaststring = f'Maxiumum temperature in {currentlocation} today is {max_temp} C, lowest temperature is{min_temp} C. The highest wind speed will be {wind_speed_max} m/s. Rain to be expected is {rain_sum} mm. {snowfall_sum} cm of snow is expected.'
          
        return forecaststring
