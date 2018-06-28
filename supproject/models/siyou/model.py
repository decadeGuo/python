#coding:utf-8


from django.db import models
class Clear(models.Model):
    c_id = models.IntegerField(default=0)
    l_id = models.IntegerField(default=0)
    explain = models.CharField(max_length=200)
    add_time = models.IntegerField(default=0)
    class Meta:
        db_table = 'yh_clear'
