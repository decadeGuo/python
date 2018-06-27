"""supproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app import login, template
# import settings
# from settings import MEDIA_SITE
# from django.conf import settings
from django.views.static import serve

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', template.index),
    url(r'^update/', include('app.urls')),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': MEDIA_SITE}),
]

urlpatterns += [
    url(r'^login/$', login.auth_login),
    url(r'^logout/$', login.logput),
]
urlpatterns += [
    url(r'index/$', template.after_login)
]
