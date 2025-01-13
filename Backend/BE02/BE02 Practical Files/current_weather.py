import datetime
import json
import urllib.request

def url_builder(lat, lon):
    user_api = 'af243c3d35c6f4fa444bd0594f3f09f6'  
    unit = 'metric'
    return 'http://api.openweathermap.org/data/2.5/weather' + \
           '?units=' + unit + \
           '&APPID=' + user_api + \
           '&lat=' + str(lat) +  \
           '&lon=' + str(lon)

def fetch_data(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    return json.loads(output)
    
def time_converter(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d %b %I:%M %p')

lon = -7.314800   
lat = 54.498718
json_data = fetch_data( url_builder(lat, lon) )

temperature = str( json_data['main']['temp'] )
timestamp = time_converter( json_data['dt'] )
description = json_data['weather'][0]['description']
place = json_data['name']
sunset = json_data['sys']['sunset']
print("Current weather in " + place)
print(timestamp + " : " + temperature +  " : " + description)
print("Sunset is at " + time_converter(sunset))