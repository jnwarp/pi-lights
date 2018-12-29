import cherrypy
import json
import os
import pigpio
import time
import commandSend

class ControlPanel(object):
	token = 'GIv2YLNiiuJwwDl359OizFEIsAmS1c7xHbq4eLU5PjGvmAeofXRundKFb3hHQLe'
	pi = pigpio.pi()
	commands = {}
	inputs = {}
	outputs = {}
	events = {}

	def test(self, data):
		print('data:', data)

	def __init__(self):
		self.path = '.'

		# setup network
		self.cmd = commandSend.CommandSend(
			self.token,
			url="http://172.16.16.61:8080/"
		)

		# add test function
		self.commandAdd('test', self.test)

		# set up input read
		wd = cherrypy.process.plugins.BackgroundTask(2, self.inputReads)
		wd.start()

	
	def commandAdd(self, command, function):
		self.commands[command] = function
		print(self.commands)

	@cherrypy.expose
	def commandReceive(self, key, command, data = ''):
		if key != self.token:
			print('Error: bad key given')
			return

		print('Command: ', command, data)
		print('Available commands: ', self.commands)
		self.commands[command](data)

	@cherrypy.expose
	def commandSend(self, command, data = ''):
		print('Sending command: ', command, data)
		self.cmd.send(command, data)

	@cherrypy.expose
	def index(self):
		return self.readFile(self.path + '/html/index.html')
	
	def eventAdd(self, name, sensor, triggers, callback):
		self.events[name] = {
			'sensor': sensor,
			'triggers': triggers,
			'callback': callback,
			'last_change': time.time(),
			'last_state': None,
			'executed': False
		}
	
	def eventRead(self, name):
		event = self.events[name]
		state = self.inputs[event['sensor']][1]
		last_state = event['last_state']
		
		if state != last_state:
			event['last_state'] = state
			event['last_change'] = time.time()
			event['executed'] = False
			self.events[name] = event

		# calculate time difference
		diff = time.time() - event['last_change']

		trigger = event['triggers']
		if trigger['state'] != state and trigger['state'] != None:
			return
		if trigger['diff'] > diff and trigger['diff'] != None:
			return
		if trigger['run_once'] and event['executed']:
			return

		# trigger event
		self.events[name]['executed'] = True
		event['callback']()
				
	
	def inputAdd(self, name, pin, callback, freq = 1):
		print('Input', name)
		self.inputs[name] = (pin, 0, callback)
		self.pi.set_mode(pin, pigpio.INPUT)
		self.pi.set_pull_up_down(pin, pigpio.PUD_DOWN)

	
	def inputRead(self, name):
		pin, oldValue, callback = self.inputs[name]

		newValue = self.pi.read(pin)
		if oldValue != newValue:
			callback(newValue)

		self.inputs[name] = (pin, newValue, callback)
	
	def inputReads(self):
		while True:
			time.sleep(0.1)

			for item in self.inputs:
				self.inputRead(item)

			for event in self.events:
				self.eventRead(event)
	
	def outputAdd(self, name, pin, value=True):
		print('Output', name, value)
		self.outputs[name] = (pin, value)
		self.pi.set_mode(pin, pigpio.OUTPUT)
		self.pi.write(pin, value)
	
	def outputSet(self, name, value):
		print('Set output:', name, value)
		pin, oldValue = self.outputs[name]
		self.outputs[name] = (pin, value)
		self.pi.write(pin, value)

	def readFile(self, file):
		f = open(file, 'r')
		return f.read()

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
