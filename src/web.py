import cherrypy
import os

class ControlPanel(object):
	def __init__(self):
		self.path = '.'
	
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
