import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                                autoescape=True)

class Handler(webapp2.RequestHandler):
	def pass_template_value_init_page(self,image_id_key = ""):
		self.render("init.html", image_id_key = image_id_key)

	def pass_template_value_welcome_page(self,username = "", login = "", logout = "", signup = ""):
		self.render("welcome.html",username = username,login = login, logout = logout, signup = signup)
		
	def pass_template_value_signup_page(self,username = "", username_error = "",email = "",email_error = "",password_error =  "",
										password_confirm_error = ""):
		self.render("signup.html",username = username, username_error = username_error, email = email,email_error = email_error,
									password_error = password_error,password_confirm_error = password_confirm_error, login = "Login")

	def pass_template_value_hellouser_page(self,logout = "",image_id_key = "",username = "", whos_page = "", follow = "",
											posts = "", following = ""):
		self.render("hello_user.html",logout = logout, image_id_key = image_id_key, username = username, whos_page = whos_page, follow = follow,
										posts = posts, following = following)
		
	def pass_template_value_uploadimage_page(self):
		self.render("upload_image.html")

	def pass_template_value_about_page(self,logout = "",signup = "",login = "",Why_this_blog = "",username = "",
										posts = ""):
		self.render("blogname.html",logout = logout, signup = signup, login = login, username = username,Why_this_blog = Why_this_blog,
										posts = posts)

	def pass_template_value_trending_page(self,logout = "",signup = "",login = "",Why_this_blog = "",username = "",
										posts = ""):
		self.render("trending.html",logout = logout, signup = signup, login = login, username = username,Why_this_blog = Why_this_blog,
										posts = posts)

	def pass_template_value_recent_page(self,logout = "",signup = "",login = "",Why_this_blog = "",username = "",
										posts = ""):
		self.render("recent.html",logout = logout, signup = signup, login = login, username = username,Why_this_blog = Why_this_blog,
										posts = posts)

	def pass_template_value_all_time_great_page(self,logout = "",signup = "",login = "",Why_this_blog = "",username = "",
										posts = ""):
		self.render("all_time_great.html",logout = logout, signup = signup, login = login, username = username,Why_this_blog = Why_this_blog,
										posts = posts)

	def pass_template_value_search_page(self, logout = "", signup = "", login = "", username = "", search_key = "",
									 tags = "", display_tag = "", display_people = ""):
		self.render("search.html", logout = logout, signup = signup, login = login, username = username, 
			search_key = search_key, tags = tags, display_tag = display_tag, display_people = display_people)
	
	def pass_template_value_tag_handler_page(self,logout = "",signup = "",login = "",Why_this_blog = "",username = "",
										posts = "", tag = ""):
		self.render("tag.html",logout = logout, signup = signup, login = login, username = username,Why_this_blog = Why_this_blog,
										posts = posts, tag = tag)

	def pass_template_value_login_page(self,username = "",loginpage_error = "",signup = "",valid_username = ""):
		self.render("login.html",username = username, loginpage_error = loginpage_error,signup = signup, valid_username = valid_username)

	def pass_template_value_password_reset_page(self,username = "", error = ""):
		self.render("passwordreset.html",username = username, error = error)
	
	def pass_template_value_recovery_page(self, username = "", error = ""):
		self.render("recovery.html",username = username, error = error)


	def pass_template_value_new_page(self,username = "",logout = "", title = "", content = "",preview = "",
										error = ""):
		# self.response.out.write(error)
		self.render("new.html",username = username,logout = logout,title = title, content = content, 
										preview = preview, error = error)

	def pass_template_value_done_page(self, username = "", logout = "", login = "",signup = "", post = "",comments = "",
									author = "", like_count = "",comment_count = "", post_id = ""):
		self.render("done.html", username = username, logout = logout, login = login, signup = signup, post = post, comments = comments,
									author = author, like_count = like_count,comment_count = comment_count, post_id = post_id)

	def pass_template_values_masthead_page(self):
		self.render("about.html")
	
	def pass_template_value_people_page(self, people = "", username = "", login = "", logout = "", signup = ""):
		self.render("people.html", people = people, username = username, login = login, logout = logout, signup = signup)

	def pass_template_value_tags_page(self, tags = "", username = "", login = "", logout = "", signup = ""):
		self.render("tags.html", tags = tags, username = username, login = login, logout = logout, signup = signup)
		
	def render(self,template,**template_values):
		template = jinja_env.get_template(template)
		page = template.render(template_values)
		self.response.out.write(page)
