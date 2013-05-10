from Databases import UserDB
from google.appengine.ext import db
from google.appengine.api import images
from Encrypt import Security
from Handler import Handler


class UploadImagePage(Handler,Security):
	def get(self):
		username_ck = str(self.request.cookies.get('username_ck'))
		if not username_ck or username_ck == 'None':
			self.redirect('/login')
		else:
			self.pass_template_value_uploadimage_page()

	def post(self):
		username_ck = str(self.request.cookies.get('username_ck'))
		username = self.return_username_if_valid_cookie(username_ck)
		avatar = images.resize(self.request.get('image'),90,90)
		userdb = UserDB.all().filter('username =',username_ck).fetch(1)
		for i in userdb:
			i.user_image = db.Blob(avatar)
			i.put()
		self.redirect('/hello_user/%s'%username)


