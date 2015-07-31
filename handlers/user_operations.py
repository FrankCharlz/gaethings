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
            response['message'] = 'id:'+str(user.id)+',key:'+str(key)

        self.response.write(json.dumps(response))

class LoginUser(BaseHandler):
    def post(self):
        username_or_email = self.request.get('username_or_email')
        password = self.request.get('password')

        self.response.headers['Content-Type'] = 'application/json'
        response = {}

        username = ''
        email = ''

        if (not username_or_email) or (not password):
            response['success'] = 0
            response['message'] = 'Field(s) empty'

        elif '@' in username_or_email:
            #it is an email...
            email = username_or_email
            response['email'] = email
            query = User.query(ndb.AND(User.email == email, User.password == password))
            response['success'] = query.count()
        else:
            #it is a user name
            username = username_or_email
            response['username'] = username
            query = User.query(ndb.AND(User.name == username, User.password == password))
            response['success'] = query.count()

        self.response.write(json.dumps(response))