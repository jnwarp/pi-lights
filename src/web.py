import cherrypy
import json
import os
import pigpio
import time

class ControlPanel(object):
	""" Variables """
	inputs = {
		'door': {
			'name': 'door_sensor',
			'pin': 20,
			'state': 0,
			'last_state': None,
			'last_change': 0
		},
		'motion': {
			'name': 'motion_sensor',
			'pin': 4,
			'state': 0,
			'last_state': None,
			'last_change': 0
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
			for item in self.inputs:
				sensor = self.inputs[item]
				sensor['state'] = self.pi.read(sensor['pin'])

				if sensor['state'] != sensor['last_state']:
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
						else:
							time.sleep(.4)
							#os.system('aplay /home/james/pi-lights/src/sounds/keypad_door_clank.wav &')

					if sensor['name'] == 'motion_sensor':
						self.outputs['motion_led']['state'] = sensor['state']

					sensor['last_state'] = sensor['state']
					sensor['last_change'] = time.time()

			for item in self.outputs:
				output = self.outputs[item]
				self.pi.write(output['pin'], output['state'])

		return
	
	@cherrypy.expose
	def index(self):
		return self.readFile(self.path + '/html/index.html')
	
	@cherrypy.expose
	def getInputs(self, force=False):
		return json.dumps(self.inputs)
	
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
