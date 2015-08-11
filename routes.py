from api.api import *
from handlers.handler import *
from handlers.save_news import *
from handlers.user_operations import *

url_mappings = [
    ('/', MainPage),
    ('/news', MainPage),
    ('/save_news', SaveNews),
    ('/save_comment', SaveComment),
    ('/news/view/(\d+)', ViewNews), #stupidity
    ('/news/view', ViewNews),
    ('/news_form', NewsForm),
    ('/login_user', LoginUser),
    ('/login_register', ViewLoginRegister),
    ('/register_user', RegisterUser),
    ('/logout', LogOut),
    ('/events', ComingSoon),
    ('/posters', ComingSoon),
    ('/profile', ComingSoon),
    ('/console', ComingSoon)
]


api_routes = [
    ('/api/get_news',GetNews),
    ('/api/get_news_by_id',GetNewsById)
]


url_mappings.extend(api_routes)

#5760616295825408-sample news id..