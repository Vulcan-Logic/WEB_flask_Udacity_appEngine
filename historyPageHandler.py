from templating import Handler1
from databaseBlog import BlogQuery 
from databaseAuth import Authenticator

#displays all the versions of a page

class historyPageHandler(Handler1):
	def get(self,pageName):
		# check authentication before displaying page.
		cookie=self.request.cookies.get("UD")
		pageName=pageName.strip()[1:]
		if cookie:
			vAuth=Authenticator()
			user=vAuth.checkCookie(cookie)
			if user:
				self.display(user,pageName=pageName)
			else: 
				self.display(user="",pageName=pageName)	
		else:
			self.display(user="",pageName=pageName)
			
	def display(self,user,pageName):
		b=BlogQuery()
		blogs=b.getBlogEntriesByName(pageName)
		if blogs.count>0:
			self.render("historyPages.html",user=user,pageName=pageName,blogs=blogs,comment="")
		else:
			comment="No Pages Found"
			self.render("historyPages.html",user=user,pageName=pageName,comment=comment)	
			