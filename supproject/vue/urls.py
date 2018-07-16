# coding=utf-8

from django.conf.urls import url
from vue.view import get_info

urlpatterns = [
    url(r'^index/$', get_info),  # 首页
]
