from requests import Session
class FacebookAPI():
	def __init__(self, username, password, url='https://localhost/', verify=False):
		self.url = url
		self.verify = verify
		self.session = Session()

		# get cookie headers
		self.session.head(self.url + 'index.php', verify=self.verify)

		# login
		self.login(username, password)

	def login(self, username, password):
		response = self.control(
			'login_team',
			{
				'team_name': username,
				'password': password
			},
			page='index',
			token=False
		)

		return response


	def control(self, action=None, data={}, upload=None, page='admin', token=True):
		if action is not None:
			data['action'] = action

		if token:
			data['csrf_token'] = self.getToken()

		if upload is not None:
			# upload is a tuple (identifier, filename, mime)
			# ex ('database_file', 'fbctf.sql.gz', 'application/gzip')
			data[upload[0]] = (upload[1], open(upload[1], 'rb'), upload[2])
			data = MultipartEncoder(data)

			header = {'Content-Type': data.content_type}
		else:
			header = {}

		print(data)

		response = self.session.post(
			url = self.url + 'index.php',
			params = {
				'p': page,
				'ajax': 'true'
			},
			data = data,
			headers = header,
			verify = self.verify
		)

		print(response.text)
		return response

	def getToken(self, category='admin', page='controls'):
		response = self.session.get(
			url = self.url + 'index.php?p=admin&page=controls',
			verify = self.verify
		)

		# extract the token from the request
		start = response.text.find('name="csrf_token" value="') + len('name="csrf_token" value="')
		end = response.text.find('"', start)
		token = response.text[start:end]

		return token

if __name__ == "__main__":
	
