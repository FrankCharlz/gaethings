import os
import urllib

import jinja2
import urlparse
import webapp2
import json

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from datetime import datetime
from save_news import SaveNews

from models.models import News
from models.models import Comment

from random import randint

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    return ndb.Key('Guestbook', guestbook_name)

def iRandom():
    return randint(100000,999999)


class MainPage(webapp2.RequestHandler):
    NEWS_TO_QUERY = 6
    def get(self):
        start_at = self.request.get('start')
        start_at = 0 if (not start_at) else int(start_at)#if start not number janga
        start_at = 0 if (start_at < 0) else start_at #if start is negative

        news = News.query().order(-News.date).fetch(offset=start_at, limit=self.NEWS_TO_QUERY)

        template_values = {
            'news': news,
            'next_story': (start_at + self.NEWS_TO_QUERY),
            'prev_story': (start_at - self.NEWS_TO_QUERY)
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))



class ViewNews(webapp2.RequestHandler):
    def get(self):
        rid = int(self.request.get('d'))

        news = News.query(News.rId == rid).fetch(1)
        comments = Comment.query(Comment.news_id == rid).\
            order(-Comment.date).fetch(limit=16)

        template_values = {
            'news': news,
            'comments': comments,
            'news_id': rid
        }

        template = JINJA_ENVIRONMENT.get_template('news_view.html')
        self.response.write(template.render(template_values))

class NewsForm(webapp2.RequestHandler):
    def get(self):

        template_values = {
        }

        template = JINJA_ENVIRONMENT.get_template('news_form.html')
        self.response.write(template.render(template_values))


class SaveComment(webapp2.RequestHandler):
    def post(self):
        body  = self.request.get('comment_body')
        author  = self.request.get('author')
        news_id  = self.request.get('news_id')

        if body and author:
            c = Comment()
            c.author = author
            c.body = body
            c.news_id = int(news_id)
            c.put()

        self.redirect('/news_view?d='+news_id)

app = webapp2.WSGIApplication([
                                  ('/', MainPage),
                                  ('/save_news', SaveNews),
                                  ('/save_comment', SaveComment),
                                  ('/news_view', ViewNews),
                                  ('/news_form', NewsForm)
                                  ], debug=True)



















