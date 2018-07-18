# coding=utf-8

from django.conf.urls import url
from vue.view import get_info,liuyan,game_res,game

urlpatterns = [
    url(r'^index/$', get_info),  # 首页
    url(r'^liuyan/$', liuyan),  # 首页
url(r'^game/$', game),  # 首页
url(r'^game/res/$', game_res),  # 首页

]
