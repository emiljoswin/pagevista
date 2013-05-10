import re
import webapp2
from Handler import Handler
from Databases import UserDB
from google.appengine.ext import db
from Encrypt import Security

class SignupPage(Handler,Security):
	def is_valid_username(self, username):
		""" check if the username is already existing or not. Return username or False
			If the user submits wrong the first time, only then cache the usernames from the DB
		"""
		userdata = UserDB.all()
		userdatas = userdata.fetch(1000)
		username_sec = self.encrypt_username(username)
		for userdata in userdatas:
			if userdata.username == username_sec:
				return None
		return username

	def chech_username_syntax(self, username):
		return username.isalnum()


	def is_valid_email(self,email):
		"""check the validity of email. Return email or False"""
		email_regex = re.compile('^[\S]+\@[\S]+\.[\S]+$')
		a = email_regex.match(email)
		if a:
			return a.group()
		else:
			return None

	def email_already_present(self,email):
		userdb = UserDB.all().fetch(1000)
		for i in userdb:
			if i.email_id == email:
				return None
		return email

	def get(self):
		username_ck = self.request.cookies.get('username_ck')
		if not username_ck or username_ck == 'None':
			self.pass_template_value_signup_page()
		else:
			username = self.return_username_if_valid_cookie(username_ck)
			# self.response.out = username
			self.redirect('/hello_user/%s'%username)

	def post(self):
		username = str(self.request.get('username'))
		email = str(self.request.get('email'))
		password = str(self.request.get('password'))
		password_confirm = str(self.request.get('password_confirm'))
		signup_success = True
		username_error = ""
		email_error = ""
		password_error = ""
		password_confirm_error = ""

		# username = self.is_valid_username(username)
		email = self.is_valid_email(email)

		if not username:
			username_error = "Please provide a valid username!"
			username = ""
			signup_success = False
		elif len(username) < 4:
			username_error = "A username must be atleast 4 characters long"
			username = ""
			signup_success = False
		elif not self.is_valid_username(username):
			username_error = "The username '" + username +"' 'is already taken!"
			# username = ""
			signup_success = False
		elif not self.chech_username_syntax(username):
			username_error = "The username must contain alphanumeric characters only"
			signup_success = False
		if not email or not self.is_valid_email(email):
			email_error = "Please provide a valid email address!"
			email = ""
			signup_success = False
		elif not self.email_already_present(email):
			email_error = "The holder of this email is already a user"
			email = ""
			signup_success = False
		if not password:
			password_error = "Please provide a valid password!"
			signup_success = False
		elif not password_confirm or password_confirm != password:
			password_confirm_error = "Passwords do not match!"
			signup_success = False
		if not signup_success:
			self.pass_template_value_signup_page(username = username, email = email,
					username_error = username_error,email_error = email_error,password_error = password_error,
					password_confirm_error = password_confirm_error)
		else:
			username_sec = self.encrypt_username(username)
			
			#email_sec = self.encrypt_email(email)
			email_sec = email
			
			password_sec = self.encrypt_password(password)
			
			userdb = UserDB(username = username_sec,email_id = email_sec,password = password_sec)
			userdb.put()
			
			self.response.headers.add_header('Set-Cookie','username_ck=%s'%username_sec)
			#self.response.headers.add_header('Set-Cookie','email_ck=%s'%email)
			#self.response.headers.add_header('Set-Cookie','password_ck=%s'%password)
			#self.response.headers.add_header('Set-Cookie','password_confirm_ck=%s'%password_confirm)
			self.redirect('/hello_user/%s'%username)