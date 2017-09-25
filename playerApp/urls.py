
from django.conf.urls import url
from django.contrib import admin
from playerApp.views import get_player, get_other, get_play

urlpatterns = [
    url(r'^get_player/', get_player, name='get_player'),
    url(r'^get_other/', get_other, name='get_other'),
    url(r'^get_play/', get_play, name='get_play'),
]
