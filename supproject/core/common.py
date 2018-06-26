# coding:utf-8
import pymysql
from django.http import HttpResponse
import json

from supproject.settings import CONFIG_INFO, DB_NAME


def ajax(data=None, message=''):
    if not data:
        data = {"status": "ok"}
    return HttpResponse(json.dumps(dict(data=data, message=message)),content_type=json)


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


def db_base(db_name, type):
    data = CONFIG_INFO
    DB_HOST = data.get('YH_DB%s_HOST' % type)
    DB_USER = data.get('YH_DB%s_USER' % type)
    DB_PORT = int(data.get('YH_DB%s_PORT' % type))
    DB_PASSWORD = data.get('YH_DB%s_PASSWORD' % type)
    return pymysql.connect(host=DB_HOST,
                           user=DB_USER,
                           port=DB_PORT,
                           passwd=DB_PASSWORD,
                           db=db_name,
                           charset="utf8")


def conn_db(db_name, sql, type):
    """更新操作"""
    conn = db_base(db_name, type)
    cxn = conn.cursor()
    cxn.execute(sql)
    conn.commit()
    cxn.close()
    conn.close()


def fetchall_to_many(db_name, sql, type, fetch_one=False, fetch_all=False):
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


def get_stu_level(user_id, p_id):
    """获取学生的等级经验"""
    db_name = next(i for i in DB_NAME if int(i.get('p_id')) == p_id).get('db_name')
    sql = """SELECT exp FROM `user_extend` WHERE user_id = {user_id};""".format(user_id=user_id)
    exp = fetchall_to_many(db_name, sql, 57, fetch_one=True)[0]
    honer, level = exp_to_grade(exp)
    return exp, level, honer


def get_stu_current(user_id, p_id):
    """获取学生当前课时"""
    db_name = next(i for i in DB_NAME if int(i.get('p_id')) == p_id).get('db_name')
    sql = """SELECT t.catalog_id,t.level_id FROM test t JOIN user_current_catalog p 
              ON t.user_book_id = p.user_book_id AND p.catalog_id = t.catalog_id WHERE p.user_id={user_id};""".format(user_id=user_id)
    res = fetchall_to_many(db_name,sql,57,fetch_one=True)

    catalog_id = res[0]
    level_id = res[-1]

    return dict(c_id=catalog_id,level=level_id,c_name=u'ID')

def exp_to_grade(exp):
    """获取等级名称和等级
    Returns grade:(称号,等级)
    """
    if exp <= 50:
        honer_level, level = u'学水', 1
    elif exp <= 100:
        honer_level, level = u'学沫', 2
    elif exp <= 200:
        honer_level, level = u'学残', 3
    elif exp <= 300:
        honer_level, level = u'学灰', 4
    elif exp <= 1000:
        honer_level, level = u'学弱', 5
    elif exp <= 2500:
        honer_level, level = u'学民', 6
    elif exp <= 4500:
        honer_level, level = u'学糕', 7
    elif exp <= 7000:
        honer_level, level = u'学神', 8
    elif exp <= 10000:
        honer_level, level = u'学霸', 9
    else:
        honer_level, level = u'学魔', 10
    return honer_level, level
