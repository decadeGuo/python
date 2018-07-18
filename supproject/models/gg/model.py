#coding:utf-8
from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()
class Project(models.Model):
    """
    功能说明：项目说明表
    ----------------------------------------
    修改人     修改时间        修改原因
    ----------------------------------------
    张二彬      2016-05-17
    """
    name = models.CharField(u'项目名称', max_length=20)  # 多个项目可以使用同一个科目编号
    subject_id = models.IntegerField(u'科目编号')
    status = models.IntegerField(u'启用状态')  # 0 未启用  1 以启用
    free_num = models.IntegerField(u"免费课时")
    unbind_free_num = models.IntegerField(u'未绑微信的免费课时')
    class Meta:
        db_table = 'yh_project'

class TeacherProject(models.Model):
    """
    功能说明：教师督导科目
    ----------------------------------
    姓名      修改时间        修改内容
    ----------------------------------
    张豪飞     2018-03-02
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher_id = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)  # 督导状态 1：督导此科目  -1：未督导此科目（可能是非督导或者督导未选择此科目）
    trained = models.IntegerField(default=0)  # 0：未培训通过   1：培训通过
    trained_time = models.DateTimeField(null=True)  # 培训通过时间

    class Meta:
        db_table = 'yh_teacher_project'

class YhWeixinBind(models.Model):
    """
    内部用户表
    """
    user_id = models.IntegerField(u'用户id')
    status = models.IntegerField(u'是否启用')  # -1  0  1
    openid = models.CharField(max_length=100)
    add_time = models.IntegerField(default=0)
    class Meta:
        db_table = 'yh_weixin_bind'


class SchoolClass(models.Model):
    """
    功能说明：加盟商学校的班级
    ---------------------------------------
    修改人                    时间
    ---------------------------------------
    张豪飞                    2017－3－5
    """

    name = models.CharField(u"班级名称", max_length=50)
    status = models.IntegerField(u"状态", default=1)  # 1：可用  -1:删除

    class Meta:
        db_table = 'yh_class'
class UserBook(models.Model):
    """
    功能说明：用户购买教材表
    ----------------------------------------
    修改人     修改时间        修改原因
    ----------------------------------------
    张豪飞    2017－03－02
    ==============================================================
    project_last_update：项目教材最后使用时间， 点名更新该字段, 首页获取用户教材，生成个性化作业会根据用户最后使用的教材来生成

    """
    TYPE_CHOICES = (
        (0, u'无'),
        (1, u'预习模式:先学后测'),
        (2, u'复习模式:先测后学')
    )
    STATUS_CHOICES = (
        (-1, u'教材已删除'),
        (0, u'教材过期，不可用'),
        (1, u'可用')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.IntegerField(u"教材ID", default=0)  # 不同科目教材表不同(同一教材不同type算两本不同教材两条记录)
    status = models.IntegerField(u'状态')  # 1：可用(已缴费)  0:不可用(未交费) 2:交费到期  -1 已删除
    project = models.ForeignKey(Project, verbose_name=u"优佳项目ID", on_delete=models.CASCADE)  # 当前教材所属科目（作为教材的属性，非限制字段）
    start_catalog_id = models.IntegerField()
    last_catalog_id = models.IntegerField()
    used_lesson_num = models.IntegerField(default=0)
    class Meta:
        db_table = 'yh_user_book'

class UserBookClass(models.Model):
    """
    功能说明：用户设置的教材和班级
    ----------------------------------------
    修改人     修改时间        修改原因
    ----------------------------------------
    张豪飞    2017－03－02
    ----------------------------------------
    用户-教材-班级  的关系如下（其他字段为班级附带或者教材附带的信息，而非限制。例如project_id表示当前教材的科目,非限制该班级和教材必须是该科目）：
    1. 用户-班级 唯一（一个用户的一个班级同时只能使用一本教材）
    2. 用户-教材 唯一（一个用户的一本教材同时只能用于一个班级）
    或者
    1. 用户-【教材-班级】（唯一）
    """
    TYPE_CHOICES = (
        (0, u'无'),
        (1, u'预习模式:先学后测'),
        (2, u'复习模式:先测后学')
    )
    STATUS_CHOICES = (
        (-1, u'教材已删除'),
        (0, u'教材过期，不可用'),
        (1, u'可用')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.IntegerField(u'用户类型')  # １学生 3教师(教师没有教材)
    cls = models.ForeignKey(SchoolClass, verbose_name=u"班级ID", on_delete=models.CASCADE)  # 班级
    user_book = models.ForeignKey(UserBook, null=True, on_delete=models.CASCADE)
    is_new = models.IntegerField(u"是否是新生", default=1)  # 0 不是 1 是
    temp_class_id = models.IntegerField(u"临时上课班级", default=0)  # 点名更新该字段
    temp_update_time = models.IntegerField(u"临时调班的时间", default=0)

    class Meta:
        db_table = 'yh_user_book_class'
class YhInsideUser(models.Model):
    """
    内部用户表
    """
    user_id = models.IntegerField(u'用户id')
    status = models.IntegerField(u'是否启用')  # 0不启用  1启用

    class Meta:
        db_table = 'yh_inside_user'