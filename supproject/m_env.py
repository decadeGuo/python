# coding:utf-8

import json

# temp = {
#     "DB_YEWU_HOST": "rm-2zerx47rp7dil1wyyco.mysql.rds.aliyuncs.com",
#     "DB_YEWU_PASSWORD": "BuM6XpFMxpDdUNCk",
#     "DB_YEWU_PORT": "3306",
#     "DB_YEWU_USER": "dev",
#     "DB_APP_HOST": "rm-2zerx47rp7dil1wyyco.mysql.rds.aliyuncs.com",
#     "DB_APP_PASSWORD": "BuM6XpFMxpDdUNCk",
#     "DB_APP_PORT": "3306",
#     "DB_APP_USER": "dev"
# }

temp = {
    "YH_DB57_HOST": "rm-2zerx47rp7dil1wyyco.mysql.rds.aliyuncs.com",
    "YH_DB57_PASSWORD": "BuM6XpFMxpDdUNCk",
    "YH_DB57_PORT": "3306",
    "YH_DB57_USER": "dev",
    "YH_DB56_HOST": "rm-2zerx47rp7dil1wyyco.mysql.rds.aliyuncs.com",
    "YH_DB56_PASSWORD": "BuM6XpFMxpDdUNCk",
    "YH_DB56_PORT": "3306",
    "YH_DB56_USER": "dev"
}
# temp = {
#     "YH_DB57_HOST": "192.168.6.134",
#     "YH_DB57_PASSWORD": "123456",
#     "YH_DB57_PORT": "3307",
#     "YH_DB57_USER": "root",
#     "YH_DB56_HOST": "192.168.6.134",
#     "YH_DB56_PASSWORD": "123456",
#     "YH_DB56_PORT": "3306",
#     "YH_DB56_USER": "root"
# }
fileObject = open('.env', 'w')
fileObject.write(json.dumps(temp))
fileObject.close()
