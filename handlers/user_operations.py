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
        username = self.request.get('username').strip().lower()
        email = self.request.get('email').strip().lower()
        password = self.request.get('password')

        response = {}

        if (not username) or (not email) or (not password):
            response['success'] = 0
            response['message'] = 'Field(s) empty'

        elif emailExists(email):
            response['success'] = 0
            response['message'] = 'Registration failed, Email already in use'
            self.redirect('/login_register?fail='+response['message'])
            return

        elif userExists(username):
            response['success'] = 0
            response['message'] = 'Registration failed, Username already in use'
            self.redirect('/login_register?fail='+response['message'])
            return

        else:
            user = User()
            user.name = username
            user.email = email
            user.password = password
            user.id = randint(1,1000000)
            key = user.put()

            response['success'] = 1
            response['message'] = 'id:'+str(user.id)+', '+str(key)

            self.session['username'] = username
            self.session['email'] = email
            self.session['level'] = 0

        self.response.write(json.dumps(response))
        self.redirect('/')

class LoginUser(BaseHandler):
    def post(self):
        username_or_email = self.request.get('username_or_email').strip().lower()
        password = self.request.get('password')

        response = {}

        if (not username_or_email) or (not password):
            response['success'] = 0
            response['message'] = 'Field(s) empty'

        else:
            result = User.query(
                ndb.AND(
                    ndb.OR(User.email == username_or_email,
                           User.name == username_or_email
                    ),
                    User.password == password)
            )

            response['success'] = result.count() # 0 = failed to get any

            if not response['success'] :
                self.redirect('/login_register?fail=L')
                return  #break out of the function

            for u in result:
                self.session['username'] = u.name
                self.session['email'] = u.email
                self.session['level'] = u.level
                break #only one result needed

        origin = str(self.request.get('origin'))
        #if not origin: origin = '/'
        self.redirect(origin)


class LogOut(BaseHandler):
    def get(self):
        self.session.clear()
        self.redirect(self.request.referer)






