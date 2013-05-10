from Databases import PostsDB
from Databases import UserDB
from Databases import TagsDB
from Databases import CommentsDB
from Databases import PeopleDB
from Databases import PasswordRecovery
from google.appengine.api import memcache


class CachePosts():
	"""never give "" to the parameter order"""

	def loadRecentPostsDb(self, filter = "", order = "", update = False):
		
		# print 'hi'  Seems working but the statement 'db fetch' was never printed. But 'hi' got printed.
		key = 'recentkey'
		postsdb = memcache.get(key)
		if not postsdb or update:
			postsdb = PostsDB.all().order('-date').fetch(30)
			memcache.set(key,postsdb)
			postsdb = list(postsdb)
		return postsdb

	def loadTrendingPostsDb(self, filter = "", order = "",  update = False):

		key = 'trendingkey'
		postsdb = memcache.get(key)
		if not postsdb or update:
			postsdb = PostsDB.all().order(order).fetch(30)
			memcache.set(key,postsdb)
			postsdb = list(postsdb)
		return postsdb

	def loadHelloUserDb(self, userdb, update = False):

		key = 'hellouserkey'
		hellouserdb = memcache.get(key)
		if not hellouserdb or update:
			hellouserdb = PostsDB.all().filter('userdb =',userdb).fetch(30)
			memcache.set(key, hellouserdb)
			hellouserdb = list(hellouserdb)
		return hellouserdb

	def returnPostById(self, p_id, update = False):
		key = "postidkey"
		postdb = memcache.get(key)
		if not postdb or update:
			postdb = PostsDB.get_by_id(int(p_id))
			memcache.set(key, postdb)
		return postdb

	def loadComments(self, contents = "", update = False):
		key = 'commentskey'
		commentsdb = memcache.get(key)
		if not commentsdb or update:
			commentsdb = CommentsDB.all().filter('postsdb =',contents).fetch(10)
			memcache.set(key, commentsdb)
		return commentsdb

class CacheTags():

	def loadAllTagsDb(self, filter = "", update = False):

		key = 'alltagskey'
		tagsdb = memcache.get(key)
		if not tagsdb or update:
			tagsdb = TagsDB.all().fetch(100)
			memcache.set(key,tagsdb)
			tagsdb = list(tagsdb)
		return tagsdb