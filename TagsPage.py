from Handler import Handler
from Databases import UserDB
from SearchPage import SearchPage
from Databases import TagsDB
from Encrypt import Security
class TagsPage(Handler,Security):
	def get_tags(self,username = ''):
		if not username:
			tagsdb = TagsDB.all().fetch(500)
			tags = []
			for i in tagsdb:
				tags.append(i.tagname)
			return set(tags)
		else:
			"""call searchpages function"""


	def get(self):
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

		tags = self.get_tags()
		self.pass_template_value_tags_page(tags, username = username, login = login, logout = logout, signup = signup)

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
			is_tag_or_people = self.request.POST.get('tags_or_people')
			# is_tag_or_people = is_tag_or_people.strip()
			search_key = search_key.strip()
			if not search_key or not is_tag_or_people:
				self.redirect('/trending')
			else:
				# self.redirect('search/%s'%search_key)
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
				# self.response.out.write('hi')
				self.pass_template_value_search_page(logout = logout, username = username,
									signup = signup, login = login, search_key = search_key, tags = l,
									display_tag = display_tag, display_people = display_people)
