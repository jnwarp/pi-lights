import argparse
import lights.py

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Choose the Pi')

    parser.add_argument('--door', dest='piPlatform', action='store_const',
        const='door',
        help='runs the "door" Raspberry Pi')
    parser.add_argument('--lights', dest='piPlatform', action='store_const',
        const='lights',
        help='runs the "lights" Raspberry Pi')

    args = parser.parse_args()
    print(args.piPlatform)


def lights:
    if(--lights):
        strip1 = LightStrip(rgb1)
        strip2 = LightStrip(rgb2)

        while True:
            strip1.setColor('orange')
            strip2.setColor('orange')
