
import webapp2
from routes import url_mappings


config = {}
config['webapp2_extras.sessions'] = { 'secret_key': 'mama-ndesi'}


app = webapp2.WSGIApplication( url_mappings, debug=True, config=config)



















