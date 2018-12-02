import argparse
import lights
import time
import web

rgb1 = (20, 16, 21)
rgb2 = (13, 26, 19)

strip1 = lights.LightStrip(rgb1)
strip2 = lights.LightStrip(rgb2)

def fadeColors(color):
	strip1.fadeColor(color)
	strip2.fadeColor(color)

def runLights():
	cp = web.ControlPanel()
	cp.commandAdd('fadeColors', fadeColors)
	cp.startServer()

def runDoor():
	cp = web.ControlPanel()
	cp.startServer()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Choose the Pi')

	parser.add_argument('--door', dest='piPlatform', action='store_const',
		const='door',
		help='runs the "door" Raspberry Pi')
	parser.add_argument('--lights', dest='piPlatform', action='store_const',
		const='lights',
		help='runs the "lights" Raspberry Pi')

	args = parser.parse_args()

	if args.piPlatform == 'lights':
		runLights()
	if args.piPlatform == 'door':
		runDoor()
