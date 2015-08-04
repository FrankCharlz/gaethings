from api.api import GetNews, GetNewsById
from handlers.handler import *
from handlers.save_news import *
from handlers.user_operations import *

url_mappings = [
    ('/', MainPage),
    ('/save_news', SaveNews),
    ('/save_comment', SaveComment),
    ('/news_view', ViewNews),
    ('/news_form', NewsForm),
    ('/login_user', LoginUser),
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


url_mappings.extend(api_routes);