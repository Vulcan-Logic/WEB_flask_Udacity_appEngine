from google.appengine.ext import db

class Blog(db.Model):
    subject=db.StringProperty(required=True)
    content=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)
    version=db.IntegerProperty()

class BlogQuery():
    def getAllBlogEntries(self):
        #return db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        return Blog.all().order('-created')
    
    def getLimitedBlogEntries(self,limit=10):
        #q = "SELECT * FROM Blog ORDER BY version DESC LIMIT %d" %limit
        #return db.GqlQuery(q)
        q=Blog.all(limit=5)
        q.order('-created')
        return q
    
    def getLatestBlogEntryByName(self,pageName):
        #q = "SELECT * FROM Blog WHERE subject = '%s' ORDER BY version DESC" %pageName
        #return db.GqlQuery(q).get()
        q=Blog.all()
        q.filter('subject =',pageName)
        q.order('-version')
        return q.get()
    
    def getBlogEntriesByName(self,pageName):
        #q = "SELECT * FROM Blog WHERE subject = '%s' ORDER BY created DESC" %pageName
        #return db.GqlQuery(q)
        q=Blog.all()
        q.filter('subject =',pageName)
        q.order('-version')
        return q
    
    def getPageNames(self):
        #q = "SELECT * FROM Blog ORDER BY subject,version,created DESC" 
        #return db.GqlQuery(q)
        q=Blog.all()
        q.order('-created')
        q.order('subject')
        q.order('-version')
        return q
     
    def getBlogEntryByNameNVersion(self,pageName="",version=""):
        version=int(version)
        q=Blog.all()
        q.filter('subject =',pageName)
        q.filter('version =', version)
        return q.get()    

        
    def putBlogEntry(self,subject="",content="",version=0):
        a = Blog(subject=subject, content=content,version=version)
        a.put()
        return a.key().id()
    
    def getBlogKey(self,pageName='',version=''):
        version=int(version)
        q=Blog.all(keys_only=True)
        q.filter('subject =', pageName)
        q.filter('version =', version)
        return q.get().id()
    
    def updateBlogEntry(self,ID,subject,version,content):
        """"q=Blog.all()
        q.filter('subject =',subject)
        q.filter('version =', version)
        b=q.get()
        b.content=content
        return b.put()"""
        if str(ID).isdigit():
            ID=int(ID)
        blogEntry_k=db.Key.from_path('Blog',ID)
        blogEntry=db.get(blogEntry_k)
        if blogEntry:
            blogEntry.content=content
            blogEntry.put()
            return blogEntry.key().id()
        else:
            return None
        
    
    def getBlogByID(self,ID):
        if str(ID).isdigit():
            ID=int(ID)
        blogEntry_k=db.Key.from_path('Blog',ID)
        blogEntry=db.get(blogEntry_k)
        if blogEntry:
            return blogEntry
        else:
            return None  