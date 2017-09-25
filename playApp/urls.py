
from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.LeaguesView.as_view(), name='Leagus'),
    url(r'^round/(?P<league_num>\d+)/$', views.RoundView.as_view(),name="Round"),
    url(r'^round/(?P<league_num>\d+)/(?P<round_num>\d+)/$', views.RoundView.as_view(),name="RoundII"),
]
