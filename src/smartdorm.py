import argparse
import lights
import time

def runLights():
    rgb1 = (20, 16, 21)
    rgb2 = (13, 26, 19)

    strip1 = lights.LightStrip(rgb1)
    strip2 = lights.LightStrip(rgb2)

    strip1.fadeColor('red')
    time.sleep(1)
    strip1.fadeColor('green')
    time.sleep(1)
    strip1.fadeColor('blue')

    strip2.fadeColor('red')
    time.sleep(1)
    strip2.fadeColor('green')
    time.sleep(1)
    strip2.fadeColor('blue')

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
        runLights()
