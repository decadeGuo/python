# coding:utf-8
import time

from django.db.models import Q
from django.shortcuts import render

from core.common import Struct, fetchall_to_many, get_stu_level, get_stu_current, ajax
from models.gg.model import UserBookClass, SchoolClass, Project, TeacherProject, YhWeixinBind, YhInsideUser, User
from models.siyou.model import UserManage
from supproject.settings import DB_NAME


def index(request):
    """主页"""
    error = request.session.get('log')
    request.session["log"] = ''
    return render(request, 'index.html', context=dict(error=error))


def is_already(username, uid, project_id):
    """判断是否具有督导资格"""
    try:
        sql = "select id from auth_user where username like'%{username}%'".format(username=username)
        user_id = fetchall_to_many('yh_edu', sql, 57, fetch_one=True)[0]
        sql = "select trained FROM employee_role where role_id=202 " \
              "and  employee_id=(select id from employee where user_id={user_id})".format(user_id=user_id)

        res = 1 if fetchall_to_many('yh_edu', sql, 57, fetch_one=True)[0] else 0
        a = TeacherProject.objects.filter(user_id=uid,
                                          project_id=project_id, trained=1).exists()
    except:
        res = a = 0
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
    学生返回：
    data:{
        is_weixin:1,
        pro_info:[
            {   
                p_id:11,
                p_name:llll
                exp:1234,
                level:6,
                honer:学渣,
                book:初中九上,
                cls:{id:1,name:班级}
                current:{c_name:第一节,c_id:1,level:4}
            }
        ]    
    }
    
    """
    vue = request.vue
    uid = request.uid
    p_ids = [int(o.get('p_id')) for o in DB_NAME]
    type = int(request.GET.get('radio','2')) if vue else request.session.get('log')
    username = User.objects.filter(pk=uid).last().username if vue else request.user.username

    if int(type) == 1:
        freeall = Project.objects.filter(pk__in=p_ids).all()
        free = [dict(un=o.unbind_free_num, al=o.free_num,p=o.name) for o in freeall]
        is_weinxin = u'已绑定' if YhWeixinBind.objects.filter(user_id=uid, status=1).exists() else u'未绑定'
        is_daan = 1 if YhInsideUser.objects.filter(user_id=uid, status=1).exists() else 0
        user_book = UserBookClass.objects.filter(user_id=uid, user_book__project_id__in=p_ids)
        cls_ids = [int(o.cls_id) for o in user_book]
        cls_info = SchoolClass.objects.filter(pk__in=cls_ids).values("id", "name")
        pro_info = []
        exp_info = []
        l = [7] # 重复的项目
        pro_info_1 = []
        for o in user_book:
            row = Struct()
            k = next((i for i in cls_info if o.cls_id == int(i.get('id'))),None)
            if not k:
                continue
            row.p_id = o.user_book.project_id
            row.p_name = u'%s(%s)'%(k.get('name'),o.user_book.project.name)
            if o.user_book.project_id not in l:
                pro_info_1.append(row)
            row.user_book_id = o.user_book_id
            row.exp, row.level, row.honer = get_stu_level(uid, row.p_id)
            row.book = u"ID:%s" % o.user_book_id
            row.cls = dict(id=k.get('id'), name=k.get('name'))
            row.current = get_stu_current(uid, row.p_id,row.user_book_id)
            pro_info.append(row)
        for o in user_book:
            if o.user_book.project_id not in l:
                tmp = Struct()
                tmp.p_id = o.user_book.project_id
                tmp.p_name = o.user_book.project.name
                tmp.exp, tmp.level, tmp.honer = get_stu_level(uid, tmp.p_id)
                l.append(o.user_book.project_id)
                exp_info.append(tmp)

        data = dict(
            type=int(type),
            is_weinxin=is_weinxin,
            pro_info=pro_info,
            exp_info=exp_info,
            is_daan=is_daan,
            pro_info_1=pro_info_1,
            free=free
        )
    else:  # 教师信息
        # 改教师名下所有的班级
        cls_ids = UserBookClass.objects.filter(user_id=uid).values_list("cls_id", flat=True)
        cls_info = SchoolClass.objects.filter(pk__in=cls_ids).values("id", "name")
        all_project = Project.objects.filter(id__in=p_ids).values("id", "name").order_by("id")
        pro_info = []
        already_pass = []
        already_info = []
        for o in all_project:
            row = Struct()
            row.project_id = int(o.get('id'))
            row.project_name = o.get('name')
            # 判断是否具有督导资格是是否完成全部培训
            if is_already(username[2:], uid, row.project_id):
                row.status = 1
                already_pass.append(row.project_id)
                already_info.append(row)
            else:
                row.status = 0
            pro_info.append(row)
        all_p_id = [int(o.get('id')) for o in all_project.exclude(id__in=already_pass)]
        need = all_project.filter(id__in=all_p_id)
        data = dict(
            cls_info = [dict(id=o.get('id'),name=o.get('name')) for o in cls_info],
            pro_info=pro_info,
            need=[dict(id=o.get('id'),name=o.get('name')) for o in need],
            already_info=already_info
        ) if vue else dict(
            type=int(type),
            cls_info=cls_info,
            pro_info=pro_info,
            need=need,
            already_info=already_info,
        )
    if vue:
        return ajax(data)
    else:
        return render(request, 'after_login.html', context=data)
