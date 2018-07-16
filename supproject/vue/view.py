# coding:utf-8
from models.gg.model import YhWeixinBind, YhInsideUser


def get_info(request):
    """"""
    uid = request.uid
    is_weinxin = 1 if YhWeixinBind.objects.filter(user_id=uid, status=1).exists() else 0
    is_daan = 1 if YhInsideUser.objects.filter(user_id=uid, status=1).exists() else 0
