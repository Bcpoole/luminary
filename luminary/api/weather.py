import json

import requests

from luminary.util import project


def get_forecast():
    """
    Get Forecast for day. If it's nighttime, it'll get the forecast for the next day period.
    Unfortunately Underground Weather discontinued their API so using weather.gov.

    :return: Forecast dictionary
    """
    response = requests.get(f"https://api.weather.gov/points/{X},{Y}")
    data = json.loads(response.content)
    periods = json.loads(requests.get(data['properties']['forecast']).content)['properties']['periods']
    if periods[0]['isDaytime']:
        return periods[0]
    else:
        return periods[1]


def get_temperature(forecast=None, degrees_fahrenheit=True):
    """
    Get temperature degrees.

    :param forecast: Forecast dictionary. Will GET forecast if None.
    :param degrees_fahrenheit: Degrees F if true, else degrees C
    :return: Degrees float
    """
    if forecast is None:
        forecast = get_forecast()

    temperature = forecast['temperature']
    if degrees_fahrenheit:
        if forecast['temperatureUnit'] == 'C':
            temperature = temperature * 1.8 + 32
        return temperature
    else:
        if forecast['temperatureUnit'] == 'F':
            temperature = (temperature - 32) / 1.8
        return temperature


def encode_forecast(forecast=None):
    """
    Deciphers forecast and encodes it to dictionary.

    :param forecast: Forecast dictionary. Will GET forecast if None.
    :return: Encoded weather dictionary
    """
    if forecast is None:
        forecast = get_forecast()
    short_forecast = forecast['shortForecast'].lower()

    # oddly the only way to get rain chance is from the icon
    simple_forecast = forecast['icon'].replace('?size=medium', '').split('/')
    simple_forecast = simple_forecast[simple_forecast.index('day') + 1:]

    def simple_forecast_contains(keys):
        if type(keys) is list:
            return any(key in simple_forecast for key in keys)
        else:
            return keys in simple_forecast

    weather = {
        'rain_chance': 0,
        'temperature': get_temperature(forecast),
        'thunderstorms': False,
        'cloud_level': 0,  # Sunny
    }

    if simple_forecast_contains(['rain', 'tsra']):
        weather['rain_chance'] = max(map(lambda x: int(x.split(',')[1]), filter(lambda y: ',' in y, simple_forecast)))
    if simple_forecast_contains('tsra'):
        weather['thunderstorms'] = True
    if short_forecast != 'sunny':
        if short_forecast == 'mostly sunny':
            weather['cloud_level'] = 1
        elif short_forecast == 'partly cloudy':
            weather['cloud_level'] = 2
        elif short_forecast == 'mostly cloudy':
            weather['cloud_level'] = 3
        else:
            weather['cloud_level'] = 4

    return weather


config = project.load_config('weather.ini')
X = config['DEFAULT']['loc_x']
Y = config['DEFAULT']['loc_y']
