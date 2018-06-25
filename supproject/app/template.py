# coding:utf-8
from django.shortcuts import render

from core.common import Struct, fetchall_to_many
from models.gg.model import UserBookClass, SchoolClass, Project, TeacherProject


def index(request):
    """主页"""
    error = request.session.get('log')
    request.session["log"] = ''
    return render(request, 'index.html',context=dict(error=error))

def is_already(username,uid,project_id):
    """判断是否具有督导资格"""
    try:
        sql = "select id from auth_user where username like'%{username}%'".format(username=username)
        user_id = fetchall_to_many('yh_edu', sql, 57, fetch_one=True)[0]
        sql = "select trained FROM employee_role where role_id=202 " \
              "and  employee_id=(select id from employee where user_id={user_id})".format(user_id=user_id)

        res = 1 if fetchall_to_many('yh_edu', sql, 57, fetch_one=True)[0] else 0
        a = TeacherProject.objects.filter(user_id=uid,
                                  project_id=project_id,trained=1).exists()
    except:
        res=a = 0
    return True if res and a else False


def after_login(request):
    """登录后首页"""
    """
    教师返回
    data:{
        cls_info:[
            {
                cls_id:11
                cls_name:'班级名字'            
            }        
        ],
        pro_info:[
            {
                project_name:项目名字，
                status：是否具有督导资格
            }
        ],
        need:[
            需要获取督导资格的科目
        ],
        already_pass:[已完成的]
    }
    
    """
    type = request.session.get('log')

    if int(type) == 1:
        pass

    else:  # 教师信息
        uid = request.uid
        # 改教师名下所有的班级
        cls_ids = UserBookClass.objects.filter(user_id=uid, user_type=type).values_list("cls_id", flat=True)
        cls_info = SchoolClass.objects.filter(pk__in=cls_ids).values("id", "name")
        all_project = Project.objects.filter(id__gte=11).values("id", "name").order_by("id")
        pro_info = []
        already_pass = []
        already_info = []
        for o in all_project:
            row = Struct()
            row.project_id = int(o.get('id'))
            row.project_name = o.get('name')
            # 判断是否具有督导资格是是否完成全部培训

            if is_already(request.user.username[2:],uid,row.project_id):
                row.status = 1
                already_pass.append(row.project_id)
                already_info.append(row)
            else:
                row.status = 0
            pro_info.append(row)
        all_p_id = [int(o.get('id')) for o in all_project.exclude(id__in=already_pass)]
        need = all_project.filter(id__in=all_p_id)
        data = dict(
            type=int(type),
            cls_info = cls_info,
            pro_info = pro_info,
            need=need,
            already_info=already_info
        )

    return render(request, 'after_login.html', context=data)
