from django.urls import path

from .views import get_main_page, get_new_book, get_new_person, give_book, get_bookobj, return_book
from .Yulia import get_rait_page

urlpatterns = [
    path('', get_main_page, name='main'),
    path('add_book/', get_new_book, name='new_book'),
    path('add_person/', get_new_person, name='new_person'),
    path('give_book/', give_book, name='give_book'),
    path('give_book/get_bookobj/', get_bookobj, name='get_bookobj'),
    path('return_book/', return_book, name = 'return_book'),
    path('raiting_book/', get_rait_page, name = 'raiting'),
]