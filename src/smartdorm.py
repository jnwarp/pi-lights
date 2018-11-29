import argparse
import lights

def lights():

    strip1 = LightStrip(rgb1)
    strip2 = LightStrip(rgb2)
def setColor(self, color = 'white', brightness = 255):
    # get the rgb color value ex (255, 255, 0)
    if type(color) == str:
        rgb = self.colors[color]
    else:
        rgb = color

    for i in range(3):
        # skip unset pins
        if self.pins[i] < 1:
            continue

        # set the color for each pin
        level = int(rgb[i] * (brightness / 255))
        self.pi.set_PWM_dutycycle(self.pins[i], level)

    # save the current color rgbNow = list(rgb) rgbNow.append(brightness)
    rgb = list(rgb)
    rgb.append(brightness)
    self.currentColor = tuple(rgb)

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
        strip1 = LightStrip(rgb1)
        strip2 = LightStrip(rgb2)
        while True:
            strip1.setColor('orange')
            strip2.setColor('orange')
