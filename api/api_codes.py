__author__ = 'CharlesMagoti'
from google.appengine.ext import ndb

"""
    This is an API for interaction with other apps
    default response is in json format

    ---Exclude login user response will be as get parameter normal: use secret token

"""

import json
import webapp2
from models.models import User, News


class LoginUser(webapp2.RequestHandler):
    def post(self):
        username_or_email = self.request.get('username_or_email')
        password = self.request.get('password')

        self.response.headers['Content-Type'] = 'application/json'
        response = {}

        if (not username_or_email) or (not password):
            response['success'] = 0
            response['message'] = 'Field(s) empty'

        else:
            result = User.query(
                ndb.AND(
                ndb.OR(User.email == username_or_email, User.name == username_or_email),
                User.password == password)
            )

            response['success'] = result.count() # 0 = failed to get any

            for u in result:
                response['username'] = u.name
                response['email'] = u.email
                response['level'] = u.level
                break #only one result needed


        self.response.write(json.dumps(response))


def news_to_dict(news, with_body=False):
    news_entry = {}
    news_entry['rid'] = news.rId
    news_entry['title'] = news.title
    news_entry['tags'] = news.tags
    news_entry['author'] = news.author
    news_entry['date'] = str(news.date) #convert date to string
    if with_body: news_entry['body'] = news.body  #not normally needed
    return  news_entry



class GetNews(webapp2.RequestHandler):
    DEFAULT_NEWS_IDADI = 50 - 1

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        response = [] #reponse is json array

        start = self.request.get('start')
        idadi = self.request.get('idadi')
        id = self.request.get('id')

        start = self.toNumber(start, 0)
        idadi = self.toNumber(idadi, self.DEFAULT_NEWS_IDADI) + 1 #limit must be > 0

        news = News.query().order(-News.date).fetch(offset=start, limit=idadi)

        for news_entry in news:
            response.append(news_to_dict(news_entry))

        self.response.write(json.dumps(response))

    def toNumber(self, x, default):
        try:
            return int(x)
        except:
            return default


class GetNewsById(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        response = {} #reponse is json object

        id = self.request.get('id')

        try:
            id = int(id)
        except:
            #error
            response['success'] = 0
            response['message'] = 'An error occured'
            self.response.write(json.dumps(response))
            return

        news = News.get_by_id(id);
        if not news:
            #error no news with the id
            response['success'] = 0
            response['message'] = 'No news with the id'
            self.response.write(json.dumps(response))
            return
        else:
            response = news_to_dict(news, True)
            self.response.write(json.dumps(response))



