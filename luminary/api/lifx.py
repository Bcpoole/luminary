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
    """
    Turns on the light. Sets to given color and brightness if given; Uses fast query if both are not.

    :param color: Color to set light to.
    :param brightness: The brightness level from 0.0 to 1.0. Overrides any brightness set in color (if any).
    :param duration: How long in seconds you want the power action to take. Range: 0.0 – 3155760000.0 (100 years).
    """
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
    """
    Turns off light with the fast query.

    :param duration: How long in seconds you want the power action to take. Range: 0.0 – 3155760000.0 (100 years).
    """
    payload = {
        "power": "off",
        "duration": duration,
        "fast": True,
    }

    set_state(payload)


def toggle_power():
    """
    https://api.developer.lifx.com/docs/toggle-power
    Turn off lights if any of them are on, or turn them on if they are all off.
    All lights matched by the selector will share the same power state after this action.
    Physically powered off lights are ignored.
    """
    requests.post(f"https://api.lifx.com/v1/lights/id:{id}/toggle", headers=headers)


def blink_power(cycles=1, period=.25, persist=False):
    """
    Blink the power state.
    :param cycles: The number of times to repeat the effect.
    :param period: The time in seconds for one cycles of the effect.
    :param persist: If false set the light back to its previous value when effect ends,
                    if true leave the last effect color.
    """
    for i in range(cycles):
        toggle_power()
        time.sleep(period)
        if not (i == cycles - 1 and persist):
            toggle_power()
            time.sleep(period)


def set_state(payload):
    """
    https://api.developer.lifx.com/docs/set-state

    :param payload: Dict of state properties.
    """
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
    """
    https://api.developer.lifx.com/docs/list-lights
    Gets the status for the configured light.

    :return: Dictionary of properties for given light.
    """
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
