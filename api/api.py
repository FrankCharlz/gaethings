__author__ = 'CharlesMagoti'
from google.appengine.ext import ndb

"""
    This is an API for interaction with other apps
    default response is in json format

    ---Exclude login user response will be as get parameter normal: use secret token

"""

import json
from base import BaseHandler
from models.models import User

class LoginUser(BaseHandler):
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
                self.session['username'] = u.name
                self.session['email'] = u.email
                self.session['level'] = u.level
                break #only one result needed


        self.response.write(json.dumps(response))

