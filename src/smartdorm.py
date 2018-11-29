import argparse
import lights


def lights():

    strip1 = lights.LightStrip(rgb1)
    strip2 = lights.LightStrip(rgb2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Choose the Pi')

    parser.add_argument('--door', dest='piPlatform', action='store_const',
        const='door',
        help='runs the "door" Raspberry Pi')
    parser.add_argument('--lights', dest='piPlatform', action='store_const',
        const='lights',
        help='runs the "lights" Raspberry Pi')

    args = parser.parse_args()

    if (args.piPlatform == 'lights'):
        strip1 = lights.LightStrip(rgb1)
        strip2 = lights.LightStrip(rgb2)
        while True:
            strip1.setColor('orange')
            strip2.setColor('orange')
