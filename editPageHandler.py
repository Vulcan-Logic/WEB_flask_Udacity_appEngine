from templating import Handler1
from databaseBlog import BlogQuery
from databaseAuth import Authenticator
from google.appengine.api import memcache


class editPageHandler(Handler1):
    user=""
    def render_front(self, subject="",content="",error=""):
        self.render("editPage.html",user=self.user,subject=subject,content=content,error=error)

    def get(self,pageName): 
        # check authentication before displaying page.
        pageName=pageName.strip()[1:]
        self.pageName=pageName
        cookie=self.request.cookies.get("UD")
        if cookie:
            vAuth=Authenticator()
            user=vAuth.checkCookie(cookie)
            if user:
                self.user=user
                content=self.checkPage(pageName)
                if content is not None:
                    self.render_front(content=content)
                else:
                    self.render_front()
            else: # user is not logged in 
                self.redirect('/login?src=_edit/%s' %pageName)    
        else: #user is not logged in 
            self.redirect('/login?src=_edit/%s' %pageName)
            
    def checkPage(self,pageName):
        version=memcache.get(pageName)
        if version is None:
            return version
        else:
            key=pageName.strip()+':'+'%d' %version
            content=memcache.get(key)
            return content
        
        
    def post(self,pageName):
        """ set the page name """
        pageName=pageName.strip()[1:]
        content = self.request.get('content')
        # get the right version
        b=BlogQuery()
        blog=b.getLatestBlogEntryByName(pageName)
        
        if blog is not None:
            version=blog.version
        else: 
        #blog is none - no entry for page name
            version = 0    
        if pageName and content:
            oldVersion=version
            version=version+1
            qid=b.putBlogEntry(pageName,content,version)
            if qid:
                key=pageName.strip()+':'+'%d' %oldVersion
                memcache.delete(pageName)
                memcache.delete(key)
                key=pageName.strip()+':'+'%d' %version
                #print 'storing in memcache pagename: '+ pageName
                #print 'storing in memcache version: %d ' %version
                #print 'storing in memcache key: '+ key
                memcache.add(pageName,version)
                memcache.add(key,content)
                #print "EP saved the entry"
                url="/%s" %pageName
                #print "EP redireccting to:" + url
                self.redirect(url)
            else:
                self.render_front(pageName,content,error="Error could not save to Database")     
        else:
            self.render_front(pageName,content,error="You need to add page content before it can be saved")
