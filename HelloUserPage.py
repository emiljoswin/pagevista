import webapp2
from Handler import Handler
from Databases import UserDB
from Databases import PostsDB
from Encrypt import Security
from Databases import PeopleDB
from google.appengine.ext import db
from google.appengine.api import images
from Databases import DefImageDB
import re
"""	
This page from the perspective of the logged in user and not logged in user is different. 
At the moment this is not checked.
"""
class ImagePage(Handler):
	def get(self):
		user_id = db.get(self.request.get("img_id"))
		if user_id.user_image:
			self.response.headers['Content-Type']="image/png"
			self.response.out.write(user_id.user_image)
		else:
			defimagedb=DefImageDB.all().fetch(1)
			for i in defimagedb:
				self.response.out.write(i.def_image)
				break


class HelloUserPage(Handler,Security):
	def get_date_without_decimal_in_seconds(self,date):
		if not date:
			return None
		date = str(date)
		r = re.compile('(.+)\.(\w+)')
		m = r.match(date)
		return m.group(1)

	def get(self,username):
		"""The homepage of username is hidden from non-logged in user. This may prompt him to register for the site."""

		username_ck = str(self.request.cookies.get('username_ck'))
		if not username_ck or username_ck == 'None':
			self.redirect('/login')
		else:
			username_sec = self.encrypt_username(username)		
			userdb = UserDB.all().filter('username =',username_sec).fetch(1)
			l = []
			for i in userdb:
				image_key = i.key()
				posts = PostsDB.all().filter('userdb =',i).fetch(100)

				for post in posts:
					date = self.get_date_without_decimal_in_seconds(post.date)
					l.append((post.key().id(), post.title, post.author, post.subject, date, post.like_count, 
								post.comment_count, post.tag1, post.tag2, post.tag3, post.like, post.dislike))
			user_posts = l
			whos_page = username 
			username = self.return_username_if_valid_cookie(username_ck)

			q = PeopleDB.all().filter('people_follows =',username_ck).fetch(100)
			following = []
			for i in q:
				following.append(i.people_followed)			

			if whos_page != username:
				if whos_page in following:
					follow = ""
				else:
					follow = "follow"
				following = ""
			else:
				follow = ""

			self.pass_template_value_hellouser_page(logout = 'Logout',image_id_key = image_key, username = username ,whos_page = whos_page,
										 follow = follow, posts = user_posts, following = following)

	def post(self,username):
		is_follow = self.request.POST.get('follow')
		is_get_image = self.request.POST.get('upload_image')
		if is_get_image:
			avatar = images.resize(self.request.get('image'),90,90)
			whos_page = username
			username_ck = str(self.request.cookies.get('username_ck'))
			userdb = UserDB.all().filter('username =',username_ck).fetch(1)
			for i in userdb:
				i.user_image = db.Blob(avatar)
				i.put()
		elif is_follow:
			whos_page = username
			username_ck = str(self.request.cookies.get('username_ck'))
			userdb = UserDB.all().filter('username =',username_ck).fetch(1)
			for i in userdb:
				peopledb = PeopleDB(userdb = i, people_followed = whos_page, people_follows = username_ck)
				peopledb.put()
				break
		self.redirect('/hello_user/%s'%username)