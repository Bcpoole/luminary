#!/usr/bin/env python

from luminary.api import lifx
from luminary.api import ultrasonic_depth_sensor as uds


def listen():
    while True:
        triggered = uds.detect()
        if triggered:
            lifx.toggle_power()


if __name__ == '__main__':
    uds.setup_pins()
    listen()
