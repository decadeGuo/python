#coding:utf-8
import pymysql
from django.http import HttpResponse
import json

from supproject.settings import CONFIG_INFO


def ajax(data=None,message=''):
    if not data:
        data = {"status":"ok"}
    return HttpResponse(json.dumps(dict(data=data,message=message)))
class Struct(dict):
    """
    - 为字典加上点语法. 例如:
    >>> o = Struct({'a':1})
    >>> o.a
    >>> 1
    >>> o.b
    >>> None
    """

    def __init__(self, dictobj={}):
        self.update(dictobj)

    def __getattr__(self, name):
        # Pickle is trying to get state from your object, and dict doesn't implement it.
        # Your __getattr__ is being called with "__getstate__" to find that magic method,
        # and returning None instead of raising AttributeError as it should.
        if name.startswith('__'):
            raise AttributeError
        return self.get(name)

    def __setattr__(self, name, val):
        self[name] = val

    def __hash__(self):
        return id(self)


def db_base(db_name,type):
    data = CONFIG_INFO
    DB_HOST = data.get('YH_DB%s_HOST'%type)
    DB_USER = data.get('YH_DB%s_USER'%type)
    DB_PORT = int(data.get('YH_DB%s_PORT'%type))
    DB_PASSWORD = data.get('YH_DB%s_PASSWORD'%type)
    return pymysql.connect(host=DB_HOST,
                           user=DB_USER,
                           port=DB_PORT,
                           passwd=DB_PASSWORD,
                           db=db_name,
                           charset="utf8")
def conn_db(db_name,sql,type):
    """更新操作"""
    conn = db_base(db_name,type)
    cxn = conn.cursor()
    cxn.execute(sql)
    conn.commit()
    cxn.close()
    conn.close()
def fetchall_to_many(db_name,sql,type,fetch_one=False,fetch_all=False):
    """查询返回字典对象结果"""
    conn = db_base(db_name, type)
    cxn = conn.cursor()
    cxn.execute(sql)
    if fetch_one:
        object_list = cxn.fetchone()
    elif fetch_all:
        object_list = cxn.fetchall()
    else:
        desc = cxn.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cxn.fetchall()
        ]
    cxn.close()
    conn.close()
    return object_list