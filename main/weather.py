import openmeteo_requests
import json
import requests_cache
import pandas as pd
from retry_requests import retry
import requests
from kgcPy import *

def get_coords(user_address):
	
	geocode_request = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={user_address}&key=xxxxxxxxxxxxxxxxxxxxxx")
	data = geocode_request.json()
	lat = data['results'][0]['geometry']['location']['lat']
	lng =data['results'][0]['geometry']['location']['lng']
	return lat, lng
def get_weather_soil_data(lat, lng):
	cache_session = requests_cache.CachedSession('.cache', expire_after = 7200)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	url = "https://historical-forecast-api.open-meteo.com/v1/forecast"

	params = {
		"latitude": lat,
		"longitude": lng,
		"start_date": '2023-06-13',
		"end_date": '2024-06-13',
		"hourly": ["temperature_2m", "soil_temperature_6cm", "soil_moisture_3_to_9cm", "rain"],
		"temperature_unit": "fahrenheit",
		"wind_speed_unit": "mph",
		"precipitation_unit": "inch",
		"models": "best_match"
	}
	
	responses = openmeteo.weather_api(url, params=params)
	response = responses[0]
	

	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_rain = hourly.Variables(1).ValuesAsNumpy()
	hourly_soil_temperature_6cm = hourly.Variables(2).ValuesAsNumpy()
	hourly_soil_moisture_3_to_9cm = hourly.Variables(3).ValuesAsNumpy()
	

	
	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}
	

	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["rain"] = hourly_rain
	hourly_data["soil_temperature_6cm"] = hourly_soil_temperature_6cm
	hourly_data["soil_moisture_3_to_9cm"] = hourly_soil_moisture_3_to_9cm
	attrs = {}
	hourly_dataframe = pd.DataFrame(data = hourly_data)

	avg_soil_temp = hourly_dataframe.loc[:, 'soil_temperature_6cm'].mean()
	avg_soil_moisture = hourly_dataframe.loc[:, 'soil_moisture_3_to_9cm'].mean()
	avg_temp = hourly_dataframe.loc[:, 'temperature_2m'].median()
	avg_rain = hourly_dataframe.loc[:, 'rain'].mean()
	
	attrs['rain'] = avg_rain
	attrs['temperature'] = avg_temp
	attrs['avg_soil_temp'] = avg_soil_temp
	attrs['avg_soil_moist'] = avg_soil_moisture
	attrs['climate'] = lookupCZ(lat, lng)
	return attrs

