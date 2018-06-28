# coding=utf-8

from django.conf.urls import url
from app import index

urlpatterns = [
    url(r'^dudao/$', index.dudao),  # 获取督导资格
    url(r'^weixin/$', index.weixin),
    url(r'^exp/$', index.exp),
    url(r'^answer/$', index.daan),
]

urlpatterns += [

]
