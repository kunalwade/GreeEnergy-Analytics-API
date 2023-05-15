import requests
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
# from src.app.forecastEngine.view import getWeatherData
from src.app.models.analytics import Analytics as AnalyticsModel
from src.app.api.base.controller import BaseController
from src.app.database import db
# from src.app.models.analytics import Analytics

class AnalyticsController(BaseController):
    def __init__(self):
        super().__init__(AnalyticsModel)

    def _get_calculations(self, latitude, longitude, site_area):
        solar_power = self.get_solar_power(latitude, longitude,site_area)
        getcarbonfootprint = self.get_carbon_footprint(solar_power)
        getbreakeven = self.get_break_even(solar_power)
        return solar_power, getcarbonfootprint, getbreakeven


    def get_calculations(self, id: int):
        session = db.session()
        analytics = session.query(AnalyticsModel).get_or_404(id)

        latitude = analytics.site.latitude
        longitude = analytics.site.longitude
        site_area = analytics.site.site_area

        solar_power, getcarbonfootprint, getbreakeven = self._get_calculations(latitude, longitude, site_area)

        session=db.session()
        analytics.update(solar_power=solar_power, carbonfootprint=getcarbonfootprint, breakeven=getbreakeven)
        session.commit()
        return analytics

    def get_weather_data (self, latitude, longitude):
        url = f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=2022-01-01&end_date=2022-12-31&hourly=temperature_2m,precipitation,cloudcover,windspeed_10m,winddirection_10m'
        response = requests.get(url)
        data = json.loads(response.text)
        print("Data:",data)
        data = pd.DataFrame({
            'date': [d for d in data['hourly']['time']],
            'temperature': [d for d in data['hourly']['temperature_2m']],
            'precipitation': [d for d in data['hourly']['precipitation']],
            'cloud_cover': [d for d in data['hourly']['cloudcover']],
        })
        return data

    def get_solar_power (self, latitude, longitude, site_area):
        area_per_panel = 1.6
        number_solarcells = site_area / area_per_panel
        weather_data = self.get_weather_data(latitude, longitude)
        model = self.train_model(weather_data)
        y_pred = self.predict(weather_data, model)
        solar_irradiance = 1000 # W/m2
        panel_efficiency = 0.2
        solar_power_output = solar_irradiance * panel_efficiency * (1 - (y_pred[0][1]/ 100)) * (1 - 0.005 * (y_pred[0][0] -25)) * area_per_panel * number_solarcells
        return solar_power_output


    def get_break_even (self, solar_power):
        solar_electricity_price = 0.1 # in USD/kWh
        solar_cost = 1000000 # in USD
        solar_revenue = solar_power * solar_electricity_price
        solar_cost_per_year = solar_cost / 25
        solar_break_even_period = solar_cost_per_year / solar_revenue
        return solar_break_even_period

    def get_carbon_footprint (self, solar_power_output):
        solar_carbon_intensity = 0.5 # in kg CO2/kWh (assumed value)
        solar_carbon_avoided = solar_power_output * solar_carbon_intensity
        return solar_carbon_avoided


    def train_model (self, weather_data):
        train_data = weather_data[:-1]
        x_train = train_data[['temperature', 'precipitation', 'cloud_cover']]
        y_train = train_data[['temperature', 'cloud_cover']]
        model = LinearRegression().fit(x_train, y_train)
        return model

    def predict (self, weather_data, model):
        test_data = weather_data[-1:]
        x_test = test_data[['temperature', 'precipitation', 'cloud_cover']]
        y_pred = model.predict(x_test)
        return y_pred
