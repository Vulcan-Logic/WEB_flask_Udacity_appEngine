import re
from templating import Handler1
from databaseAuth import Authenticator

class newuserHandler(Handler1):
	pageName=None
	def render_front(self,user="",email="", error="",error1="",error2="",error3="",error4="",pageName='newUser'):
		self.render("newuserpage.html",user=user,email=email,error=error,error1=error1,error2=error2,error3=error3,error4=error4,pageName=pageName)
	
	def get(self):
		#render new user form and accept details
		src=self.request.get("src")
		if src is not None:
			self.pageName = src.strip()
		self.render_front()
		
	
	def post(self):
		#accept new user details and add to the database, set cookie and send to frontpage
		user=self.request.get("username")
		password=self.request.get("password")
		rpassword=self.request.get("verify")
		email=self.request.get("email")
		error1=""
		error2=""
		error3=""
		error4=""
		error=""
		if user and password:
			#check for validity of username, email and password
			if not valid_username(user) or not valid_password(password):
				proceed=False
				if not valid_username(user):
					error1="Invalid Username"
				if not valid_password(password):
					error2="Invalid Password"
			else:
				proceed=True
		else:
			proceed=False
			if not user:
				error1="User Name cannot be blank"
			if not password:
				error2="Password cannot be blank"
				
		#check for valid email if supplied		
		if email:
			if not valid_email(email):
				error4="Invalid Email"
				proceed=False

		if proceed:		
			#values passed are valid, try to proceed	
			vAuth=Authenticator()
			#check if username exists
			if vAuth.checkUser(user):
					error1="User Name already exists"
			else:
				#username does not exist try to insert a new user record		
				if password==rpassword:
					vAuthReply=vAuth.putnewUser(user, password)
					if vAuthReply:
					# user successfully added, try to get a new cookie
						cookie=vAuth.putCookieValue(user)
						if cookie:
							#send a new response with set cookie in it
							#print "setting cookie value to:" + cookie
							self.response.headers.add_header("Set-Cookie", "UD=%s;Path=/" %cookie)
							#self.redirect("/wpr")
							if self.pageName is not None:
								self.redirect("/%s" %self.pageName)
							else:
								self.redirect('/')
						else:
							#cookie value is none so an error occurred
							error="error generating new cookie"	
					else:
							#error in inserting a new user in the database
						error="error inserting new user records"	
				else:
					error3="Passwords do not match"
					#if not email:
				#error4="Email cannot be blank"	
		self.render_front(user=user,email=email,error1=error1,error2=error2,error3=error3,error4=error4,error=error)					

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$") 
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
	return USER_RE.match(username)

def valid_password(password):
	return PASS_RE.match(password)

def valid_email(email):
	return EMAIL_RE.match(email)