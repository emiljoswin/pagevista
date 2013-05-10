from Handler import Handler
from Databases import UserDB
from Encrypt import Security
from Databases import PasswordRecovery

class RecoveryPage(Handler,Security):
	def get(self, recovery_id):

		precovery = PasswordRecovery.all().filter('random_url =',recovery_id).filter('reset =',False).fetch(1)


		if not precovery:
			self.response.out.write('invalid page')
		else:

			for i in precovery:
				username = i.username
				break
			username = self.return_username_if_valid_cookie(username)
			self.pass_template_value_recovery_page(username = username, error = "")

	def post(self, recovery_id):

		password = self.request.get('password')
		password_confirm = self.request.get('password_confirm')
		precovery = PasswordRecovery.all().filter('random_url =',recovery_id).fetch(1)

		for i in precovery:
			username = i.username
			break
			
		if not password or password.isspace():
			self.pass_template_value_recovery_page(username = username, error = "Please enter a valid password")
		elif password != password_confirm:
			self.pass_template_value_recovery_page(username = username, error = "Passwords do not match")
		else:

			
			userdb = UserDB.all().filter('username =',username).fetch(1)
			for i in userdb:
				i.password = self.encrypt_password(password)
				i.put()
				break

			for i in precovery:
				i.reset = True
				i.put()

			# home = "http://localhost:8080/blogname"

			self.response.out.write("""password has been changed successfully.
			 <a href = "http://pagevista.appspot.com/login">return</a>""")
