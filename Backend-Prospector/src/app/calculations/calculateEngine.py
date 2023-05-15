import requests
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def getWeatherData (lat, lon):
    url = f'https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date=2022-01-01&end_date=2022-12-31&hourly=temperature_2m,precipitation,cloudcover,windspeed_10m,winddirection_10m'
    response = requests.get(url)
    data = json.loads(response.text)
    data = pd.DataFrame({
        'date': [d for d in data['hourly']['time']],
        'temperature': [d for d in data['hourly']['temperature_2m']],
        'precipitation': [d for d in data['hourly']['precipitation']],
        'cloud_cover': [d for d in data['hourly']['cloudcover']],
    })
    return data

def getSolarPower (lat, lon, siteArea):
    areaPerPanel = 1.6
    number_solarcells = siteArea / areaPerPanel
    weather_data = getWeatherData(lat, lon)
    model = train_model(weather_data)
    y_pred = predict(weather_data, model)
    solar_irradiance = 1000 # W/m2
    panel_efficiency = 0.2
    solar_power_output = solar_irradiance * panel_efficiency * (1 - (y_pred[0][1]/ 100)) * (1 - 0.005 * (y_pred[0][0] -25)) * areaPerPanel * number_solarcells
    return solar_power_output

def train_model (weatherData):
    train_data = weatherData[:-1]
    X_train = train_data[['temperature', 'precipitation', 'cloud_cover']]
    y_train = train_data[['temperature', 'cloud_cover']]
    model = LinearRegression().fit(X_train, y_train)
    return model

def predict (weatherData, model):
    test_data = weatherData[-1:]
    X_test = test_data[['temperature', 'precipitation', 'cloud_cover']]
    y_pred = model.predict(X_test)
    print(y_pred)
    return y_pred


def getBreakEven (solar_power):
    solar_electricity_price = 0.1 # in USD/kWh
    solar_cost = 1000000 # in USD
    solar_revenue = solar_power * solar_electricity_price
    solar_cost_per_year = solar_cost / 25
    solar_break_even_period = solar_cost_per_year / solar_revenue
    return solar_break_even_period

def getCarbonFootprint (solar_power_output):
    solar_carbon_intensity = 0.5 # in kg CO2/kWh (assumed value)
    solar_carbon_avoided = solar_power_output * solar_carbon_intensity
    return solar_carbon_avoided

def main ():
    lat = 19.383884366282555
    lon = 75.03028459781545
    solar_out = getSolarPower(lat, lon, 1000)
    break_even = getBreakEven(solar_out)
    carbon_footprint = getCarbonFootprint(solar_out)
    print(solar_out, break_even, carbon_footprint)

main()
