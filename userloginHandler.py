from templating import Handler1
from databaseAuth import Authenticator

class userloginHandler(Handler1):
	
	def render_front(self,user="",error="",pageName='login'):
		self.render("userloginpage.html",user=user,error=error,pageName=pageName)	
		
	def get(self):
		pageName=self.request.get('src').strip()
		cookie=self.request.cookies.get("UD")
		if cookie and pageName:
			print pageName
			self.redirect("/logout?src=login&pageName=%s" %pageName)
		elif cookie:
			self.redirect("/logout?src=login")
    	#render new user form and accept details
		self.render_front()
	
	def post(self):
		#check if user exists
		#check if password matches that on file
		#generate a new cookie and set it in the response
		#redirect the browser to the main page
		user=self.request.get("user")
		password=self.request.get("password")
		pageName=self.request.get('src').strip()
		vAuth = Authenticator()
		error=""
		if vAuth.checkUser(user):
			if vAuth.checkUserPW(user, password)==1:
				#add a new cookie. 
				cookie=vAuth.putCookieValue(user)
				if cookie:
					#send a new response with set cookie in it
					self.response.headers.add_header("Set-Cookie", "UD=%s;Path=/" %cookie)
					print "in post pageName is %s" %pageName
					if pageName is not None:
						self.redirect('/%s' %pageName)
					else:
						self.redirect('/')	
				else:
					#cookie value is none so an error occurred
					error="Error generating new cookie"	
			else:
				error="Incorrect password"
		else:
			error="User: %s Not found in database" %user
			user=""
		if error:
			self.render_front(user,error)
