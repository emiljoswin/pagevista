import webapp2
from Handler import Handler
from Encrypt import Security
from Databases import PostsDB
from Databases import TagsDB
from Databases import UserDB

class SearchPage(Handler,Security):
	def get_tags(self):
		tags = []
		tagsdb = TagsDB.all().fetch(1000)
		for tag in tagsdb:
			if tag.tagname and tag.tagname not in tags:
				tags.append(tag.tagname)
		return sorted(tags)

	def within_mismatch_limit(self, mismatch, tagname, search_key):
		table = []
		len1 = len(tagname)
		len2 = len(search_key)
		for i in range(len1 + 1):
			row = []
			for j in range(len2 + 1):
				if i == 0:
					row.append(j)
				elif j == 0:
					row.append(i)
				else:
					row.append(0)
			table.append(row)
		for i in range(1,len1 + 1):
			for j in range(1,len2 + 1):
				if tagname[i-1] == search_key[j-1]:
					m = table[i-1][j-1]
				else:
					m = table[i-1][j-1] + 1
				ins = table[i-1][j] + 1
				de = table[i][j-1] + 1
				if m <= ins and m <= de:
					val = m
				elif ins <= m and ins <= de:
					val = ins
				else:
					val = de
				table[i][j] = val

		if table[len1][len2] > mismatch:
			return None
		else:
			return table[len1][len2]

	def return_tags_username(self, mismatch, search_key, tags_or_people):
		l = []
		if tags_or_people == 'tags':
			tagsdb = TagsDB.all().fetch(1000)
			for i in tagsdb:
				if abs(len(i.tagname) - len(search_key)) > mismatch+1:
					continue
				else:
					var = self.within_mismatch_limit(mismatch, i.tagname, search_key)
					if var or var == 0 :
						if (i.tagname,var) not in l:
							l.append((i.tagname,var))
			return l

		elif tags_or_people == 'people':
			userdb = UserDB.all().fetch(1000)
			for i in userdb:
				username = self.return_username_if_valid_cookie(i.username)
				if abs(len(username) - len(search_key)) > mismatch+1:
					# print 'if'
					continue
				else:
					# print 'else'
					var = self.within_mismatch_limit(mismatch, username, search_key)
					if var or var == 0 :
						if (username,var) not in l:
							l.append((username,var))
			return l

	def get_search_result(self, search_key,cursor_start,tags_or_people):
		key_length = len(search_key)
		if key_length <= 3:
			""" **************************************************
				**************************************************
				Retrieve the username from encoded username for len < 3.
			    *************************************************
			    *************************************************"""
			if tags_or_people == 'tags':
				tagsdb = TagsDB.all().filter('tagname =',search_key).fetch(100)
			elif tags_or_people == 'people':
				tagsdb = UserDB.all().filter('username =',search_key).fetch(100)
			l = []
			for i in tagsdb:
				l.append((i.tagname,1))
		elif key_length > 3 and key_length <= 5:
			mismatch = 1
			l = self.return_tags_username(mismatch, search_key, tags_or_people)
		elif key_length > 5 and key_length <= 8:
			mismatch = 2
			l = self.return_tags_username(mismatch, search_key, tags_or_people)
		else:
			mismatch = 3
			l = self.return_tags_username(mismatch, search_key, tags_or_people)
		return set(l)

	def get(self,search_key):
		is_tag_or_people = self.request.POST.get('tags_or_people')
		self.response.out.write(is_tag_or_people)
		tags_sorted = self.get_tags()
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

		self.pass_template_value_search_page(logout = logout, username = username,
									signup = signup, login = login, search_key = search_key, tags = tags_sorted)

		# if not username_ck or username_ck == 'None':
		# 	self.pass_template_value_search_page(login = "Login",signup = "Signup",tags = tags_sorted)
		# else:
		# 	username = username_ck
		# 	username = self.return_username_if_valid_cookie(username_ck)
		# 	self.pass_template_value_search_page(logout = "Logout",username = username,tags = tags_sorted)
			
	def post(self,search_key):
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
				self.redirect('/search')
			else:
				tags = self.get_search_result(search_key,0,is_tag_or_people)
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

