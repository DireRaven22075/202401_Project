from . import views
from django.urls import path
from .views import Everytime
from asgiref.sync import async_to_sync

urlpatterns = [
    path('', Everytime.home, name='home'),
    path('connect/', Everytime.ev_login, name='login'),
    path('connect_info/', Everytime.ev_login, name='login_info'),
    path('get-content/', async_to_sync(Everytime.ev_free_field), name='free_field'),
    path('post/', async_to_sync(Everytime.ev_post), name='post'),
    path('post_field/', async_to_sync(Everytime.ev_post), name='post_field'),
    path('disconnect/', Everytime.logout, name='logout'), #logout
    #path('search/', async_to_sync(Everytime.ev_search_field), name='search_field'),
    #path('connect', )
]