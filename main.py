import os
import webapp2
import jinja2
import hashlib
from AboutPage import AboutPage
from SignupPage import SignupPage
from HelloUserPage import HelloUserPage
from LogoutPage import LogoutPage
from LoginPage import LoginPage
from NewPage import NewPage
from DonePage import DonePage
from HelloUserPage import ImagePage
from InitPage import InitPage
from InitPage import ImageLoader
from UploadImagePage import UploadImagePage
from MastheadPage import MastheadPage
from RecentPage import RecentPage
from TrendingPage import TrendingPage
from AllTimeGreatPage import AllTimeGreatPage
from SearchPage import SearchPage
from TagHandlerPage import TagHandlerPage
from PasswordResetPage import PasswordResetPage
from RecoveryPage import RecoveryPage
from PeoplePage import PeoplePage
from TagsPage import TagsPage
from WelcomePage import WelcomePage
""" Call the default as the first page after loading the app. It contains some datastore entries that 
are defaults for example, userimage etc"""


app = webapp2.WSGIApplication([ ('/init', InitPage),
								('/',RecentPage),
								('/welcome',WelcomePage),
								('/blogname',AboutPage),
								('/recent',RecentPage),
								('/trending',TrendingPage),
								('/all_time_great',AllTimeGreatPage),
								('/search/(\w*)',SearchPage),
								('/tag/(\w*)',TagHandlerPage),
								('/signup' ,SignupPage),
								('/login',LoginPage),
								('/password_reset',PasswordResetPage),
								('/recovery/(\w+)',RecoveryPage),
								('/hello_user/(\w*)',HelloUserPage),
								('/img',ImagePage),
								('/img_def',ImageLoader),
								('/upload_image',UploadImagePage),
								('/logout',LogoutPage),
								('/new',NewPage),
								('/done/(\d+)',DonePage),
								('/people',PeoplePage),
								('/tags',TagsPage),
								('/about',MastheadPage)],
                                 debug=True)