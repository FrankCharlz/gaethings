
from google.appengine.ext import ndb

class News(ndb.Model):
    rId = ndb.IntegerProperty()
    title = ndb.StringProperty()
    body = ndb.TextProperty()
    tags = ndb.StringProperty(indexed=False)
    author = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Comment(ndb.Model):
    body = ndb.TextProperty()
    author = ndb.StringProperty(indexed=False)
    news_id = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class User(ndb.Model):
    id = ndb.IntegerProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    level = ndb.IntegerProperty(default=0)
    profile_photo_key = ndb.BlobKeyProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)