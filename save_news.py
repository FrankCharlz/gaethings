import urllib

import jinja2
import webapp2
import json
from random import randint

from google.appengine.ext import ndb
from google.appengine.ext import blobstore

from datetime import datetime
from models.models import News


class SaveNews(webapp2.RequestHandler):
    def post(self):
        title = self.request.get('title')
        body  = self.request.get('news_body')
        tags = self.request.get('tags')
        author = self.request.get('author')

        self.response.headers['Content-Type'] = 'application/json'
        response = {}

        if (not title) or (not body):
            response['success'] = 0
            response['message'] = 'Field(s) empty'

        else:
            n = News();
            n.title = title
            n.body = body
            n.author = author
            n.tags = tags
            n.put()
            response['success'] = 1
            response['message'] = 'News added successfully'
        #self.redirect('/')
        self.response.write(json.dumps(response))




