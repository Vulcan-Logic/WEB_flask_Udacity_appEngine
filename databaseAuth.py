#WIP
import random
import string
import hmac

from google.appengine.ext import db

class User(db.Model):
    username=db.StringProperty(required=True)
    password=db.StringProperty(default="")
    created=db.DateTimeProperty(auto_now_add=True)

class passwordRandom(db.Model):
    user=db.StringProperty(required=True)
    PWrandom=db.StringProperty()
     
class cookieUser(db.Model):
    user=db.StringProperty(required=True)
    cookie=db.StringProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)
    #expiryDate=db.DateProperty()

class Authenticator():

    def putnewUser(self,user,password):
        # details of inserting a new user in database procedure.
        # generate a new random code for the password field and store it in a password-random database
        # combine supplied user password and random code and generate a new database pw field value
        # store new user name and coded password in database.
        vUser=User(username=str(user).strip())
        vUserSalt=str(make_salt(size=10)).strip()
        vSecuredPassword=make_secure_password(salt=vUserSalt, password=password)
        vPWRandom=passwordRandom(user=user,PWrandom=vUserSalt)
        vPWRandom.put()
        vUser.password=vSecuredPassword
        vUser.put()
        if vPWRandom and vUser:
            return True
        else:
            return False 
    
    def checkUser(self,user):
        #check if user name exists in database
        #if so return the userID otherwise return None
        vUserQ=User.all()
        vUserQ.filter("username =", user)
        vUser=vUserQ.get()
        if vUser:
            return True
        else:
            return None
        
    def return_secure_password(self,user):
        vUserQ=User.all()
        vUserQ.filter("username =", user)
        vUser=vUserQ.get()
        if vUser:
            return vUser.password
        else:
            return None
    
        
    def checkUserPW(self, user, password):
        #check if supplied password exists in database for given user
        #get the salt from the PWRandom table for the given user
        #get the stored password from the user table
        #make the secured password again using the stored/retrieved salt and password parameter
        #check the new secured password is equal to the password stored in table. 
        vPWRandom=self.getStoredSalt(user)
        if vPWRandom: #salt is not empty - hence user exists, proceed
            if self.return_secure_password(user)==make_secure_password(vPWRandom, password):
                return 1
            else: 
                return 2
        else: 
            return 3
    
    def getStoredSalt(self,user=""):
        if self.checkUser(user): #if not None then proceed
            vPWRandomQ=passwordRandom.all()
            vPWRandomQ.filter("user =", user)
            vPWRandom=vPWRandomQ.get()
            if vPWRandom:
                return str(vPWRandom.PWrandom)
            else:
                return None
        
    def changePassword(self,user,newPW,oldPW):
        # change password for given user
        # check if old PW is valid, if not return error
        # if old PW is valid, generate new and update random value stored in password-random database
        # generate a new coded password value and update the user database.
        pass 

    def checkCookie(self,cookie):
        #split the cookie into salt and value
        #get the user and the stored cookie value from the salt  
        #encrypt the obtained cookie value and salt and see if the passed cookie 
        #is valid or not. 
        #print "get cookie gets the value of: " + cookie
        cookie1=str(cookie).split("|")
        #print "cookie salt is:" + cookie1[0]
        cookie_k = db.Key.from_path('cookieUser', cookie1[0])
        vCookieObj=db.get(cookie_k)
        #print "Got here"
        if vCookieObj:
            #print "got here too"
            vCookieValue=vCookieObj.cookie
            #print "cookie value is: " + vCookieValue
            #print "generated secure password is: " +  str(make_secure_password(cookie1[0],vCookieValue))
            #print "cookie 1 value is: " + cookie1[1]
            if str(make_secure_password(cookie1[0],vCookieValue))==str(cookie1[1]):
                user1=vCookieObj.user
                #print "User according to cookie is:" + user1
                return user1
            else:
                return None
        else:
            return None

    def putCookieValue(self,user):
        #generate a new cookie value for the said user.
        salt=str(make_salt(10)).strip()
        cookieValue=str(make_salt(size=15)).strip()
        vCookie=cookieUser(key_name=salt,user=user,cookie=cookieValue)
        vCookieKey = vCookie.put()
        if vCookieKey:
            vCookieReturn2=make_secure_password(salt,cookieValue)
            vCookieReturn=str("%s|%s" %(salt,vCookieReturn2)) 
            return vCookieReturn     
        else:
            return None
        
    def remove_cookie(self,cookie):
        cookie1=str(cookie).split("|")
        #print "cookie salt is:" + cookie1[0]
        cookie_k = db.Key.from_path('cookieUser', cookie1[0])
        vCookieObj=db.get(cookie_k)
        if vCookieObj:
            vCookieObj.delete()
            return True
        else:
            return None
        
            
    def test_coding_password(self,user,password):
        vSalt=self.getStoredSalt(user)
        if vSalt:
            return make_secure_password(vSalt,password)
        else:
            return None    
            
def make_salt(size=5, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))  


def make_secure_password(salt,password):
    #return secure password here
    return hmac.new(salt,password).hexdigest()



  
