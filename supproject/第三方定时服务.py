#coding:utf-8
import time
import os
import re
log = [1,2,3,4,5,6,7,8,9]

def c():
    o = os.listdir(os.path.dirname(os.path.abspath(__file__)))
    names = [o for o in o if o[-3:] == 'txt']
    names.sort()
    l = int(names[-1][-5]) if names else 0
    print(names)
    def c_c(names,l):
        name = 'q_%s.txt' % l
        print(l)
        if name in names:
            l = next(i for i in log if i==l+1)
            name = 'q_%s.txt' % l
        p = open(name,'w')
        p.close()
        print(name,l,'我执行了,执行时间:%s'%int(time.time()))
    c_c(names,l)
c()
import schedule
# schedule.every().days.at("15:31").do(c)
schedule.every(5).seconds.do(c)
while True:
    schedule.run_pending()
# name = 'q_0.txt'
# l=0
# if os.path.exists(name):
#     name = next(i for i in log if i==l+1)
#     p = open(name,'w')
#     p.close()