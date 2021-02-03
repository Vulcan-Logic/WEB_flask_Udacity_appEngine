from templating import Handler1
from google.appengine.api import memcache

class flushHandler(Handler1):
	
	def get(self):
		memcache.MemcacheFlushRequest()
		self.redirect('/frontpage')
	