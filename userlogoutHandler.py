from templating import Handler1
from databaseAuth import Authenticator

class userlogoutHandler(Handler1):
		
	def get(self):
		pageName=None
		cookie=self.request.cookies.get("UD")
		src=self.request.get("src")
		print src
		if src is not None:
			src=src.strip()
			if src=='login':
				pageName=self.request.get('pageName')
				print 'in the logout method with pageName %s' %pageName
				if pageName is not None:
					pageName=pageName.strip()
			else:
				pageName=src.strip()	
					
		if cookie:
			vAuth=Authenticator()
			user=vAuth.checkCookie(cookie)
			if user:
				if vAuth.remove_cookie(cookie):
					self.response.headers.add_header("Set-Cookie", "UD=;Path=/")
					if pageName is not None:
						self.redirect('/%s' %pageName)
					else:
						self.redirect('/')# pageName is none 
			else: 
				self.response.headers.add_header("Set-Cookie", "UD=;Path=/")
				if pageName is not None:
					self.redirect('/%s' %pageName)
				else:
					self.redirect('/')# pageName is none 	
		else:
			self.response.headers.add_header("Set-Cookie", "UD=;Path=/")
			if pageName is not None:
				self.redirect('/%s' %pageName)
			else:
				self.redirect('/')# pageName is none
		
					