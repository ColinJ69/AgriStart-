from .WeatherData import get_coords
from .WeatherData import get_weather_soil_data
import requests
import torch
from torchvision import transforms
from PIL import Image
import os
import haversine as hs   
from haversine import Unit
import reverse_geocoder as rg
import pandas as pd
import cv2
import torch.nn as nn
def is_farmable(address):
    class_names = ['good', 'bad']
    url = requests.get(f'https://maps.googleapis.com/maps/api/streetview?parameters&size=640x640&fov=50&location={address}&key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    
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
    if comp['climate'] != 'Tundra' or comp['climate'] != 'Desert':
        final_score += 3
        
    if 60 < comp['temperature'] < 85:
        final_score += 1
    
    if 5 < miles < 10:
        final_score += 1
    elif miles > 10:
        final_score += 3
    
    if farmable == 'good':
        final_score += 3
    
    final_score *= 10
    return final_score, comp, city, miles
        
    
    
    
def get_recommendations(N, P, K, pH, temperature):
    crops = pd.read_csv('https://github.com/ColinJ69/AgriStart/raw/main/Data/Crop_recommendation.csv')
    df = crops[((abs(crops['N'] - float(N))) < 15) & ((abs(crops['P'] - float(P))) < 15) & ((abs(crops['K'] - float(K))) < 15) &
               ((abs(crops['ph'] - float(pH))) < 1) & ((abs(crops['temperaturef'] - float(temperature))) < 15)]
    best_crops = df['label'].value_counts()[:3].index.tolist()

    def recommend_fert():
        
        fertilizer = pd.read_csv('https://github.com/ColinJ69/AgriStart/raw/main/Data/fertilizer.csv')
        values = []
        for crop in best_crops:
          
            n = fertilizer[fertilizer['Crop'] == crop]['N'].iloc[0]
           
            p = fertilizer[fertilizer['Crop'] == crop]['P'].iloc[0]
           
            k = fertilizer[fertilizer['Crop'] == crop]['K'].iloc[0]
         
        

            na = n - float(N)
            pa = p - float(P)
            ka = k - float(K)
        
            temp = {abs(na): "N", abs(pa): "P", abs(ka): "K"}
            max_value = temp[max(temp.keys())]
            if max_value == "N":
                if n < 0:
                    key = 'NHigh'
                else:
                    key = "Nlow"
            elif max_value == "P":
                if p < 0:
                    key = 'PHigh'
                else:
                    key = "Plow"
            else:
                if k < 0:
                    key = 'KHigh'
                else:
                    key = "Klow"
            values.append(key)
        return values
    values = recommend_fert()
    results = dict(zip(best_crops, values))
    return(results)
    
class Model(nn.Module):
  def __init__(self):
    super().__init__()
    self.conv1 = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1),
    nn.ReLU(), nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1),
    nn.ReLU(), nn.MaxPool2d(kernel_size=2, stride=2))
    self.conv2 = nn.Sequential(nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1),
    nn.ReLU(), nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1),
    nn.ReLU(), nn.MaxPool2d(kernel_size=2, stride=2))
    self.classifier = nn.Sequential(nn.Dropout(), nn.Linear(3276800, 3))

  def forward(self, x):
    x = self.conv1(x)
    x = self.conv2(x)
    x = x.view(x.size(0), -1)
    x = self.classifier(x)
    return x
    
def disease_detection():
    model = Model()
    model.load_state_dict(torch.load("C:/Users/johns/Downloads/disease_model2.pth"))
    model.eval()
    transform = transforms.Compose([transforms.Resize((640,640)), transforms.ToTensor()])
    class_names = ['Healthy', 'Powdery', 'Rust']
    cam = cv2.VideoCapture(0)
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imwrite('disease_img.jpg', frame)
        def detect():
            img = Image.open('disease_img.jpg')
            model.eval()
            with torch.inference_mode():
                img_trans = transform(img).unsqueeze(dim=0)
                output_disease = model(img_trans)
                predicted_class = torch.argmax(torch.softmax(output_disease, dim=1),dim=1)
                return class_names[predicted_class.item()]
        return detect()
    cam.release()
    os.remove('disease_img.jpg')
    cv2.destroyAllWindows()
        

        

        
recommend_crops(90, 42, 43, 6.9, 69, 202)
