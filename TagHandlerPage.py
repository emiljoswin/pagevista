import webapp2
from Handler import Handler
from Encrypt import Security
from Databases import PostsDB
from SearchPage import SearchPage
import re

class TagHandlerPage(Handler,Security):
	def get_date_without_decimal_in_seconds(self,date):
		if not date:
			return None
		date = str(date)
		r = re.compile('(.+)\.(\w+)')
		m = r.match(date)
		return m.group(1)

	def get_tagged_posts(self,tagname):
		l = []
		postdb = PostsDB.all().filter('tag1 =',tagname).fetch(100)		
		for post in postdb:
			date = self.get_date_without_decimal_in_seconds(post.date)
			l.append((post.key().id(), post.title, post.author, post.subject, date, post.like_count, 
								post.comment_count, post.tag1, post.tag2, post.tag3, post.like, post.dislike,post.post))
	
		postdb = PostsDB.all().filter('tag2 =',tagname).fetch(100)		
		for post in postdb:
			date = self.get_date_without_decimal_in_seconds(post.date)
			l.append((post.key().id(), post.title, post.author, post.subject, date, post.like_count, 
								post.comment_count, post.tag1, post.tag2, post.tag3, post.like, post.dislike,post.post))
	
		postdb = PostsDB.all().filter('tag3 =',tagname).fetch(100)		
		for post in postdb:
			date = self.get_date_without_decimal_in_seconds(post.date)
			l.append((post.key().id(), post.title, post.author, post.subject, date, post.like_count, 
								post.comment_count, post.tag1, post.tag2, post.tag3, post.like, post.dislike,post.post))
		return set(l)

	def get(self,tagname):
		tagged_posts = self.get_tagged_posts(str(tagname))
		username_ck = str(self.request.cookies.get('username_ck'))
		if not username_ck or username_ck == 'None':
			self.pass_template_value_tag_handler_page(login = "Login",signup = "Signup",posts = tagged_posts,
													tag = tagname)
		else:
			username = username_ck
			username = self.return_username_if_valid_cookie(username_ck)
			self.pass_template_value_tag_handler_page(logout = "Logout",username = username,posts = tagged_posts,
													tag = tagname)
			
	def post(self,tagname):
		# self.response.out.write('hello')
		# is_username = str(self.request.POST.get('username'))
		# self.response.out.write(is_username)
		# if is_username:
		# 	username = self.request.cookies.get('username_ck')
		# 	self.redirect('/hello_user/%s'%username)

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
				display_tag = False
				display_people = False
				if is_tag_or_people == 'tags':
					display_tag = True
				if is_tag_or_people == "people":
					display_people = True
				self.pass_template_value_search_page(logout = logout, username = username,
									signup = signup, login = login, search_key = search_key, tags = l,
									display_tag = display_tag, display_people = display_people)
			