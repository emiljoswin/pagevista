from Handler import Handler
from Databases import UserDB 
from Databases import PostsDB
from Encrypt import Security
from Databases import TagsDB
from MemCached import CachePosts, CacheTags

class NewPage(Handler, UserDB, PostsDB, Security, CachePosts, CacheTags):

	def replace_space_with_underscore(self,tagname):
		l = tagname.split()
		tag = ""
		for i in l:
			if not tag:
				tag = str(i)
			else:
				tag = tag + '_' + str(i)
		return tag

	"""	
	def load_preview(self,title, content,username,username_ck):
		self.pass_template_value_new_page(title = title, 
										content = content,preview = content,username = username,logout = "logout")"""

	def load_upload(self,title, content, username, username_ck, tag1 = "", tag2 = "", tag3 = ""):
		users = UserDB.all().filter('username =',username_ck).fetch(1)
		for i in users:
			title = title.strip()[:50]
			post_username = PostsDB(userdb = i,title = title, post = content, like_count = 0,author = username)
			post_username.put()
			post_id = post_username.key().id()
			post_username = PostsDB.get_by_id(int(post_id))
			tag1 = tag1.strip()[:15]
			tag2 = tag2.strip()[:15]
			tag3 = tag3.strip()[:15]
			tagfound = False
			if tag1 :
				tagfound = True
				tag = self.replace_space_with_underscore(tag1)
				tagsdb = TagsDB(postsdb = post_username, tagname = tag, post_id = post_username.key().id())
				post_username.tag1 = tag
				tagsdb.put()
			if tag2 and tag2 != tag1:
				tagfound = True
				tag = self.replace_space_with_underscore(tag2)
				tagsdb = TagsDB(postsdb = post_username, tagname = tag, post_id = post_username.key().id())
				post_username.tag2 = tag
				tagsdb.put()
			if tag3 and tag3 != tag1 and tag3 != tag2:
				tagfound = True
				tag = self.replace_space_with_underscore(tag3)
				tagsdb = TagsDB(postsdb = post_username, tagname = tag, post_id = post_username.key().id())
				post_username.tag3 = tag
				tagsdb.put()
			if not tagfound:
				tag = title[:10]
				tagsdb = TagsDB(postsdb = post_username, tagname = tag, post_id = post_username.key().id())
				post_username.tag1 = tag
				tagsdb.put()
			post_username.put()
			self.loadRecentPostsDb(order = "-date", update = True)
			self.loadTrendingPostsDb(order = '-rating', update = True)
			self.loadAllTagsDb(update = True)

			self.redirect('/done/%d'%post_username.key().id())
			break
		# if not users:
		# 	content = "no usres returned from the query " +  username_ck
		"""instead of passing to the new_page redirect to the done page"""
		# self.pass_template_value_new_page(username = username, preview = content)	
		
	def load_save(self, username):
		""" need to work on saving more than one post at a time by more than one person"""
		pass

	def get(self):
		username_ck = str(self.request.cookies.get('username_ck'))
		if not username_ck or username_ck == "None":
			self.redirect('/login')
		else:
			username = self.return_username_if_valid_cookie(username_ck)
			self.pass_template_value_new_page(username = username,logout = "Logout")

	def post(self):
		username_ck = str(self.request.cookies.get('username_ck'))
		if not username_ck or username_ck == "None":
			self.redirect('/login')
		else:
			username = self.return_username_if_valid_cookie(username_ck)

		is_preview = self.request.POST.get('preview',None)
		is_upload = self.request.POST.get('upload',None)
		is_save = self.request.POST.get('save',None)
		# title = ""
		# subject = ""
		content = ""
		title = self.request.get('title')
		# subject = self.request.get('subject')
		content = self.request.get('editor1')
		tag1 = self.request.get('tag1')
		tag2 = self.request.get('tag2')
		tag3 = self.request.get('tag3')
		if not title or not content or title.isspace() or content.isspace() or len(content) < 140:
			# self.response.out.write('hi')
			error = "A post should have a valid title and a content"
			self.pass_template_value_new_page(username = username, title = title, content = content, error = error)

		else:
			"""planning to take out the preview button since there is a preview option 
			   inbuild in the editor."""
			if is_preview:
				self.load_preview(title,content,username, username_ck)
			elif is_upload:
				self.load_upload(title,content,username, username_ck, tag1, tag2, tag3)
			elif is_save:
				"""need to work on saving more than one post by a single user"""
				self.load_save(title, content, username, username_ck)
