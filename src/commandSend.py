from requests import Session
from requests_toolbelt import MultipartEncoder

class CommandSend():
	def __init__(self, token, url='https://localhost/', verify=False):
		self.url = url
		self.verify = verify
		self.session = Session()
		self.token = token

		# get cookie headers
		self.session.head(self.url, verify=self.verify)

	def send(self, command, data={}):
		response = self.session.post(
			url = self.url + 'commandReceive',
			params = {
				'token': self.token,
				'command': command
			},
			data = data,
			headers = header,
			verify = self.verify
		)

		print(response.text)
		return response
