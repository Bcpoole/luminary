import configparser
import requests
import json
import time


class HSBK:
    def __init__(self, color, brightness=None):
        if type(color) is str:
            response = requests.get(f"https://api.lifx.com/v1/color?string={color}", headers=headers)
            color = json.loads(response.content)

        self.hue = color['hue']
        self.saturation = color['saturation']
        if brightness is not None:
            self.brightness = color['brightness']
        elif brightness in color:
            self.brightness = color['brightness']
        else:
            self.brightness = 1.0
        self.kelvin = color['kelvin']

    @staticmethod
    def encode_color(color):
        color_str = []
        if color.hue is not None:
            color_str.append(f"hue:{color.hue}")
        if color.saturation is not None:
            color_str.append(f"saturation:{color.saturation}")
        if color.brightness is not None:
            color_str.append(f"brightness:{color.brightness}")
        if color.kelvin is not None:
            color_str.append(f"kelvin:{color.kelvin}")

        return ' '.join(color_str)


def turn_on(color=None, brightness=None, duration=None):
    payload = {"power": "on"}

    if color:
        payload = HSBK.encode_color(color)
    if brightness is not None:
        payload['brightness'] = brightness
    if duration is not None:
        payload['duration'] = duration

    set_state(payload)


def turn_off(duration=None):
    payload = {
        "power": "off",
    }

    if duration:
        payload['duration'] = duration

    set_state(payload)


def toggle_power():
    status = get_status()
    if status['power'] == 'off':
        turn_off()
    else:
        turn_on()


def blink_power(blinks=1):
    for _ in range(blinks):
        toggle_power()
        time.sleep(.25)
        toggle_power()
        time.sleep(.25)


def blink_color(blinks=1, duration=0.0, color=None):
    status = get_status()

    if color is not None:
        color = HSBK(color)

    base_payload = {
        "power": status['power'],
        "duration": duration,
        "color": HSBK.encode_color(HSBK(status['color'])),
    }

    blink_payload = {
        "power": "on",
        "duration": duration,
    }
    if color:
        blink_payload['color'] = HSBK.encode_color(color)

    for _ in range(blinks):
        set_state(blink_payload)
        time.sleep(.25)
        set_state(base_payload)
        time.sleep(.25)


def set_state(payload):
    response = requests.put(f"https://api.lifx.com/v1/lights/id:{id}/state", headers=headers, data=payload)
    if response.ok:
        resp = json.loads(response.content)
        if type(resp) is list:
            return resp[0]
        else:
            return resp
    else:
        raise requests.exceptions.HTTPError(response.status_code)


def get_status():
    response = requests.get(f"https://api.lifx.com/v1/lights/id:{id}", headers=headers)
    if response.ok:
        return json.loads(response.content)[0]
    else:
        raise requests.exceptions.HTTPError(response.status_code)


config = configparser.ConfigParser()
config.read('../config/lifx.ini')
headers = {
    "Authorization": f"Bearer {config['DEFAULT']['api_key']}",
}

id = config['DEFAULT']['light_id']
