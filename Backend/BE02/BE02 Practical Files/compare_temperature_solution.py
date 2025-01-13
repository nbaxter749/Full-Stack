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

lat_1 = input("Enter the first latitude value >> ")
lon_1 = input("Enter the first longitude value >> ")
json_data_1 = fetch_data( url_builder( lat_1, lon_1))
temperature_1 = json_data_1['main']['temp']
place_1 = json_data_1['name']

lat_2 = input("Enter the second latitude value >> ")
lon_2 = input("Enter the second longitude value >> ")
json_data_2 = fetch_data( url_builder( lat_2, lon_2))
temperature_2 = json_data_2['main']['temp']
place_2 = json_data_2['name']

print("Temperature at {} is {}".format(place_1, temperature_1))
print("Temperature at {} is {}".format(place_2, temperature_2))

if temperature_1 > temperature_2:
    print("{} is hotter than {}".format(place_1, place_2))
elif temperature_1 < temperature_2:
    print("{} is hotter than {}".format(place_2, place_1))
else:
    print("{} and {} are the same temperature".format(place_1, place_2))
    

