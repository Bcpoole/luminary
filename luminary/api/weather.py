import json

import requests

from luminary.util import project


def get_forecast():
    response = requests.get(f"https://api.weather.gov/points/{X},{Y}")
    data = json.loads(response.content)
    return json.loads(requests.get(data['properties']['forecast']).content)['properties']['periods'][0]


config = project.load_config('weather.ini')
X = config['DEFAULT']['loc_x']
Y = config['DEFAULT']['loc_y']
