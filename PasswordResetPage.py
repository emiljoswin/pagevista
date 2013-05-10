from Handler import Handler
from Databases import UserDB
from Encrypt import Security
from Databases import PasswordRecovery
import string
import random
from google.appengine.api import mail


class PasswordResetPage(Handler,Security):
	def get(self):

		self.pass_template_value_password_reset_page()

	def post(self):
		username = str(self.request.get('username'))
		username_sec = self.encrypt_username(username)
		userdb = UserDB.all().filter('username =',username_sec)

		if userdb.count() == 0:
			self.pass_template_value_password_reset_page(username = username, error = "Such a user does not exist. Make sure you typed the correct username.")
		else:
			random_string = string.ascii_uppercase + string.ascii_lowercase + string.digits
			# self.response.out.write(random_string + "<br>")
			random_url = ''.join(random.choice(random_string) for i in range(15))
			# self.response.out.write(random_url)


			for i in userdb:
				email = i.email_id
				break

			recovery_link = "http://pagevista.appspot.com/recovery/"+random_url
			sender = "<ejoswin@gmail.com>"
			to = "<" + email + ">"
			body = "reset your password here " + recovery_link
			subject = "ZOOSMASH - password reset"
			body = """Dear""" + username +""",

			Here is the link for resetting your password as per requested """ + recovery_link + """ Please follow the instructions. 

			If you had not requested a password reset for your account please ignore this mail.


			Thank you,
			myGreenPage team

			"""
			# self.response.out.write(random_url + " " + to + " " + body)

			mail.send_mail(sender= sender,
								to = to,
								subject = "reset mail",
								body = body)


			precovery = PasswordRecovery(random_url = random_url, username = username_sec)
			precovery.put()

			self.pass_template_value_password_reset_page(error = "A link to reset your password has" +
			 							"been mailed to you.Plese follow instructions mentioned "+
			 							"in it to reset yor password. ")
		