from Handler import Handler

class MastheadPage(Handler):
	def get(self):
		self.pass_template_values_masthead_page()
		