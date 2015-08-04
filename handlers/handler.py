from base import BaseHandler
from google.appengine.ext import ndb
from webapp2_extras import sessions
from base import *
from random import randint
import webapp2
from models.models import *


class MainPage(BaseHandler):
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


class ViewNews(BaseHandler):
    def get(self):
        id = int(self.request.get('d'))

        news = News.get_by_id(id);

        comments = Comment.query(Comment.news_id == news.rId). \
            order(-Comment.date).fetch(limit=16)

        template_values = {
            'news': news,
            'comments': comments,
            'news_id': id,
            'name': self.session.get('username'),
            }

        template = JINJA_ENVIRONMENT.get_template('news_view.html')
        self.response.write(template.render(template_values))

class ViewLoginRegister(BaseHandler):
    def get(self):
        template_values = {
            'origin': str(self.request.referer),
            'fail': self.request.get('fail')
        }
        template = JINJA_ENVIRONMENT.get_template('login_register.html')
        self.response.write(template.render(template_values))


class NewsForm(BaseHandler):
    def get(self):
        #template_values = {}
        template = JINJA_ENVIRONMENT.get_template('news_form.html')
        self.response.write(template.render())

class SaveComment(BaseHandler):
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

class ComingSoon(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('coming_soon.html')
        self.response.write(template.render())


