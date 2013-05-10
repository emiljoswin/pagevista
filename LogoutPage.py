import webapp2
from Handler import Handler

class LogoutPage(Handler):
	def get(self):
		username = None	
		email = None
		password = None
		password_confirm = None
		# ***********DO NOT DELETE********************
		# cursor_ck = 0
		# self.response.headers.add_header('Set-Cookie','cursor_ck=%d'%cursor_ck)
		self.response.headers.add_header('Set-Cookie','username_ck=%s'%username)
		# self.response.headers.add_header('Set-Cookie','email_ck=%s'%email)
		# self.response.headers.add_header('Set-Cookie','password_ck=%s'%password)
		# self.response.headers.add_header('Set-Cookie','password_confirm_ck=%s'%password_confirm)
		self.redirect('/welcome')

	def post(self):
		pass