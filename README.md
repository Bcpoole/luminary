# Luminary

Making your LIFX bulb smarter.

Currently only supports 1 bulb (as that's my personal setup).

## Setup
`python setup.py`

## Scripts
### light_switch
Let's you hook up a ultrasonic depth sensor (tested with HC-SR04) to a Raspberry Pi to serve as a light switch.

### wakeup
Turns on light at designated time and then reports the weather through colors and blinks.

## About
I wanted to make my LIFX bulb smarter, such as a depth sensor switch attached to the side of my night stand instead of arguing with Amazon Alexa I said "lights off", not "define off". Plus I wanted to encode daily weather in colors + flashes when I have it turn on in the morning.

I'm running this off a Raspberry Pi, and might include ESP32 support in the future.

## TODO
- support for LIFX Scenes (I don't currently have any set up)
