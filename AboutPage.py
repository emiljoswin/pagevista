import webapp2
from Handler import Handler
from Encrypt import Security
from Databases import PostsDB
from SearchPage import SearchPage
from Databases import UserDB
import re
class AboutPage(Handler,Security):
	def get_date_without_decimal_in_seconds(self,date):
		if not date:
			return None
		date = str(date)
		r = re.compile('(.+)\.(\w+)')
		m = r.match(date)
		return m.group(1)


	def get_recent_posts(self):
		l = []
		postdb = PostsDB.all().fetch(100)
		for post in postdb:
			date = self.get_date_without_decimal_in_seconds(post.date)
			l.append((post.key().id(), post.title, post.author, post.subject, date, post.like_count, 
					post.comment_count, post.tag1, post.tag2, post.tag3, post.like, post.dislike))
		return l

	def get(self):
		l = self.get_recent_posts()
		username_ck = str(self.request.cookies.get('username_ck'))
		if not username_ck or username_ck == 'None':
			self.pass_template_value_about_page(login = "Login",signup = "Signup",posts = l)
			# self.response.out.write(login)

		else:
			username = username_ck
			username = self.return_username_if_valid_cookie(username_ck)
			self.pass_template_value_about_page(logout = "Logout",username = username,posts = l)
			
	def post(self):
		username_ck = str(self.request.cookies.get('username_ck'))
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

		is_tag_search = self.request.POST.get('tag_search')
		if is_tag_search:
			# self.response.out.write('hi')
			search_key = str(self.request.get('search_key'))
			is_tag_or_people = self.request.POST.get('tags_or_people')
			is_tag_or_people = is_tag_or_people.strip()
			search_key = search_key.strip()
			if not search_key or not is_tag_or_people:
				self.redirect('/recent')
			else:
				tags = SearchPage().get_search_result(search_key,0,is_tag_or_people)
				tags = sorted(tags, key = lambda x: x[1] )
				l = []
				for (tag,rank) in tags:
					l.append(tag)
				# self.response.out.write(l)	
				display_tag = False
				display_people = False
				if is_tag_or_people == 'tags':
					display_tag = True
				if is_tag_or_people == "people":
					display_people = True
				# self.response.out.write(display_people)
				# self.response.out.write(display_tag)
				self.pass_template_value_search_page(logout = logout, username = username,
									signup = signup, login = login, search_key = search_key, tags = l,
									display_tag = display_tag, display_people = display_people)
		
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
			for result in results:
				if result.username == username_sec and result.password == password_sec:
					login_valid = True
					break
			if login_valid:
				"""set cookie and redirect to the users homepage
				"""
				self.response.headers.add_header('Set-Cookie','username_ck=%s'%username_sec)
				self.redirect('/hello_user/%s'%username_entered)
			else:
				loginpage_error = "invalid username and password"
				login_valid = False
				self.pass_template_value_login_page(loginpage_error = loginpage_error,signup = "Signup")
	