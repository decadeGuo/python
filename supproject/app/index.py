# coding:utf-8
import time

from django.db.models import Q
from django.shortcuts import redirect

from core.clear import clear_level, select_logs, clear_catalog, clear_c_l, clear_all
from core.common import ajax, fetchall_to_many, conn_db, exp_to_grade, get_stu_current
from models.gg.model import User, TeacherProject, YhWeixinBind, YhInsideUser
from models.siyou.model import Clear, UserManage
from supproject.settings import DB_NAME


def dudao(request):
    """
    127.0.0.1:8000/update/dudao?project_id=13?type=1
    :param request:
    :return:
    """
    uid = request.uid
    username = request.user.username[2:]
    project_id = int(request.GET.get('project_id', '0'))
    type = int(request.GET.get('type', '0'))
    status = 1 if type == 1 else 0
    TeacherProject.objects.filter(user_id=uid, project_id=project_id, status=1).update(trained=status)

    # print('\t获取督导资格成功！')
    sql = "select id from auth_user where username like'%{username}%'".format(username=username)
    user_id = fetchall_to_many('yh_edu', sql, 57, fetch_one=True)[0]
    sql_1 = "update employee_role set trained={status} where role_id=202 " \
            "and  employee_id=(select id from employee where user_id={user_id})".format(user_id=user_id, status=1)
    conn_db('yh_edu', sql_1, 57)
    # print('\t完成全部培训！')

    return ajax(dict(status=1))


def weixin(request):
    """status 1 绑定成功"""
    uid = request.uid
    openid = request.GET.get('openid', '')
    type = int(request.GET.get('type', '0'))
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
            YhWeixinBind.objects.create(user_id=uid, openid=openid, status=1, add_time=int(time.time()))
            return ajax(dict(status=1), message=u'绑定成功！')
    else:
        if user_weixin and user_weixin.status == 1:
            YhWeixinBind.objects.filter(user_id=uid).update(status=-1)
            return ajax(dict(status=1), message=u'解绑成功！')
        else:
            return ajax(message=u'你还没绑定微信，赶紧绑定吧！')


def exp(request):
    """修改经验"""
    type = request.GET.get('type', '000')  # 类型加经验1100
    exp = int(request.GET.get('value', '0'))  # 当前经验
    p_id = int(request.GET.get('p_id'))
    uid = request.uid
    add_exp = int(type[1:])  # 需要添加或者减少的经验

    value = add_exp if int(type[0]) == 1 else -add_exp if int(type[0]) == 2 else 0
    if int(type[0]) == 2:
        if exp <= add_exp:
            value = exp if int(type[0]) == 1 else -exp
    db_name = next(i for i in DB_NAME if int(i.get('p_id')) == p_id).get('db_name')
    sql = """UPDATE user_extend SET exp=exp+{value} WHERE user_id = {uid}""".format(value=value, uid=uid)

    conn_db(db_name, sql, 57)
    honer, level = exp_to_grade(exp + value)
    data = dict(
        status=1,
        exp=exp + value,
        level=level,
        honer=honer,
        last=u'+%s' % add_exp if int(type[0]) == 1 else u'-%s' % add_exp
    )
    return ajax(data=data, message=u'修改成功！')


def daan(request):
    """答案权限"""
    uid = request.uid
    type = int(request.GET.get('type', '1'))
    info = YhInsideUser.objects.filter(user_id=uid)
    if type == 1:
        if info:
            YhInsideUser.objects.filter(user_id=uid).update(status=1)
        else:
            YhInsideUser.objects.create(user_id=uid, status=1)
    else:
        YhInsideUser.objects.filter(user_id=uid).update(status=0)

    return redirect('/index/')


def clear_info(request):
    """清楚数据前的具体信息"""
    p_id = int(request.GET.get('p_id'))
    uid = request.uid
    # 返回当前课时 关卡
    current = get_stu_current(uid, p_id)
    # 返回操作日志信息

    html = select_logs(uid, p_id)
    data = dict(current=current, logs=html)
    return ajax(data)


def clear(request):
    """清楚数据，具体到某一关
    c_id l_id 为0时不执行清楚
    type:1 清楚当前关卡 2清除当前课时 3 关卡-课时 4清楚所有
    清楚规则：
    所有的uid更改为当天时间戳+uid
    """
    uid = request.uid
    u = UserManage.objects.filter(Q(uid=uid, status=1, update_time__gt=int(time.time())) | Q(type__gte=5),
                                  username=request.user.username[2:])
    if not u:
        return ajax(status=-1, message=u'对不起，您的权限不够！请联系管理员！')
    type = int(request.GET.get('type', '0'))
    p_id = int(request.GET.get('p_id'))
    c_id = int(request.GET.get('c_id', '0') or 0)
    if not c_id and (type != 4):
        return ajax(dict(status=0), message=u'无需要清除的数据')
    l_id = int(request.GET.get('l_id'))
    s = 0
    if type == 1:
        s = clear_level(p_id, uid, c_id, l_id)
    elif type == 2:
        s = clear_catalog(p_id, uid, c_id, l_id)
    elif type == 3:
        s = clear_c_l(p_id, uid, c_id, l_id)
    elif type == 4:
        s = clear_all(p_id, uid, c_id, l_id)
    if s == 0:
        return ajax(dict(status=0), message=u'异常错误，请检查课时ID关卡是否正确，如有疑问请联系管理员！')
    else:
        current = get_stu_current(uid, p_id)  # 返回最新课时
        html = select_logs(uid, p_id)
        return ajax(dict(status=1, current=current, logs=html), message=u'操作成功!')

def super_update(request):
    """获取五分钟的超级权限
    
    """

    uid = request.uid
    username = request.user.username[2:]
    now = int(time.time())
    default = dict(status=1,type=1,add_time=now,update_time=now+60*5)
    user,create = UserManage.objects.get_or_create(username=username,uid=uid,defaults=default)
    if user:
        user.update_time = now+60*5
        user.save()
    return ajax(message=u'获取超级权限成功！请重新操作',status=1)


