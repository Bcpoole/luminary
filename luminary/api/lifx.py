import configparser
import json
import time

import requests


class HSBK:
    def __init__(self, color, brightness=None):
        """
        Hue Saturation Brightness Kelvin

        :param color: Either color name string of dict of HSBK values.
        :param brightness: Color brightness. Will set to 1.0 if None and color has no brightness value.
        """
        if type(color) is str:
            response = requests.get(f"https://api.lifx.com/v1/color?string={color}", headers=headers)
            color = json.loads(response.content)

        self.hue = color.get('hue')
        self.saturation = color.get('saturation')
        if brightness is not None:
            self.brightness = color['brightness']
        else:
            self.brightness = color.get('brightness', 1.0)
        self.kelvin = color.get('kelvin')

    def encode(self):
        """
        Gets LIFX API compatible string representation of color.

        :return: LIFX API color data string.
        """
        color_str = []
        if self.brightness is not None:
            color_str.append(f"brightness:{self.brightness}")
        if self.hue is not None:
            color_str.append(f"hue:{self.hue}")
        if self.saturation is not None:
            color_str.append(f"saturation:{self.saturation}")
        if self.kelvin is not None:
            color_str.append(f"kelvin:{self.kelvin}")

        return ' '.join(color_str)


def turn_on(color=None, brightness=None, duration=1.0):
    payload = {
        "power": "on",
        "duration": duration
    }

    if color:
        payload['color'] = HSBK(color).encode()
    if brightness is not None:
        payload['brightness'] = brightness
    if color is None and brightness is None:
        payload['fast'] = True

    set_state(payload)


def turn_off(duration=1.0):
    payload = {
        "power": "off",
        "duration": duration,
        "fast": True,
    }

    set_state(payload)


def toggle_power():
    requests.post(f"https://api.lifx.com/v1/lights/id:{id}/toggle", headers=headers)


def blink_power(blinks=1):
    for _ in range(blinks):
        toggle_power()
        time.sleep(.25)
        toggle_power()
        time.sleep(.25)


def blink_color(blinks=1, duration=0.0, color=None):
    status = get_status()

    base_payload = {
        "power": status['power'],
        "duration": duration,
        "color": HSBK.encode(HSBK(status['color'])),
    }

    blink_payload = {
        "power": "on",
        "duration": duration,
    }
    if color is not None:
        blink_payload['color'] = HSBK.encode(HSBK(color))

    for _ in range(blinks):
        set_state(blink_payload)
        time.sleep(.25)
        set_state(base_payload)
        time.sleep(.25)


def set_state(payload):
    response = requests.put(f"https://api.lifx.com/v1/lights/id:{id}/state", headers=headers, data=json.dumps(payload))
    if not response.ok:
        raise requests.exceptions.HTTPError(response.status_code, response.reason, response.content)


def cycle(states, defaults=None, direction='forward'):
    """
    https://api.developer.lifx.com/docs/cycle
    Make the light(s) cycle to the next or previous state in a list of states.

    :param states: Array of state hashes as per Set State. Must have 2 to 10 entries.
    :param defaults: Default values to use when not specified in each states[] object.
    :param direction: Direction in which to cycle through the list. Can be forward or backward.
    """
    payload = {
        "states": states,
        "direction": direction,
    }
    if defaults is not None:
        payload['defaults'] = defaults

    response = requests.post(f"https://api.lifx.com/v1/lights/id:{id}/cycle", headers=headers, data=json.dumps(payload))
    if not response.ok:
        raise requests.exceptions.HTTPError(response.status_code, response.reason, response.content)


def get_status():
    response = requests.get(f"https://api.lifx.com/v1/lights/id:{id}", headers=headers)
    if response.ok:
        return json.loads(response.content)[0]
    else:
        raise requests.exceptions.HTTPError(response.status_code, response.reason, response.content)


config = configparser.ConfigParser()
config.read('../config/lifx.ini')
headers = {
    "Authorization": f"Bearer {config['DEFAULT']['api_key']}",
}

id = config['DEFAULT']['light_id']
