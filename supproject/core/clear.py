# coding:utf-8
import pymysql
from django.http import HttpResponse
import json
import time
from core.common import fetchall_to_many, conn_db, get_db_name
from models.siyou.model import Clear
from supproject.settings import CONFIG_INFO, DB_NAME

n = 1000000
def get_test(p_id, uid, cid, lid):
    db_name = get_db_name(p_id)

    sql = """SELECT id,level_status,s_json_data,clear_time FROM test WHERE user_id={uid} AND catalog_id={cid} AND level_id={lid}""".format(
        uid=uid, cid=cid, lid=lid)
    return fetchall_to_many(db_name, sql, 57)[0]


def select_logs(uid, pid):
    """获取操作日志"""
    logs = Clear.objects.filter(uid=uid, p_id=pid).order_by("-id").values_list("explain", flat=True)
    html = '<br>'.join(logs)
    return html

def get_level_sql(tid,lid,iscurrent=True):
    sql_1 = """UPDATE knowledge_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id}""".format(n=n,id=tid)
    sql_2 = """UPDATE method_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id}""".format(n=n,id=tid)
    sql_3 = """UPDATE example_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id}""".format(n=n,id=tid)
    sql_4 = """UPDATE apply_test SET id=id+{n},test_id=test_id+{n} WHERE test_id={id} AND level_id={lid}""".format(
        n=n,id=tid,lid=lid
    )
    if iscurrent:
        return sql_1 if lid == 1 else sql_2 if lid == 2 else sql_3 if lid == 3 else sql_4


def clear_level(p_id, uid, cid, lid):
    """
    清除当前关卡--逻辑说明：
    更改test表中level_id字段，update_time字段，position 删除该关卡对应的具体详情表中的数据
    """
    db_name = get_db_name(p_id)
    info = get_test(p_id, uid, cid, lid)
    if not info:
        return 0
    id = int(info.get('id'))
    l_id = lid - 1 if lid > 1 else 1
    level_status = 0 if int(info.get('level_status')) == 1 else 0
    clear_time = 0 if level_status == 0 else info.get('clear_time')
    update_time = int(time.time())
    data = json.loads(info.get('s_json_data'))
    n_lid = [l for l in range(lid, lid + 10) if 'lv_%s' % l in data.keys()]
    for o in n_lid:
        del data['lv_%s' % o]
    try:
        # 更新test表中字段
        sql_1 = """UPDATE test SET level_id={lid},level_status={status},position=0,
                    update_time={now},clear_time={clear_time},s_json_data='{data}' WHERE id={id}""".format(
            lid=l_id, status=level_status, now=update_time, id=id, clear_time=clear_time,data=str(json.dumps(data))
        )
        conn_db(db_name, sql_1, 57)
        sql_2 = get_level_sql(id,lid)
        conn_db(db_name, sql_2, 57)

        time1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(update_time))
        main = u'您于%s清除了%s课时%s关的数据' % (time1, cid, lid)
        Clear.objects.create(uid=uid, p_id=p_id, c_id=cid, l_id=lid, explain=main, add_time=update_time)
        return 1
    except:
        return 0

def clear_catalog(p_id, uid, cid, lid):
    """"""
    db_name = get_db_name(p_id)
    info = get_test(p_id, uid, cid, lid)
    if not info:
        return 0
    id = int(info.get('id'))


    # 更新test表中字段
    sql_1 = """UPDATE test SET user_id=user_id+{n},user_book_id=user_book_id+{n},id=id+{n} WHERE id={id}""".format(
         id=id,n=n
    )
    conn_db(db_name, sql_1, 57)
    # 更新关卡关联的所有关卡记录
    try:
        sql_2 = """UPDATE knowledge_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id}; 
                  UPDATE method_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id};
                  UPDATE example_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id};
                  UPDATE apply_test SET id=id+{n},test_id=test_id+{n} WHERE test_id={id};
            """.format(id=id,n=n)
        conn_db(db_name, sql_2, 57,many=True)
    except:
        pass
    now = int(time.time())
    time1 = time.strftime('%m/%d %H:%M:%S', time.localtime(now))
    main = u'您于%s清除了%s课时全部的数据' % (time1, cid)
    Clear.objects.create(uid=uid, p_id=p_id, c_id=cid, l_id=lid, explain=main, add_time=now)
    return 1


def clear_c_l(p_id, uid, c_id, l_id):
    """课时--关卡"""
def clear_all(p_id, uid, c_id, l_id):
    """"""



