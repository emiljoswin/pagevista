import hashlib

class Security():
	username_secret = "my_username_secret"
	password_secret = "my_password_secret"
	email_secret = "my_email_secret"
	post_id_secret = "my_post_id_secret"

	def encrypt_username(self,username):
		username = str(username)
		return (username+'|'+hashlib.md5(self.username_secret+username).hexdigest())

	def encrypt_email(self,email):
		email = str(email)
		return hashlib.md5(self.email_secret+email).hexdigest()

	def encrypt_password(self,password):
		password = str(password)
		return hashlib.md5(self.password_secret+password).hexdigest()

	def encrypt_post_id(self,post_id):
		post_id = str(post_id)
		return (post_id + '|' + hashlib.md5(self.post_id_secret+post_id).hexdigest())

	def return_post_id_if_valid_cookie(self,post_id_ck):
		if not post_id:
			return None
		post_id = post_id_ck.split('|')[0]
		post_id = str(post_id)
		required_post_id = post_id + '|' + hashlib.md5(self.post_id_secret + post_id).hexdigest()
		if required_post_id == post_id_ck:
			return post_id
		return None

	def return_username_if_valid_cookie(self,username_ck):
		if not username_ck:
			return None
		username = username_ck.split('|')[0]
		username = str(username)
		required_username = username + '|' + hashlib.md5(self.username_secret + username).hexdigest()
		if required_username == username_ck:
			return username
		return None

	def check_if_password_valid(self,input_password):
		pass
