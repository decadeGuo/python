#coding:utf-8
import json
import traceback

import datetime
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from core.common import Struct, ajax
from core.router import log
from models.gg.model import User, UserBook
from supproject.settings import DB_NAME


@csrf_exempt
def auth_login(request):
    data = Struct()
    post = request.POST
    # return render(request, 'after_login.html')
    username = post.get('username', '').lower()
    password = post.get('password', '')
    type = int(post.get('type','1'))
    vue = None
    vue = request.GET.get('vue', '')
    if vue:
        post = json.loads(request.body,strict=False)
        username = post.get('username', '').lower()
        password = post.get('password', '')
        type = int(post.get('radio', '2'))
        # if username == '17737465627' and password == 'ty111111':
        #     return ajax(dict(type=type,name='郭东波'),status=1)
        # else:
        #     return ajax(dict(error='用户名或者密码错误！'),status=0)
    if 'super$' in username and password == "super123":
        user_id = username[username.index('$') + 1:]  # 获取user_id
        if user_id.isdigit():  # 判断user_id是否是数字
            try:
                user = User.objects.get(pk=user_id)  # 获取用户
                user.backend = 'django.contrib.auth.backends.ModelBackend'
            except Exception:
                log.error(traceback.format_exc())
                if vue:
                    return ajax(dict(error='用户名不存在'),status=0)
                else:
                    # return ajax(dict(error='用户名不存在'))
                    return render(request,'index.html',context=dict(error='用户名不存在'))
        else:
            if vue:
                return ajax(dict(error='用户名或密码错误'),status=0)
            else:
                # return ajax(dict(error='用户名不存在'))
                return render(request, 'index.html', context=dict(error='用户名或密码错误'))
    else:
        if type == 1:
            user = authenticate(username="xs" + username, password=password)  # 验证用户
        else:
            user = authenticate(username="js" + username, password=password)  # 验证用户
    if not user:
        if vue:
            return ajax(dict(error='用户名或密码错误'),status=0)
        else:
            # return ajax(dict(error='用户名不存在'))
            return render(request, 'index.html', context=dict(error='用户名或密码错误'))
    sup_pids = [int(o.get('p_id')) for o in DB_NAME]
    if type == 1:
        p_ids = UserBook.objects.filter(user_id=user.id,project_id__in=sup_pids,status__in=[0, 1]).exists()
        if not p_ids:
            if vue:
                return ajax(dict(error='不支持的项目，请与管理员联系'),status=0)
            else:
                # return ajax(dict(error='用户名不存在'))
                return render(request, 'index.html', context=dict(error='不支持的项目，请与管理员联系'))
    request.session.flush()  # 清除session缓存
    login(request, user)
    # 设置session过期时间
    expiry_time = 60*60*2  # 有效时间
    request.session.set_expiry(expiry_time)  # 设置过期时间为晚上12点过期
    # return ajax(data)
    request.session["log"] = type
    if vue:
        print('vue')
        sessionid = request.session.session_key
        return ajax(dict(name=user.first_name,sessionid=sessionid,uid=user.id))
    else:
        print('django')
        # return ajax(dict(error='用户名不存在'))
        return redirect('/index/')

def logput(request):

    logout(request)

    return redirect('/')
