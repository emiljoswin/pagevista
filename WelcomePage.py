from Handler import Handler
from Encrypt import Security
class WelcomePage(Handler,Security):
	def get(self):
		username_ck = str(self.request.cookies.get('username_ck'))
		username = self.return_username_if_valid_cookie(username_ck)
		if not username_ck or username_ck == 'None':
			login = "Login"
			signup = "Signup"
			username = ""
			logout = ""
		else:
			username = self.return_username_if_valid_cookie(username_ck)
			login = ""
			signup = ""
			logout = "Logout"

		self.pass_template_value_welcome_page(username = username, login = login, logout = logout, signup = signup)

	def post(self):
		self.pass_template_value_welcome_page()