# coding:utf-8

import json

# temp = {
#     "YH_DB57_HOST": "rm-2zeot1p1x23628hg9o.mysql.rds.aliyuncs.com",
#     "YH_DB57_PASSWORD": "BuM6XpFMxpDdUNCk",
#     "YH_DB57_PORT": "3306",
#     "YH_DB57_USER": "dev",
#     "YH_DB56_HOST": "rm-2ze372665tb1j1x9oo.mysql.rds.aliyuncs.com",
#     "YH_DB56_PASSWORD": "BuM6XpFMxpDdUNCk",
#     "YH_DB56_PORT": "3306",
#     "YH_DB56_USER": "dev",
# }

temp = {
    "YH_DB57_HOST": "192.168.6.134",
    "YH_DB57_PASSWORD": "123456",
    "YH_DB57_PORT": "3307",
    "YH_DB57_USER": "root",
    "YH_DB56_HOST": "192.168.6.134",
    "YH_DB56_PASSWORD": "123456",
    "YH_DB56_PORT": "3306",
    "YH_DB56_USER": "root"
}
fileObject = open('.env', 'w')
fileObject.write(json.dumps(temp))
fileObject.close()
