import json
from random import randint
from base import BaseHandler
from models.models import User

from google.appengine.ext import ndb

def userExists(username):
    q = User.query(User.name == username)
    return q.count()


def emailExists(email):
    q = User.query(User.email == email)
    return q.count()


class RegisterUser(BaseHandler):
    def post(self):
        username = self.request.get('username')
        email = self.request.get('email')
        password = self.request.get('password')

        self.response.headers['Content-Type'] = 'application/json'
        response = {}

        if (not username) or (not email) or (not password):
            response['success'] = 0
            response['message'] = 'Field(s) empty'

        elif emailExists(email):
            response['success'] = 0
            response['message'] = 'Email already used'

        elif userExists(username):
            response['success'] = 0
            response['message'] = 'Username already in use'

        else:
            user = User()
            user.name = username
            user.email = email
            user.password = password
            user.id = randint(100000,999999)
            key = user.put()

            response['success'] = 1
            response['message'] = 'id:'+str(user.id)+', '+str(key)

            self.session['username'] = username
            self.session['email'] = email

        self.response.write(json.dumps(response))
        self.redirect('/')

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
        self.redirect('/')











