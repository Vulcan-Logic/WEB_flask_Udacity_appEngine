import webapp2
from newuserHandler import newuserHandler
from userloginHandler import userloginHandler
from userlogoutHandler import userlogoutHandler
from frontpageHandler import frontpageHandler
from editPageHandler import editPageHandler
from wikiPageHandler import wikiPageHandler
from historyPageEditor import historyPageEditor
from historyPageDisplay import historyPageDisplay
from historyPageHandler import historyPageHandler


PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/signup',newuserHandler),('/logout',userlogoutHandler),('/login',userloginHandler),('/frontpage', frontpageHandler),('/_history_edit',historyPageEditor),('/_history_dis',historyPageDisplay),('/_history'+ PAGE_RE, historyPageHandler),('/_edit' + PAGE_RE,editPageHandler),(PAGE_RE,wikiPageHandler)], debug = True)

