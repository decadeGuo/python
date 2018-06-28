#coding:utf-8
import time

from django.shortcuts import redirect

from core.common import ajax, fetchall_to_many, conn_db, exp_to_grade
from models.gg.model import User, TeacherProject, YhWeixinBind, YhInsideUser
from models.siyou.model import Clear
from supproject.settings import DB_NAME


def dudao(request):
    """
    127.0.0.1:8000/update/dudao?project_id=13?type=1
    :param request:
    :return:
    """
    uid = request.uid
    username = request.user.username[2:]
    project_id = int(request.GET.get('project_id','0'))
    type = int(request.GET.get('type','0'))
    status = 1 if type == 1 else 0
    TeacherProject.objects.filter(user_id=uid,project_id=project_id,status=1).update(trained=status)

    # print('\t获取督导资格成功！')
    sql = "select id from auth_user where username like'%{username}%'".format(username=username)
    user_id = fetchall_to_many('yh_edu', sql, 57, fetch_one=True)[0]
    sql_1 = "update employee_role set trained={status} where role_id=202 " \
            "and  employee_id=(select id from employee where user_id={user_id})".format(user_id=user_id,status=1)
    conn_db('yh_edu', sql_1, 57)
    # print('\t完成全部培训！')

    return ajax(dict(status=1))

def weixin(request):
    """status 1 绑定成功"""
    uid = request.uid
    openid = request.GET.get('openid','')
    type = int(request.GET.get('type','0'))
    user_weixin = YhWeixinBind.objects.filter(user_id=uid).last()
    if not openid and not user_weixin:
        return ajax(message=u'openid不能为空哦！')
    if type == 2:
        if user_weixin and user_weixin.status == 1:
            return ajax(message=u'你已绑定过微信')
        elif user_weixin:
            YhWeixinBind.objects.filter(user_id=uid).update(status=1)
            return ajax(dict(status=1), message=u'绑定成功！')
        else:
            YhWeixinBind.objects.create(user_id=uid,openid=openid,status=1,add_time=int(time.time()))
            return ajax(dict(status=1),message=u'绑定成功！')
    else:
        if user_weixin and user_weixin.status == 1:
            YhWeixinBind.objects.filter(user_id=uid).update(status=-1)
            return ajax(dict(status=1), message=u'解绑成功！')
        else:
            return ajax(message=u'你还没绑定微信，赶紧绑定吧！')

def exp(request):
    """修改经验"""
    type = request.GET.get('type','000')    # 类型加经验1100
    exp = int(request.GET.get('value','0'))   # 当前经验
    p_id = int(request.GET.get('p_id'))
    uid = request.uid
    add_exp = int(type[1:]) # 需要添加或者减少的经验

    value = add_exp if int(type[0]) == 1 else -add_exp if int(type[0]) == 2 else 0
    if int(type[0]) == 2:
        if exp <= add_exp:
            value = exp if int(type[0]) == 1 else -exp
    db_name = next(i for i in DB_NAME if int(i.get('p_id')) == p_id).get('db_name')
    sql = """UPDATE user_extend SET exp=exp+{value} WHERE user_id = {uid}""".format(value=value,uid=uid)

    conn_db(db_name,sql,57)
    honer,level = exp_to_grade(exp+value)
    data = dict(
        status=1,
        exp = exp+value,
        level=level,
        honer = honer,
        last = u'+%s'%add_exp if int(type[0]) == 1 else u'-%s'%add_exp
    )
    return ajax(data=data,message=u'修改成功！')

def daan(request):
    """答案权限"""
    uid = request.uid
    type = int(request.GET.get('type','1'))
    info = YhInsideUser.objects.filter(user_id=uid)
    if type == 1:
        if info:
            YhInsideUser.objects.filter(user_id=uid).update(status=1)
        else:
            YhInsideUser.objects.create(user_id=uid,status=1)
    else:
        YhInsideUser.objects.filter(user_id=uid).update(status=0)

    return redirect('/index/')
def clear(request):
    """清楚数据，具体到某一关"""



