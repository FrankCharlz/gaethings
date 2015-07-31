
from google.appengine.ext import ndb

class News(ndb.Model):
    rId = ndb.IntegerProperty()
    title = ndb.StringProperty()
    body = ndb.TextProperty()
    tags = ndb.StringProperty()
    author = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)#date serves as id, screwing things

class Comment(ndb.Model):
    body = ndb.TextProperty()
    author = ndb.StringProperty()
    news_id = ndb.IntegerProperty()#saves as key to link with news entry
    date = ndb.DateTimeProperty(auto_now_add=True)

