# coding=utf-8

from django.conf.urls import url
# import index
from app import index

urlpatterns = [
    url(r'^dudao/$', index.dudao),  # 获取督导资格
    url(r'^weixin/$', index.weixin)
]

urlpatterns += [

]
