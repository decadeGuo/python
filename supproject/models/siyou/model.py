#coding:utf-8


from django.db import models
class Clear(models.Model):
    uid = models.IntegerField(default=0)
    p_id = models.IntegerField(default=0)
    c_id = models.IntegerField(default=0)
    l_id = models.IntegerField(default=0)
    explain = models.CharField(max_length=200)
    add_time = models.IntegerField(default=0)
    type = models.IntegerField(default=0) # 0 清空数据 1 答案权限 2督导资格 3微信
    class Meta:
        db_table = 'yh_clear'

class UserManage(models.Model):
    uid = models.IntegerField(default=0)
    username = models.CharField(max_length=100)
    type = models.IntegerField(default=0)
    add_time = models.IntegerField(default=0)
    update_time = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    class Meta:
        db_table='yh_user_manage'
class QuickLogin(models.Model):
    """快速登录表"""
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    status = models.IntegerField(default=1)
    type = models.IntegerField(default=0)
    remark = models.CharField(max_length=1000)
    name = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    class Meta:
        db_table='quick_login'
class LiuYan(models.Model):
    uid = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    content = models.CharField(max_length=300)
    add_time = models.IntegerField(default=0)

    class Meta:
        db_table='liuyan'
class Game(models.Model):
    """游戏记录"""
    type = models.IntegerField(default=0) # 1 火眼金睛
    uid = models.IntegerField(default=0)
    time = models.IntegerField(default=0) # 游戏用时
    dw = models.CharField(max_length=500)
    add_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='game'

