import datetime
import requests
import folium

# Real time taxi availability data
today = datetime.datetime.today() 
params = {"date": today.strftime("%Y-%m-%d")} # YYYY-MM-DD 
taxi = requests.get('https://api.data.gov.sg/v1/transport/taxi-availability', params=params).json()
taxi['features'][0]['properties']['taxi_count']

# Plotting taxis on Sg map
sg_map = folium.Map([1.3521, 103.8198], zoom_start = 12, tiles="Stamen Terrain")
for coord in taxi['features'][0]['geometry']['coordinates']:
    folium.Marker([coord[1], coord[0]]).add_to(sg_map)
sg_map

# Save the map to an HTML file
sg_map.save("taxi_availability_map.html")