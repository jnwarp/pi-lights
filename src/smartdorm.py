import os
import argparse
import time
import web
import lights

rgb1 = (20, 16, 21)
rgb2 = (13, 26, 19)

strip1 = lights.LightStrip(rgb1)
strip2 = lights.LightStrip(rgb2)

occupied = False
cp = web.ControlPanel()

def fadeColors(color):
	strip1.fadeColor(color)
	strip2.fadeColor(color)

def doorChanged(value):
	if value:
		print('Door sensor closed.')
	else:
		print('Door sensor open!')
		os.system('aplay /home/james/pi-lights/src/sounds/keypad_door_open.wav &')
		cp.commandSend('fadeColors', 'white')

def motionChanged(value):
	global occupied
	cp.outputSet('motion_led', value)
	if not(occupied):
		cp.commandSend('fadeColors', 'seagreen')
	occupied = True

def emptyRoom():
	global occupied
	cp.commandSend('fadeColors', 'black')
	occupied = False

def runLights():
	cp.commandAdd('fadeColors', fadeColors)
	cp.startServer()

def runDoor():
	# setup door sensor
	cp.inputAdd('door', 20, doorChanged)
	cp.outputAdd('door', 21, True)

	# setup motion sensor
	cp.inputAdd('motion', 17, motionChanged)
	cp.outputAdd('motion_led', 27, True)
	cp.eventAdd(
		name = 'empty_room',
		sensor = 'motion',
		triggers = {
			'state': False,
			'diff': 60*30,
			'run_once': True
		},
		callback = emptyRoom
	)

	# start web server, no more code will be executed
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
