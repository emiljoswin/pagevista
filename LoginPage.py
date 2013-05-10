import webapp2
from Handler import Handler
from Databases import UserDB
from Encrypt import Security

class LoginPage(Handler,Security):
	def get(self):
		username_ck = self.request.cookies.get('username_ck')
		if not username_ck or username_ck == 'None':
			self.pass_template_value_login_page(signup = "Signup")
		else:
			username = self.return_username_if_valid_cookie(username_ck)
			self.redirect('/hello_user/%s'%username)

	def post(self):
		"""
			Fetch a maximum of 1000 usernames as of now and compare to see if the username 
			entered is valid.
		"""
		username_entered = str(self.request.get('username'))
		password_entered = str(self.request.get('password'))
		login_valid = False
		if not username_entered or not password_entered:
			loginpage_error = "invalid username and password"
			login_valid = False
			self.pass_template_value_login_page(loginpage_error = loginpage_error)
		else:
			q = UserDB.all()
			results = q.fetch(1000)
			password_sec = self.encrypt_password(password_entered)
			username_sec = self.encrypt_username(username_entered)
			username_found = False
			for result in results:
				if result.username == username_sec and result.password == password_sec:
					login_valid = True
					break
				elif result.username == username_sec:
					username_found = True
			if login_valid:
				"""set cookie and redirect to the users homepage
				"""
				self.response.headers.add_header('Set-Cookie','username_ck=%s'%username_sec)
				self.redirect('/hello_user/%s'%username_entered)
			else:
				if username_found:
					# self.response.out.write("username found")
					self.pass_template_value_login_page(signup = "Signup", valid_username = "True")
				else:
					loginpage_error = "invalid username and password"
					login_valid = False
					self.pass_template_value_login_page(loginpage_error = loginpage_error,signup = "Signup")


			