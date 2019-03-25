import time  # Import time library

import RPi.GPIO as GPIO  # Import GPIO library
from luminary.util import project


def setup_pins():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)


def detect():
    GPIO.output(TRIG, False)
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150  # Multiply pulse duration by 17150 to get distance

    return distance < 6


config = project.load_config('raspberry-pi.ini')
TRIG = int(config['DEFAULT']['uds_trig'])
ECHO = int(config['DEFAULT']['uds_echo'])
