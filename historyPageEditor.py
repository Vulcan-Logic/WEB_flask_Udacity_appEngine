from templating import Handler1
from databaseBlog import BlogQuery
from databaseAuth import Authenticator
from google.appengine.api import memcache


class historyPageEditor(Handler1):
    user=""
    
    def render_front(self, subject="",content="",error=""):
        self.render("historyEditPage.html",user=self.user,subject=subject,content=content,error=error)

    def get(self): 
        # check authentication before displaying page.
        pageName=self.request.get("pageName")
        version=self.request.get("version")
        cookie=self.request.cookies.get("UD")
        if cookie:
            vAuth=Authenticator()
            user=vAuth.checkCookie(cookie)
            if user:
                self.user=user
                content=self.getContent(pageName,version)
                if content:
                    self.render_front(content=content)
                else:
                    self.render_front(error="Unable to fetch contents from database")    
            else: # user is not logged in 
                self.redirect('/login?src=_history_edit?pageName=%s&version=%s' %(pageName,version))    
        else: #user is not logged in 
            self.redirect('/login?src=_history_edit?pageName=%s&version=%s' %(pageName,version))
            
    def getContent(self,pageName,version):
        b=BlogQuery()
        blog=b.getBlogEntryByNameNVersion(pageName,version)
        if blog is not None:
            return blog.content
        else:
            return None
        
        
    def post(self):
        newContent = self.request.get('content')
        pageName=self.request.get("pageName")
        version=self.request.get("version")
        oldContent=self.getContent(pageName,version)
        # get the right version
        if newContent.strip() != "":
            if newContent.strip() != oldContent.strip():#content has changed - save the page
                b=BlogQuery()            
                qid=b.getBlogKey(pageName,version)
                sid=b.updateBlogEntry(qid,pageName,version,newContent)
                #update the record with the same key
                #check if the save was successful and redirect
                url="/_history_dis?pageName=%s&version=%s" %(pageName,version)
                self.redirect(url)
            else: # content has not changed, redirect to history page
                url="/_history_dis?pageName=%s&version=%s" %(pageName,version)
                print url
                self.redirect(url)
        else:
            self.render_front(pageName,newContent,error="Cannot save page with blank content")
