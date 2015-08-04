
import webapp2
import json
from random import randint


from datetime import datetime
from base import BaseHandler
from models.models import News


class SaveNews(BaseHandler):
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
            n.author = self.session.get('username')
            n.tags = tags
            n.rId = randint(0, 999999999)#God doesnt play dice, I do
            n.put()
            response['success'] = 1
            response['message'] = 'News added successfully'
        #self.redirect('/')
        self.response.write(json.dumps(response))




