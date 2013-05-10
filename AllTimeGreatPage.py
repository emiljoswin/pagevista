import webapp2
from Handler import Handler
from Encrypt import Security
from Databases import PostsDB
from SearchPage import SearchPage

""" Device an algo to decrement the rating with every passing hour """
class AllTimeGreatPage(Handler,Security):
	def get_recent_posts(self):
		posts = {}
		postdb = PostsDB.all().order("-rating").fetch(30)
		l = []		
		for post in postdb:
			l.append((post.key().id(), post.title, post.author, post.subject, post.date, post.like_count, 
								post.comment_count, post.tag1, post.tag2, post.tag3, post.like, post.dislike))
		return l

	def get(self):
		posts = self.get_recent_posts()
		username_ck = str(self.request.cookies.get('username_ck'))
		if not username_ck or username_ck == 'None':
			self.pass_template_value_about_page(login = "Login",signup = "Signup",posts = posts)
		else:
			username = username_ck
			username = self.return_username_if_valid_cookie(username_ck)
			self.pass_template_value_all_time_great_page(logout = "Logout",username = username,posts = posts)
			
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
			search_key = str(self.request.get('search_key'))
			search_key = search_key.strip()
			# self.response.out.write(search_key + "<br>")
			if not search_key:
				self.redirect('/tags')
			else:
				# self.response.out.write('hi' + search_key)

				tags = SearchPage().get_search_result(search_key)
				# self.response.out.write('hi ' + str(tags))
				tags = sorted(tags, key = lambda x: x[1] )
				# self.response.out.write(tags)
				l = []
				for (tag,rank) in tags:
					l.append(tag)
				# self.response.out.write(l)
				self.pass_template_value_tags_page(logout = logout, username = username,
									signup = signup, login = login, search_key = search_key, tags = l)
