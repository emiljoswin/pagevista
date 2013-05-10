from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import images

class DefImageDB(db.Model):
	"""The class contains a single image file that is used as default display_pic of the user"""
	def_image = db.BlobProperty()

class UserDB(db.Model):
	"""This class is used to store information about the users.
	It includes their photos and description as well. The people whom 
	the username follows is obtained from the PeopleDB class.
	"""
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email_id = db.StringProperty(required = True)
	user_image = db.BlobProperty()
	user_description = db.StringProperty()

class PostsDB(db.Model):
	""" is associted with UserDB so that a user can have as many posts
	as he wants. The PeopleDB keeps account of the people who already
	voted on a particular post
	"""
	userdb = db.ReferenceProperty(UserDB,collection_name = "posts")
	title = db.StringProperty()
	subject = db.StringProperty()
	post = db.TextProperty()
	like_count = db.IntegerProperty()
	like = db.IntegerProperty(default = 0)
	dislike = db.IntegerProperty(default = 0)
	author = db.StringProperty()#the author of the post
	date = db.DateTimeProperty(auto_now_add = True)
	comment_count = db.IntegerProperty(default = 0)
	rating = db.FloatProperty(default = 0.0)# 0.2  = dislike, 0.4 = like, 0.6 = comment
	tag1 = db.StringProperty()
	tag2 = db.StringProperty()
	tag3 = db.StringProperty()
	"""
	saved_title  = db.StringProperty()
	saved_subject = db.StringProperty()
	saved_post = db.StringProperty()	
	store the saved post only. 
	would need to make it possible to save more than one post at a time 
	for a single user. At the moment it is not possible with this single 
	saved_post"""

	upvotes = db.IntegerProperty()
	downvotes = db.IntegerProperty()
class TagsDB(db.Model):
	postsdb = db.ReferenceProperty(PostsDB, collection_name = "posts_tags")
	tagname = db.StringProperty()
	post_id = db.IntegerProperty()

class CommentsDB(db.Model):
	"""is associated with Posts so that more than one comment can occur
	in one post. The PeopleDB is used to keep account of the people who
	alredy voted on a particular comment.
	"""
	postsdb = db.ReferenceProperty(PostsDB,collection_name = "comments")
	commenter = db.StringProperty()
	comment = db.TextProperty()
	upvotes = db.IntegerProperty()
	downvotes = db.IntegerProperty()

class PeopleDB(db.Model):
	"""the purpose of this class is to represent the followers of the 
	users and to know about who all voted for a particular 
	post or comment"""
	userdb = db.ReferenceProperty(UserDB, collection_name = "followers") 
	postsdb = db.ReferenceProperty(PostsDB, collection_name = "post_voters")
	commentsdb = db.ReferenceProperty(CommentsDB, collection_name = "comment_voters")
	people_followed = db.StringProperty()# the one who is being followed ie whos_post
	people_follows = db.StringProperty() # the one who follows whos_post

	posts_id = db.IntegerProperty()#to store the id of post liked by people_liked
	username_liked = db.StringProperty()#to store all the people who have clicked like button
	has_liked_boolean = db.BooleanProperty() #tookout default = false 
	"""the one who is followed"""

class PasswordRecovery(db.Model):
	random_url = db.StringProperty()
	reset = db.BooleanProperty(default = False)
	username = db.StringProperty()