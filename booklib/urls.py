from django.urls import path

from .views import get_main_page, get_new_book, get_new_person, give_book, get_bookobj, return_book, auth_user, get_data_person
from .utils import send_debt_email
urlpatterns = [
    path('', get_main_page, name='main'),
    path('add_book/', get_new_book, name='new_book'),
    path('add_person/', get_new_person, name='new_person'),
    path('give_book/', give_book, name='give_book'),
    path('give_book/get_bookobj/', get_bookobj, name='get_bookobj'),
    path('return_book/', return_book, name = 'return_book'),
    path('login/', auth_user, name='login'),
    # path('person/', get_person_data, name='person_data'),
    path('give_book/get_data_person/', get_data_person, name='get_data'),
    path('send_email/', send_debt_email, name='debt_email'),
]