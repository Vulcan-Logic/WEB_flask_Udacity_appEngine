from templating import Handler2
from databaseBlog import BlogQuery
from databaseAuth import Authenticator
from google.appengine.api import memcache

class wikiPageHandler(Handler2):
    def get(self,pageName): 
        # check authentication before displaying page.
        if pageName.strip()=="/":
            pageName="root"
        else:    
            pageName=pageName.strip()[1:]
        """check if page exists, if it does redirect to front page"""
        """else redirect to edit page with page name"""
        if self.checkPage(pageName):
            self.displayPage(pageName)
        else:
            self.redirect('/_edit/%s' %pageName)
        
    def checkPage(self,pageName):
        """check memcache/database for records"""
        version=memcache.get(pageName)
        if version is None:
            version=0
        key=pageName.strip()+':'+'%d' %version
        content=memcache.get(key)
        #print 'CP:getting from memcache pagename: '+ pageName
        #print 'CP:storing in memcache version: %d' %version
        #print 'CP:storing in memcache key: '+ key   
        if content is None:
            b=BlogQuery()
            blog=b.getLatestBlogEntryByName(pageName)
            if blog is not None:
                content=blog.content
                version=blog.version
                print blog.content
                print blog.version
                key=pageName.strip()+':'+'%d' %version
                memcache.add(pageName,version)
                if not memcache.add(key,content):
                    print "unable to store value"
                retVal=True
            else:
                #print 'WP query did not return the page contents'
                retVal=False
        else:
            retVal=True
        return retVal
    
    def displayPage(self,pageName):
        #print 'displayPage :' + pageName
        cookie=self.request.cookies.get("UD")
        if cookie:
            vAuth=Authenticator()
            user=vAuth.checkCookie(cookie)
            if user:
                self.display(user,pageName)
            else: 
                self.display(pageName=pageName)    
        else:
            self.display(pageName=pageName)
    
    def display(self,user="",pageName=""):
        version=memcache.get(pageName)
        if version is None:
            version=0
        key=pageName.strip()+':'+'%d' %version
        content=memcache.get(key)
        #print 'DSP: getting from memcache pagename: '+ pageName
        #print 'DSP: getting frm memcache version: %d' %version
        #print 'DSP: getting frm memcache key: '+ key 
        if content is None: 
            #print "DSP:unable to retrieve"
            self.render('displayPage.html',user=user,error="Unable to retrieve page contents")
        else:
            self.render("displayPage.html",user=user,content=content, pageName=pageName)