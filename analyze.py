#from .Weather_Data import get_coords
#from .Weather_data import get_weather_soil_data
import requests
import torch
from torchvision import transforms
from PIL import Image
import os
import haversine as hs   
from haversine import Unit
import reverse_geocoder as rg
import pandas as pd

def is_farmable(address):
    class_names = ['good', 'bad']
    url = requests.get(f'https://maps.googleapis.com/maps/api/streetview?parameters&size=640x640&fov=50&location={address}&key=xxxxxxxxxxx')
    
    with open("img.png", "wb") as file:
        file.write(url.content)
    MODEL = torch.load("C:/Users/johns/Downloads/soil_quality_model.pth")
    MODEL.eval()
    img = Image.open("img.png")
    transform = transforms.Compose([transforms.ToTensor()])
    with torch.inference_mode():
        trans_img = transform(img).unsqueeze(dim=0)
        output = MODEL(trans_img)
    predicted_class = torch.argmax(torch.softmax(output, dim=1),dim=1)
    os.remove("img.png")
    return class_names[predicted_class.item()]
def get_nearby_city(lat, lng):
    coordinates = (lat,lng)
    results = rg.search(coordinates, mode=1)
    lat, lng, city = results[0]['lat'], results[0]['lon'], results[0]['name']
    distance = hs.haversine((float(lat), float(lng)), coordinates, unit=Unit.MILES)
    shortened_dist = round(distance, 1)
    return city, shortened_dist
def determine_farmability(address):
    lat, lng = get_coords(address)
    city, miles = get_nearby_city(lat, lng)
    attrs = get_weather_soil_data(lat, lng)
    print(attrs)
    comp = {}
    soil_moisture = attrs['avg_soil_moist']
    print(soil_moisture)
    if  0.2 < soil_moisture < 0.8:
        comp['soil_moist'] = 'Optimal moisture'
    elif soil_moisture < 0.2:
        comp['soil_moist'] = 'Low moisture'
    elif soil_moisture > 0.8:
        comp['soil_moist'] = 'Excess moisture'
       
    comp['temperature'] = attrs['temperature']
    s_temp = attrs['avg_soil_temp']
    if 60 < s_temp < 75:
        comp['s_temp'] = 'Good Soil Temperature'
    elif s_temp < 60:
        comp['s_temp'] = 'Low Soil Temperature'
    elif s_temp > 75:
        comp['s_temp'] = 'High Soil Temperature'
    
    climate = attrs['climate']
    abbr_to_name = {'Af': 'Tropical', 'Am': 'Tropical','Aw': 'Tropical', 'As': 'Tropical', 'BWh': 'Desert', 'BWk':'Desert', 'BSh': 'Semi-arid', 'BSk': 'Semi-arid', 'Csa': 'Temperate',
                    'Csb': 'Temperate', 'Csc': 'Temperate', 'Cfa': 'Temperate', 'Cfb': 'temperate', 'Cfc':'temperate',
                    'Cwa':'Temperate','Cwb':'Temperate','Cwc':'Temperate','Dfc':'Continental','Dfb':'Continental','Dfa':'Continental', 'Dfd':'Continental','Dwa':'Continental', 'Dwb':'Continental', 'Dwc':'Continental',
                    'Dwd':'Continental', 'Dsa':'Continental', 'Dsb':'Continental', 'Dsc':'Continental', 'Dsd':'Continental', 'ET': 'Tundra','EF': 'Tundra'}
    comp['climate'] = abbr_to_name[climate]
           
    farmable = is_farmable(address)
    return comp, farmable, city, miles


def get_score(address):
    comp, farmable, city, miles = determine_farmability(address)
    final_score = 0
    max_score = 10
    if comp['climate'] == 'Tundra' or comp['climate'] == 'Desert':
        final_score -= 2
    else:
        final_score += 2
        
    if 60 < comp['temperature'] > 85:
        final_score -= 1
    else: 
        final_score += 1
    
    if 5 < miles < 10:
        final_score += 1
    elif miles < 5: 
        final_score -= 1
    else:
        final_score += 3
        
    
    
    
def recommend_crops(N, P, K, pH, temperature, rainfall):
    crops = pd.read_csv('https://github.com/ColinJ69/AgriStart/raw/main/Data/Crop_recommendation.csv')
    df = crops[((abs(crops['N'] - N)) < 10) & ((abs(crops['P'] - P)) < 10) & ((abs(crops['K'] - K)) < 10) &
               ((abs(crops['ph'] - pH)) < 1) & ((abs(crops['temperaturef'] - temperature)) < 10) &  ((abs(crops['rainfall'] - rainfall)) < 35)]
    recommendations = df[['label']]
    best_crops = recommendations.value_counts().nlargest(3)
    
    
    def recommend_fert():
        
        fertilizer = pd.read_csv('https://github.com/ColinJ69/AgriStart/raw/main/Data/fertilizer.csv')
        top_crop1 = best_crops.iloc[0]
        top_crop2 = best_crops.iloc[1]
        top_crop3 = best_crops.iloc[2]
        

        

        
recommend_crops(90, 42, 43, 6.9, 69, 202)
