#!/usr/bin/env python
import time

from luminary.api import lifx, weather


def wakeup():
    lifx.turn_on()
    time.sleep(60)  # wait 1 minute to report weather
    for _ in range(3):  # signal about to report weather
        lifx.blink_power()
    time.sleep(5)  # delay to not mix up blinks from warning
    report_weather()


def report_weather():
    pass


if __name__ == '__main__':
    wakeup()
