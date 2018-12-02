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

	def __init__(self):
		self.path = '.'

		# setup network
		self.cmd = commandSend.CommandSend(
			self.token,
			url="http://172.16.16.61:8080/"
		)
	
	def commandAdd(self, command, function):
		self.commands[command] = function

	@cherrypy.expose
	def commandReceive(self, key, command, data = {}):
		if key != self.token:
			print('Error: bad key given')
			return

		print('Command: ' + command)
		self.commands[command](data)

	@cherrypy.expose
	def commandSend(self, command, data = {}):
		print('Sending command: ' + command)
		self.cmd.send(command, data)

	@cherrypy.expose
	def index(self):
		return self.readFile(self.path + '/html/index.html')

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
