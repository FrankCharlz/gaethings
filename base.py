from datetime import datetime

__author__ = 'CharlesMagoti'
import os
from webapp2_extras import sessions
import webapp2

import jinja2
from jinja2 import Environment

def muda_ulopita(d):
    ct = datetime.now()
    seconds = int((ct - d).total_seconds())
    if seconds > 3600 * 24 * 7:
        return ''
    elif seconds > 3600 * 24 :
        return ' | <b>'+str(seconds//3600//24)+' days </b>'
    elif seconds > 3600:
        return ' | <b>'+str(seconds//3600)+'h </b>'
    elif seconds > 60:
        return ' | <b>'+str(seconds//60)+'m </b>'
    else:
        return ' | <b>'+str(seconds)+'s </b>'

def get_id(entity):
    #return the auto-generated entity id..
    return entity.key.id()


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

JINJA_ENVIRONMENT.filters['muda_ulopita'] = muda_ulopita
JINJA_ENVIRONMENT.filters['get_id'] = get_id

class BaseHandler(webapp2.RequestHandler):

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        #set env to accept sessions
        JINJA_ENVIRONMENT.globals['session'] = self.session_store.get_session()

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)


    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

