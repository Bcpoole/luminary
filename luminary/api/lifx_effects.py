import json
import math

import requests

from luminary.api import lifx
from luminary.api.lifx import HSBK


def breathe(color, from_color=None, period=1.0, cycles=1.0, persist=False, power_on=True, peak=0.5):
    """
    https://api.developer.lifx.com/docs/breathe-effect
    Performs a breathe effect by slowly fading between the given colors. Use the parameters to tweak the effect.

    :param color: The color to use for the breathe effect.
    :param from_color: The color to start the effect from. If this parameter is omitted then the color the bulb is
                       currently set to is used instead.
    :param period: The time in seconds for one cycle of the effect.
    :param cycles: The number of times to repeat the effect.
    :param persist: If false set the light back to its previous value when effect ends,
                    if true leave the last effect color.
    :param power_on: If true, turn the bulb on if it is not already on.
    :param peak: Defines where in a period the target color is at its maximum. Minimum 0.0, maximum 1.0.
    """
    payload = {
        "color": HSBK(color).encode(),
        "period": period,
        "cycles": cycles,
        "persist": persist,
        "power_on": power_on,
        "peak": peak,
    }
    if from_color is not None:
        payload['from_color'] = HSBK(from_color).encode()

    post_effect("breathe", payload)


def move(direction="forward", period=1.0, cycles=math.inf, power_on=True):
    """
    https://api.developer.lifx.com/docs/move-effect
    Performs a move effect on a linear device with zones, by moving the current pattern across the device.
    Use the parameters to tweak the effect.

    Warning: I only have one light at time of writing this so I only wrote this to support one light.

    :param direction: Move direction, can be forward or backward.
    :param period: The time in seconds for one cycle of the effect.
    :param cycles: The number of times to move the pattern across the device. Special cases are 0 to switch the effect
                   off, and unspecified to continue indefinitely.
    :param power_on: Switch any selected device that is off to on before performing the effect.
    """
    payload = {
        "direction": direction,
        "period": period,
        "power_on": power_on,
    }
    if cycles != math.inf:
        payload['cycles'] = cycles

    post_effect("move", payload)


def morph(palette, period=5.0, duration=math.inf, power_on=True):
    """
    https://api.developer.lifx.com/docs/morph-effect
    Performs a morph effect on the tiles in your selector. Use the parameters to tweak the effect.
    Note that the brightness of the morph is determined by the brightness of the tile, rather than the brightness of the
    colours in the palette. To change the brightness, use the SetState endpoint.

    Warning: I don't have LIFX tiles so this is untested other than status.ok.

    :param period:  This controls how quickly the morph runs. It is measured in seconds.
                    A lower number means theanimation is faster
    :param duration: How long the animation lasts for in seconds. Not specifying a duration makes the animation never
                     stop. Specifying 0 makes the animation stop. Note that there is a known bug where the tile remains
                     in the animation once it has completed if duration is nonzero.
    :param palette: You can control the colors in the animation by specifying a list of color specifiers.
    :param power_on: Switch any selected device that is off to on before performing the effect.
    """

    payload = {
        "period": period,
        "palette": palette,
        "power_on": power_on,
    }
    if duration != math.inf:
        payload['duration'] = duration

    post_effect("morph", payload)


def flame(period=5, duration=math.inf, power_on=True):
    """
    https://api.developer.lifx.com/docs/flame-effect
    Performs a flame effect on the tiles in your selector. Use the parameters to tweak the effect.
    Note that the brightness of the flame is determined by the brightness of the tile.
    To change the brightness, use the SetState endpoint.

    Warning: I don't have LIFX tiles so this is untested other than status.ok.

    :param period: This controls how quickly the flame runs. It is measured in seconds.
                   A lower number means the animation is faster
    :param duration: How long the animation lasts for in seconds. Not specifying a duration makes the animation never
                     stop. Specifying 0 makes the animation stop. Note that there is a known bug where the tile remains
                     in the animation once it has completed if duration is nonzero.
    :param power_on: Switch any selected device that is off to on before performing the effect.
    """
    payload = {
        "period": period,
        "power_on": power_on,
    }

    if duration != math.inf:
        payload['duration'] = math.inf

    post_effect("flame", payload)


def pulse(color, from_color=None, period=1.0, cycles=1.0, persist=False, power_on=True):
    """
    https://api.developer.lifx.com/docs/pulse-effect
    Performs a pulse effect by quickly flashing between the given colors. Use the parameters to tweak the effect.

    :param color: The color to use for the pulse effect.
    :param from_color: The color to start the effect from. If this parameter is omitted then the color the bulb is
                       currently set to is used instead.
    :param period: The time in seconds for one cycles of the effect.
    :param cycles: The number of times to repeat the effect.
    :param persist: If false set the light back to its previous value when effect ends,
                    if true leave the last effect color.
    :param power_on: If true, turn the bulb on if it is not already on.
    """
    payload = {
        "color": HSBK(color).encode(),
        "period": period,
        "cycles": cycles,
        "persist": persist,
        "power_on": power_on,
    }
    if from_color is not None:
        payload['from_color'] = HSBK(from_color).encode()

    post_effect("pulse", payload)


def effects_off(power_off=False):
    """
    https://api.developer.lifx.com/docs/effects-off
    Turns off any running effects on the device. This includes any waveform (breathe or pulse) as well as
    Tile or Multizone firmware effects.
    Also, if you specify power_off as true then the lights will also be powered off.

    :param power_off: If true, the devices will also be turned off.
    """
    payload = {"power_off": power_off}
    post_effect("off", payload)


def post_effect(effect, payload):
    """
    Formats payload and POST to given effect api.

    :param effect: Effect to use.
    :param payload: JSON payload.
    """
    response = requests.post(f"https://api.lifx.com/v1/lights/id:{id}/effects/{effect}",
                             headers=headers, data=json.dumps(payload))
    if not response.ok:
        raise requests.exceptions.HTTPError(response.status_code, response.reason, response.content)


headers = {
    "Authorization": f"Bearer {lifx.config['DEFAULT']['api_key']}",
}

id = lifx.config['DEFAULT']['light_id']
