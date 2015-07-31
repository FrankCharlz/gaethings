
from google.appengine.ext import ndb

class News(ndb.Model):
    title = ndb.StringProperty()
    body = ndb.TextProperty()
    tags = ndb.StringProperty()
    author = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Comment(ndb.Model):
    body = ndb.TextProperty()
    author = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

