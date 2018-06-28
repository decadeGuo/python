#coding:utf-8


from django.db import models
class Clear(models.Model):
    uid = models.IntegerField(default=0)
    p_id = models.IntegerField(default=0)
    c_id = models.IntegerField(default=0)
    l_id = models.IntegerField(default=0)
    explain = models.CharField(max_length=200)
    add_time = models.IntegerField(default=0)
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
