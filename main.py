import os
import urllib

import jinja2
import urlparse
import webapp2
import json

from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from datetime import datetime
from lanora import SaveNews

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



class MainPage(webapp2.RequestHandler):
    NEWS_TO_QUERY = 4;
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
        d = self.request.get('d')
        try:
            #backward compatibility
            date = datetime.strptime(d, '%Y-%m-%d_%H:%M:%S')#2014-10-18_03:55:56
        except:
            date = datetime.strptime(d, '%Y-%m-%d_%H:%M:%S.%f')#2014-10-18_03:55:56
            pass

        news = News.query(News.date == date).fetch(1)

        template_values = {
            'news': news
        }

        template = JINJA_ENVIRONMENT.get_template('news_view.html')
        self.response.write(template.render(template_values))

class NewsForm(webapp2.RequestHandler):
    def get(self):

        template_values = {
        }

        template = JINJA_ENVIRONMENT.get_template('news_form.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
                                  ('/', MainPage),
                                  ('/save_news', SaveNews),
                                  ('/news_view', ViewNews),
                                  ('/news_form', NewsForm)
                                  ], debug=True)



















