import datetime
import json
import urllib.request

def url_builder(lat, lon):
    user_api = 'af243c3d35c6f4fa444bd0594f3f09f6'  
    unit = 'metric'
    return 'http://api.openweathermap.org/data/2.5/forecast' + \
           '?units=' + unit + \
           '&APPID=' + user_api + \
           '&lat=' + str(lat) +  \
           '&lon=' + str(lon)

def fetch_data(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    return json.loads(output)
    
def time_converter(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d %b')

lon = -7.314800
lat = 54.498718
json_data = fetch_data( url_builder(lat, lon) ) 

today= ""
highest_temp= -1000
for forecast in json_data['list']:
    timestamp = time_converter( forecast['dt'])
    temperature = forecast['main']['temp']
    if today == "":
        today = timestamp
        highest_temp = temperature
    elif today == timestamp:
        if temperature > highest_temp:
            highest_temp = temperature
    else:
        print("{} : {}".format(today, highest_temp))
        today = timestamp
        highest_temp = temperature
print("{} : {}".format(today, highest_temp))
