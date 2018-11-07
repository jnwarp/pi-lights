import cherrypy
import json
import os
import pigpio
import time

class ControlPanel(object):
	inputs = {
		'door': {
			'name': 'door_sensor',
			'pin': 20,
			'state': 0,
			'last_state': None,
			'last_change': 0,
			'time_diff': 0
		},
		'motion': {
			'name': 'motion_sensor',
			'pin': 4,
			'state': 0,
			'last_state': None,
			'last_change': 0,
			'time_diff': 0
		}
	}

	outputs = {
		'motion_led': {
			'name': 'motion_led',
			'pin': 17,
			'state': 0,
			'last_state': None,
			'last_change': 0
		}
	}

	events = {
		'person_leaves': {
			'name': 'person_gone',
			'input': 'motion',
			'input_state': 0,
			'input_delay': 15,
			'run_once': True,
			'last_change': 0,
		}
	}


	pi = pigpio.pi()

	def __init__(self):
		self.path = '.'

		# setup input/output pins
		self.setupInputPins()

		# start background loop
		wd = cherrypy.process.plugins.BackgroundTask(2, self.backgroundLoop)
		wd.start()

	def backgroundLoop(self):
		while True:
			time.sleep(0.1)

			# check for input changes
			for item in self.inputs:
				sensor = self.inputs[item]
				sensor['state'] = self.pi.read(sensor['pin'])

				if sensor['state'] != sensor['last_state']:
					sensor['time_diff'] = time.time() - sensor['last_change']
					self.sensorChanged(sensor)

					sensor['last_state'] = sensor['state']
					sensor['last_change'] = time.time()

			# run code to update states
			for item in self.events:
				event = self.events[item]
				for item2 in self.inputs:
					if event['input'] == item2:
						self.eventUpdate(event, sensor)

			# write output pins
			for item in self.outputs:
				output = self.outputs[item]
				self.pi.write(output['pin'], output['state'])

		return
	
	def sensorChanged(self, sensor):
		if sensor['name'] == 'door_sensor':
			if sensor['last_state'] == 1:
				motion = self.inputs['motion']
				delay = time.time() - motion['last_change']
				print(motion)
				print(delay)
				if delay > 20 or (delay < 1 and motion['state'] == 1):
					print('Welcome back')
				else:
					print('Goodbye')
				os.system('aplay /home/james/pi-lights/src/sounds/keypad_door_open.wav &')

		if sensor['name'] == 'motion_sensor':
			self.outputs['motion_led']['state'] = sensor['state']

	def eventUpdate(self, event, sensor):
		debug = False

		if event['input_state'] != sensor['state']:
			if debug:
				print('wrong state', sensor['state'])
			return

		if event['input_delay'] > time.time() - sensor['last_change']:
			if debug:
				print('wrong delay', time.time() - sensor['last_change'])
			return

		if event['run_once']:
			if event['last_change'] == sensor['last_change']:
				if debug:
					print('already ran')
				return

		print(event)

		if event['name'] == 'person_gone':
			print('TURN OFF LIGHTS')

		event['last_change'] = sensor['last_change']
	
	@cherrypy.expose
	def index(self):
		return self.readFile(self.path + '/html/index.html')
	
	@cherrypy.expose
	def getInputs(self, force=False):
		return json.dumps(self.inputs)

	@cherrypy.expose
	def setOutput(self, name, state):
		if name in self.outputs:
			self.outputs[name]['state'] = int(state)
	
	def readFile(self, file):
		f = open(file, 'r')
		return f.read()
	
	def setupInputPins(self):
		for item in self.inputs:
			sensor = self.inputs[item]

			print('Input ' + sensor['name'], sensor['pin'])

			self.pi.set_mode(sensor['pin'], pigpio.INPUT)
			self.pi.set_pull_up_down(sensor['pin'], pigpio.PUD_DOWN)

		for item in self.outputs:
			output = self.outputs[item]

			print('Output ' + output['name'], output['pin'])
			self.pi.set_mode(output['pin'], pigpio.OUTPUT)
	
	def startServer(self, port=8080):
		conf = {
			'/static': {
				'tools.staticdir.root': os.path.abspath(os.getcwd()),
				'tools.staticdir.on': True,
				'tools.staticdir.dir': self.path + '/html'
			}
		}

		cherrypy.config.update({'server.socket_port': port})
		cherrypy.config.update({'server.socket_host': '0.0.0.0'})
		cherrypy.quickstart(self, '/', conf)

if __name__ == '__main__':
	cp = ControlPanel()
	cp.startServer()
