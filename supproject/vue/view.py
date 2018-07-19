# coding:utf-8
import json
import random

from django.views.decorators.csrf import csrf_exempt

from core.common import ajax
from models.gg.model import YhWeixinBind, YhInsideUser, User
from models.siyou.model import Clear, LiuYan, Game
import time

def get_info(request):
    """"""
    uid = request.uid
    logs = Clear.objects.filter(uid=uid).order_by("-id").values_list("explain", flat=True)
    logs = [o for o in logs]
    ly = LiuYan.objects.filter().all().order_by("-id")
    liuyan = [dict(name=o.name,content=o.content,time = time.strftime('%m/%d %H:%M:%S', time.localtime(o.add_time))) for o in ly]

    return ajax(dict(logs=logs,liuyan=liuyan))
@csrf_exempt
def liuyan(request):
    """"""
    uid = request.uid
    username = User.objects.filter(pk=uid).last().first_name
    print username,'mmmmmmm'
    type = int(request.GET.get('radio','1'))
    content = json.loads(request.body).get('text')
    name = u'%s(%s)'%(username , u'学生' if type == 1 else u'老师')
    now = int(time.time())
    LiuYan.objects.create(uid=uid,name=name,content=content,add_time=now)
    return ajax()
def get_game_log(uid):
    res = Game.objects.filter(uid=uid, type=1).last()
    jilu = json.loads(res.dw) if res else []

    return jilu
def game(request):
    """"""
    ziyuan = [(u'赢', u'羸'), (u'未', u'末'), (u'暧', u'暖'), (u'肓', u'盲'), (u'夭', u'天')]
    level = {"1":28,"2":104,"3":252,"4":442,"5":640}
    l = request.GET.get('l','1')   # 挑战等级　传入默认一级
    try:
        n = level[l]
    except:
        n = level["5"]
    obj = random.choice(ziyuan) # 干扰项
    grx = list(obj[0] * n)
    right = obj[-1] # 正确答案
    m = random.randint(1, n)
    grx[m - 1] = right
    num = grx.index(right)  # 正确答案的位置

    jilu = get_game_log(request.uid)

    return ajax(dict(c=grx,n=num,al=n,l=int(l)+1,jilu=jilu))

def game_res(request):
    """"""
    dw = {"1": "☆最强王者☆", "2": "☆超凡大师☆",
          "3": "☆璀璨砖石☆", "4": "☆华贵铂金☆", "5": "●荣耀黄金●", "6": "●不屈白银●", "7": "英勇黄铜", "8": "垃圾塑料"}

    time = int(request.GET.get('time','100'))  # 时间
    l = int(request.GET.get('l','1'))
    if time <= 1:
        score = dw["1"]
    elif time <= 3:
        score = dw["2"]
    elif time <= 7:
        score = dw["3"]
    elif time <= 12:
        score = dw["4"]
    elif time <= 18:
        score = dw["5"]
    elif time <= 30:
        score = dw["6"]
    elif time <= 50:
        score = dw["7"]
    else:
        score = dw["8"]
    current = {"lv":"lv%s"%l,"dw":score,"time":time}
    res = Game.objects.filter(uid=request.uid, type=1).last()
    if not res:
        res = Game.objects.create(uid=request.uid,type=1,time=0,dw=json.dumps([]))
    data = json.loads(res.dw)
    cur = next((k for k in data if k.get('lv') == "lv%s"%l),None)
    if cur:
        if int(cur["time"] > time):
            cur["time"] = time
            cur["dw"] = score
    else:
        data.append(current)
    Game.objects.filter(uid=request.uid, type=1).update(dw=json.dumps(data))

    jilu = get_game_log(request.uid)
    return ajax(dict(score=score,time=time,jilu=jilu))


