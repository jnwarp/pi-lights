from requests import Session

class CommandSend():
	def __init__(self, token, url='https://localhost/', verify=False):
		self.url = url
		self.verify = verify
		self.session = Session()
		self.token = token

	def send(self, command, data={}):
		response = self.session.post(
			url = self.url + 'commandReceive',
			params = {
				'key': self.token,
				'command': command
			},
			data = data,
			verify = self.verify
		)

		print(response.text)
		return response
