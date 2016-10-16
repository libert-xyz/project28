import httplib2
import json
import os

def getGeoCode(inputString):
    google_api_key = os.environ['google_api_key']
    locationString = inputString.replace(" ","+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'
    %(locationString,google_api_key))

    h = httplib2.Http()
    response, content = h.request(url,'GET')
    result = json.loads(content.decode())

    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']
    return (lat,lng)
