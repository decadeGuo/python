# coding=utf-8

from django.conf.urls import url
from app import index

urlpatterns = [
    url(r'^dudao/$', index.dudao),  # 获取督导资格
    url(r'^weixin/$', index.weixin),
    url(r'^exp/$', index.exp),
    url(r'^answer/$', index.daan),
    url(r'^clear/info/$', index.clear_info),
    url(r'^clear/content/$', index.clear)
]

urlpatterns += [
    url(r'^get/super/$',index.super_update)
]
