#coding:utf-8
import time

from core.common import ajax, fetchall_to_many, conn_db
from models.gg.model import User, TeacherProject, YhWeixinBind


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
    TeacherProject.objects.filter(user_id=uid,project_id=project_id).update(trained=status)

    # print('\t获取督导资格成功！')
    sql = "select id from auth_user where username like'%{username}%'".format(username=username)
    user_id = fetchall_to_many('yh_edu', sql, 57, fetch_one=True)[0]
    sql_1 = "update employee_role set trained={status} where role_id=202 " \
            "and  employee_id=(select id from employee where user_id={user_id})".format(user_id=user_id,status=1)
    conn_db('yh_edu', sql_1, 57)
    # print('\t完成全部培训！')

    return ajax(dict(status=1))

def weixin(request):
    uid = request.uid
    openid = request.GET.get('openid')
    if YhWeixinBind.objects.filter(user_id=uid).exists():
        return ajax(message='你已绑定过微信')
    YhWeixinBind.objects.create(user_id=uid,openid=openid,status=1,add_time=int(time.time()))
    return ajax(dict(status=1))

