from templating import Handler2
from databaseBlog import BlogQuery 
from databaseAuth import Authenticator

class historyPageDisplay(Handler2):
	def get(self):
		# check authentication before displaying page.
		cookie=self.request.cookies.get("UD")
		pageName=self.request.get('pageName')
		version=self.request.get('version')
		print pageName
		print version
		if pageName.strip() !="" and version.strip() !="": 
			if cookie:
				vAuth=Authenticator()
				user=vAuth.checkCookie(cookie)
				if user:
					self.display(user,pageName=pageName,version=version)
				else: 
					self.display(pageName=pageName,version=version)	
			else:
				self.display(pageName=pageName,version=version)
		else:
			comment="Error-Invalid Page ID data-Unable to load page from database"
			self.render("historyPageDisplay.html",comment=comment)	
		
	def display(self,user="",pageName="",version=""):
		b=BlogQuery()
		blog=b.getBlogEntryByNameNVersion(pageName,version)
		if blog:
			self.render("historyPageDisplay.html",user=user,pageName=blog.subject,version=blog.version,content=blog.content,comment="")
		else:
			comment="Unable to load page from database - page not found"
			self.render("historyPageDisplay.html",user=user,comment=comment)	
			