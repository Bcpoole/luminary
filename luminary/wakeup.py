#!/usr/bin/env python
import time

from luminary.api import lifx, lifx_effects, weather
from luminary.api.lifx import HSBK


def wakeup():
    """
    Wakeup light, delay minute for wake up laziness, then report weather.
    """
    lifx.turn_on(brightness=1)
    time.sleep(60)  # wait 1 minute to report weather
    report_weather()


def report_weather():
    """
    Blink colors for temperature, rain chance, thunder storms, and cloud level.
    """
    weather_report = weather.encode_forecast()

    def transition():
        """
        Blink green to indicate transition.
        """
        lifx_effects.pulse('green', period=2)
        time.sleep(2)

    transition()
    transition()

    # Temperature
    temperature = weather_report['temperature']
    # these values are all subjective to what I think is very hot, hot, etc.
    if temperature >= 95:  # dark red
        lifx_effects.pulse(
            HSBK({'hue': 7.031357289997711, 'saturation': 0.979995422293431, 'kelvin': 4000}), period=2)
    elif temperature >= 85:  # red
        lifx_effects.pulse(
            HSBK({'hue': 7.031357289997711, 'saturation': 0.6299992370489051, 'kelvin': 4000}), period=2)
    elif temperature >= 78:  # orange
        lifx_effects.pulse(
            HSBK({'hue': 42.188143739986266, 'saturation': 0.9726710917830167, 'kelvin': 4000}), period=2)
    elif temperature >= 68:  # yellow
        lifx_effects.pulse(
            HSBK({'hue': 45.00068665598535, 'saturation': 1, 'kelvin': 4000}), period=2)
    elif temperature >= 60:  # sunny white
        lifx_effects.pulse(
            HSBK({'hue': 237.65987640192265, 'saturation': 0, 'kelvin': 3500}), period=2)
    elif temperature >= 50:  # light blue
        lifx_effects.pulse(
            HSBK({'hue': 177.19020370794232, 'saturation': 0.7199969481956207, 'kelvin': 4000}), period=2)
    else:  # snowy white
        lifx_effects.pulse(
            HSBK({'hue': 237.65987640192265, 'saturation': 0, 'kelvin': 9000}), period=2)

    transition()

    # Precipitation
    precipitation_chance = weather_report['precipitation_chance']
    if precipitation_chance == 0:  # sunny white
        lifx_effects.pulse(
            HSBK({'hue': 237.65987640192265, 'saturation': 0, 'kelvin': 3500}), period=2)
    elif precipitation_chance <= 25:  # white blue
        lifx_effects.pulse(
            HSBK({'hue': 177.19020370794232, 'saturation': 0.4399938963912413, 'kelvin': 4000}), period=2)
    elif precipitation_chance <= 50:  # light blue
        lifx_effects.pulse(
            HSBK({'hue': 177.19020370794232, 'saturation': 0.7199969481956207, 'kelvin': 4000}), period=2)
    elif precipitation_chance <= 75:  # blue
        lifx_effects.pulse(
            HSBK({'hue': 202.50308995193407, 'saturation': 0.7199969481956207, 'kelvin': 4000}), period=2)
    else:  # dark blue
        lifx_effects.pulse(
            HSBK({'hue': 220.78461890592814, 'saturation': .9, 'kelvin': 4000}), period=2)

    if weather_report['thunderstorms']:  # yellow
        lifx_effects.pulse(
            HSBK({'hue': 45.00068665598535, 'saturation': 1, 'kelvin': 4000}), period=2)
    if weather_report['snow']:  # snowy white
        lifx_effects.pulse(
            HSBK({'hue': 237.65987640192265, 'saturation': 0, 'kelvin': 9000}), period=2)

    transition()

    # Cloud Level
    cloud_dim = 100 - (25 * weather_report['cloud_level'])
    lifx.turn_on(brightness=cloud_dim)
    time.sleep(1)
    lifx.turn_on(brightness=1)

    transition()
    transition()


if __name__ == '__main__':
    wakeup()
