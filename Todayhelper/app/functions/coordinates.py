import requests


### Fetch coordinates based om location entered

def fetchcoordinates(currentlocation,language):
    urlcordinates = 'https://geocoding-api.open-meteo.com/v1/search'
    cordinatesparameters = {'name':currentlocation}
    cordinatesresponse = requests.get(urlcordinates, params=cordinatesparameters, verify=False)
    if cordinatesresponse.status_code==200:
        cordinatesdata = cordinatesresponse.json()
        #print(cordinatesdata)
        if cordinatesdata.get('results'):


            lat = cordinatesdata['results'][0]['latitude']
            lon = cordinatesdata['results'][0]['longitude']
            country = cordinatesdata['results'][0]['country']
            population = cordinatesdata['results'][0]['population']

            if language == 'SE':
                coordinatesstring = f'Koordinater för {currentlocation} med {population} invånare, som ligger i {country} är latitude: {lat} och longitude: {lon}',lat,lon
            else:
                coordinatesstring = f'The coordinates for {currentlocation} with {population} inhabitants, located in {country} has latitude: {lat} and longitude: {lon}',lat,lon
                
            return coordinatesstring


        else: return f'Ingen plats hittad'
    else:
        return f'Fel vid API-anrop: {cordinatesresponse.status_code}'

