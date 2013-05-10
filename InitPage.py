from google.appengine.api import images
from Handler import Handler
from Databases import DefImageDB
from google.appengine.ext import blobstore
from google.appengine.ext import db

class ImageLoader(Handler):
	def get(self):
		image_id = db.get(self.request.get("img_id"))
		if image_id:
			self.response.headers['Content-Type']="image/png"
			self.response.out.write(image_id.def_image)
		else:
			self.response.out.write("no image")


class InitPage(Handler):
	def get(self):
		defimagedb = DefImageDB.all().fetch(1)
		key = "no_key_found"
		for i in defimagedb:
			key = i.key()
		self.pass_template_value_init_page(image_id_key = key)

	def post(self):
		default_image = images.resize(self.request.get('def_img'),90,90)
		defimagedb = DefImageDB(def_image = db.Blob(default_image))
		defimagedb.put()
		self.redirect('/init')
