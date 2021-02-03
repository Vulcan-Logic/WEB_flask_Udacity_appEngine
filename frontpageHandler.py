from templating import Handler2
from templating import Handler1
from databaseBlog import BlogQuery 
from databaseAuth import Authenticator

class frontpageHandler(Handler2):
	def get(self):
		# check authentication before displaying page.
		cookie=self.request.cookies.get("UD")
		if cookie:
			vAuth=Authenticator()
			user=vAuth.checkCookie(cookie)
			if user:
				self.display(user)
			else: 
				self.display()	
		else:
			self.display()
			
	def display(self,user=""):
		b=BlogQuery()
		blogs=b.getPageNames()
		if blogs.count>0:
			self.render("frontpage.html",user=user,blogs=blogs,comment="")
		else:
			comment="No Pages Found"
			self.render("frontpage.html",user=user,comment=comment)	
			
	def post(self):
		pageName=self.request.get('pageName')
		if pageName != "":
			self.redirect('/%s' %pageName.strip())
		else:
			self.redirect('/')
			