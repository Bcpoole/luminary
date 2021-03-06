import configparser
import os


def setup_configs():
    setup_lifx()
    setup_raspberry_pi()
    setup_weather()


def setup_lifx():
    config_file = f"{config_dir}/lifx.ini"
    if os.path.exists(config_file):
        print('LIFX already set up.')
        return
    print('Setting up LIFX...')

    config = gen_config()

    config['DEFAULT']['api_key'] = input('API Key: ')
    config['DEFAULT']['light_id'] = input('Light Bulb id: ')

    with open(config_file, 'w') as configfile:
        config.write(configfile)


def setup_raspberry_pi():
    config_file = f"{config_dir}/raspberry-pi.ini"
    if os.path.exists(config_file):
        print('Raspberry Pi already set up.')
        return
    print('Setting up Raspberry Pi...')

    config = gen_config()

    config['DEFAULT']['uds_trig'] = input('Ultrasonic Depth Sensor TRIG: ')
    config['DEFAULT']['uds_echo'] = input('Ultrasonic Depth Sensor ECHO: ')

    with open(config_file, 'w') as configfile:
        config.write(configfile)


def setup_weather():
    config_file = f"{config_dir}/weather.ini"
    if os.path.exists(config_file):
        print('Weather already set up.')
        return
    print('Setting up Weather...')

    config = gen_config()

    print('Coordinates are rounded to 3 decimal places.')
    config['DEFAULT']['loc_x'] = "{:.3f}".format(float(input('X coord: ')))
    config['DEFAULT']['loc_y'] = "{:.3f}".format(float(input('Y coord: ')))

    with open(config_file, 'w') as configfile:
        config.write(configfile)


def gen_config():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {}
    return config


if __name__ == '__main__':
    config_dir = 'config'
    os.makedirs(config_dir, exist_ok=True)
    setup_configs()
