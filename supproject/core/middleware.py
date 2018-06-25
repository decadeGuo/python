#coding:utf-8
import traceback
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.utils import timezone

from django.utils.deprecation import MiddlewareMixin

from core.common import ajax
from core.router import log
nologin_urls = ["/","/logout/","/login/"]

class AuthenticationMiddleware(MiddlewareMixin):
    """"""


    def process_response(self, request, response):
        try:
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
            response["Access-Control-Max-Age"] = "1728000"
        except Exception as e:
            log.error("process_response1:%s" % e)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        """
        # if not settings.DEBUG:
        #     return None

        path = str(request.path)
        # 如果请求的路径为 js css 文件 不处理
        if path.startswith('/static/'):
            pass
        elif path in nologin_urls:
            pass
        else:
            # pass
            user = request.user
            uid = user.id if user else 0
            # session_key = ""
            # if request.GET.get("sessionid"):
            #     session_key = request.GET.get("sessionid")
            # if not session_key:
            #     print('走到这里了')
            #     print(request.META)
            #     if request.META.get("HTTP_SESSIONID"):
            #
            #         session_key = request.META.get("HTTP_SESSIONID")
            #         print(session_key)
            # if session_key:
            #     try:
            #         s = Session.objects.get(pk=session_key, expire_date__gt=timezone.now())
            #         uid = s.get_decoded().get('_auth_user_id')
            #     except:
            #         log.error(traceback.format_exc())
            # else:
            #     uid = request.GET.get("uid") or 0
            request.uid = uid
            if not uid:
                request.session["log"] = u'会话过期重新登录'
                return redirect('/')
        return None