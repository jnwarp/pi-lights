import cherrypy
import json
import os
import pigpio
import time

class ControlPanel(object):
	""" Variables """
	inputs = {
		'door': {
			'pin': 2,
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
			for sensor in self.inputs:
				pin = self.inputs[sensor]['pin']
				self.inputs[sensor]['state'] = self.pi.read(pin)
				if self.inputs[sensor]['state'] != self.inputs[sensor]['last_state']:
					if sensor == 'door' and self.inputs[sensor]['last_state'] == 1 and time.time()-self.inputs[sensor]['last_change'] > (60*10):
						os.system('mpg321 /home/james/pi-lights/AI_welcome.mp3')
					self.inputs[sensor]['last_state'] = self.inputs[sensor]['state']
					self.inputs[sensor]['last_change'] = time.time()

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
		for sensor in self.inputs:
			pin = self.inputs[sensor]['pin']

			print(sensor, pin)

			self.pi.set_mode(pin, pigpio.PUD_DOWN)
	
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
