from Handler import Handler
from Databases import PostsDB
from Databases import CommentsDB
from Databases import UserDB
from Encrypt import Security
from Databases import PeopleDB
from SearchPage import SearchPage
import re
from MemCached import CachePosts

	
class DonePage(Handler, Security, CachePosts):
	def get_date_without_decimal_in_seconds(self,date):
		if not date:
			return None
		date = str(date)
		r = re.compile('(.+)\.(\w+)')
		m = r.match(date)
		return m.group(1)

	def get_contents(self,post_id):
		# post = PostsDB.get_by_id(int(post_id))
		# self.response.out.write(int(post_id))
		post = self.returnPostById(post_id, False)
		date = self.get_date_without_decimal_in_seconds(post.date)
		l = []
		l.append((post.key().id(), post.title, post.author, post.subject, date, post.like_count, 
								post.comment_count, post.tag1, post.tag2, post.tag3, post.like, post.dislike,post.post))
		return l


	def get(self,post_id):
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

		# contents = PostsDB.get_by_id(int(post_id))
		contents = self.returnPostById(post_id, True)
		comment_count = contents.comment_count
		if not contents.tag1:
			contents.tag1 = ""
		if not contents.tag2:
			contents.tag2 = ""
		if not contents.tag3:
			contents.tag3 = ""
		for content in [contents]:
			if content:
				username_sec = content.userdb.username
		author = self.return_username_if_valid_cookie(username_sec)
		post = self.get_contents(post_id)
		# commentsdb = CommentsDB.all().filter('postsdb =',contents).fetch(10)
		commentsdb = self.loadComments(contents, False)
		username_ck = str(self.request.cookies.get('username_ck'))

		self.pass_template_value_done_page(username = username, logout = logout, login = login, signup = signup,
											 post = post, author = author, comments = commentsdb,
											 like_count = contents.like_count, comment_count = comment_count, post_id = post_id)
		
	def post(self,post_id):
		
		self.response.out.write('in post')
		username_ck = str(self.request.cookies.get('username_ck'))
		username = self.return_username_if_valid_cookie(username_ck)
		if not username or username == "None":
			pass
		else:
			is_comment = self.request.POST.get('submit_comment')
			is_like = self.request.POST.get('like')
			is_dislike = self.request.POST.get('dislike')
			if is_comment:
				if not username or username == "None":
					self.response.out.write("login")
				comment = self.request.get('comment')
				if not comment or comment.isspace():
					self.redirect('/done/%d'%int(post_id))
				else:
					postsdb = PostsDB.get_by_id(int(post_id))
					commentsdb = CommentsDB(postsdb = postsdb,comment = comment, commenter = username)
					postsdb.comment_count = postsdb.comment_count + 1
					postsdb.rating = postsdb.rating + 0.6
					postsdb.put()
					commentsdb.put()

					"""caching"""
					self.returnPostById(post_id, True)
					self.loadComments(postsdb, True)
					self.loadRecentPostsDb(order = '-date', update = True)
					self.loadTrendingPostsDb(order = '-rating', update = True)


					self.redirect('/done/%d'%int(post_id))
			elif is_like:
				peopledb = PeopleDB.all().filter('posts_id =',int(post_id)).filter('username_liked =',username)
				if peopledb.count() == 0:
					self.response.out.write('not found')#display it int a box
					peopledb = PeopleDB(posts_id = int(post_id),has_liked_boolean = True, username_liked = username)
					peopledb.put()
					postsdb = PostsDB.get_by_id(int(post_id))
					postsdb.like_count = postsdb.like_count + 1
					postsdb.like = postsdb.like + 1
					postsdb.rating = postsdb.rating + 0.4
					postsdb.put()
					self.response.out.write('you have successfully liked this post for the first time')#display it int a box
				else:
					peopledb.fetch(1)
					for i in peopledb:
						if i.has_liked_boolean:
							self.response.out.write('you cannot like more than once')#display it int a box
						else:
							i.has_liked_boolean = True
							i.put()
							postsdb = PostsDB.get_by_id(int(post_id))
							postsdb.like_count = postsdb.like_count + 1
							postsdb.like = postsdb.like + 1
							postsdb.rating = postsdb.rating + 0.4
							postsdb.put()							
							self.response.out.write('you have successfully liked this post after disliking it')#display it in a box in js
							break

				"""caching"""
				self.returnPostById(post_id, True)	
				self.loadRecentPostsDb(order = '-date', update = True)
				self.loadTrendingPostsDb(order = '-rating', update = True)


				self.redirect('/done/%d'%int(post_id))
			elif is_dislike:
				peopledb = PeopleDB.all().filter('posts_id =',int(post_id)).filter('username_liked =',username)
				if peopledb.count() == 0:
					self.response.out.write('not found')
					peopledb = PeopleDB(posts_id = int(post_id), has_liked_boolean = False, username_liked = username)
					peopledb.put()
					postsdb = PostsDB.get_by_id(int(post_id))
					postsdb.like_count = postsdb.like_count - 1
					postsdb.dislike = postsdb.dislike - 1 
					postsdb.rating = postsdb.rating + 0.2
					postsdb.put()
					self.response.out.write('you have successfully disliked the post for the first time')#display it int a box
				else:
					peopledb.fetch(1)
					for i in peopledb:
						if not i.has_liked_boolean:
							self.response.out.write('you cannot dislike more than once')#display it int a box
						else:
							i.has_liked_boolean = False
							i.put()
							postsdb = PostsDB.get_by_id(int(post_id))
							postsdb.like_count = postsdb.like_count - 1
							postsdb.dislike = postsdb.dislike - 1 
							postsdb.rating = postsdb.rating + 0.2
							postsdb.put()	
							self.response.out.write('you have successfully disliked this post after liking it')#display it int a box
							break

				"""caching"""
				self.returnPostById(post_id, True)	
				self.loadRecentPostsDb(order = '-date', update = True)
				self.loadTrendingPostsDb(order = '-rating', update = True)


				self.redirect('/done/%d'%int(post_id))	




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
			# is_tag_or_people = is_tag_or_people.strip()
			search_key = search_key.strip()
			if not search_key or not is_tag_or_people:
				self.redirect('/trending')
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


		# FOR LOGGING IN FROM THE LOGIN PROMPT WINDOW


		# username_ck = str(self.request.cookies.get('username_ck'))
		# is_login = self.request.POST.get('login_prompt')
		# if is_login:
		# 	self.response.out.write('login pressed')
		# 	a = 'Emil|a26e00a1ad717d6f37d681396dc82c26'
		# 	# self.response.headers.add_header('Set-Cookie','username_ck=%s'%a)
			