# coding:utf-8
import pymysql
from django.http import HttpResponse
import json
import time
from core.common import fetchall_to_many, conn_db, get_db_name
from models.gg.model import UserBook
from models.siyou.model import Clear
from supproject.settings import CONFIG_INFO, DB_NAME

n = 1000000


def get_test(p_id, uid, user_book_id):
    db_name = get_db_name(p_id)

    sql = """SELECT id,level_status,s_json_data,clear_time FROM test WHERE user_id={uid} AND user_book_id={cid}""".format(
        uid=uid, cid=user_book_id)
    res = fetchall_to_many(db_name, sql, 57)
    return res[0] if res else 0


def select_logs(uid, pid):
    """获取操作日志"""
    logs = Clear.objects.filter(uid=uid, p_id=pid).order_by("-id").values_list("explain", flat=True)
    html = '<br>'.join(logs)
    return html


def get_level_sql(tid, lid, iscurrent=True):
    """清楚模板  数理化预科的数据结构"""
    sql_1 = """UPDATE knowledge_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id};""".format(n=n, id=tid)
    sql_2 = """UPDATE method_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id};""".format(n=n, id=tid)
    sql_3 = """UPDATE example_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id};""".format(n=n, id=tid)
    sql_4 = """UPDATE apply_test SET id=id+{n},test_id=test_id+{n} WHERE test_id={id} AND level_id={lid};""".format(
        n=n, id=tid, lid=lid
    )
    if iscurrent:
        return sql_1 if lid == 1 else sql_2 if lid == 2 else sql_3 if lid == 3 else sql_4
    else:
        sql_4 = """UPDATE apply_test SET id=id+{n},test_id=test_id+{n} WHERE test_id={id} AND level_id>={lid};""".format(
            n=n, id=tid, lid=lid)
        if lid == 1:
            return sql_1 + sql_2 + sql_3 + sql_4
        elif lid == 2:
            return sql_2 + sql_3 + sql_4
        elif lid == 3:
            return sql_3 + sql_4
        else:
            return sql_4


def clear_level(p_id, uid, cid, lid,user_book_id):
    """
    清除当前关卡--逻辑说明：
    更改test表中level_id字段，update_time字段，position 删除该关卡对应的具体详情表中的数据
    """
    db_name = get_db_name(p_id)
    info = get_test(p_id, uid, user_book_id)

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
            lid=l_id, status=level_status, now=update_time, id=id, clear_time=clear_time, data=str(json.dumps(data))
        )
        conn_db(db_name, sql_1, 57)
        sql_2 = get_level_sql(id, lid)
        conn_db(db_name, sql_2, 57)

        time1 = time.strftime('%m/%d %H:%M:%S', time.localtime(update_time))
        main = u'您于%s清除了%s课时%s关的数据--1' % (time1, cid, lid)
        Clear.objects.create(uid=uid, p_id=p_id, c_id=cid, l_id=lid, explain=main, add_time=update_time)
        return 1
    except:
        return 0


def clear_catalog(p_id, uid, cid, lid,user_book_id):
    """"""
    db_name = get_db_name(p_id)
    info = get_test(p_id, uid,user_book_id)
    if not info:
        return 0
    id = int(info.get('id'))

    # 更新test表中字段
    sql_1 = """UPDATE test SET user_id=user_id+{n},user_book_id=user_book_id+{n},id=id+{n} WHERE id={id} AND user_book_id={user_book_id}""".format(
        id=id, n=n,user_book_id=user_book_id
    )
    conn_db(db_name, sql_1, 57)
    # 更新关卡关联的所有关卡记录
    try:
        sql_2 = """UPDATE knowledge_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id}; 
                  UPDATE method_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id};
                  UPDATE example_study SET id=id+{n},test_id=test_id+{n} WHERE test_id={id};
                  UPDATE apply_test SET id=id+{n},test_id=test_id+{n} WHERE test_id={id};
            """.format(id=id, n=n)
        conn_db(db_name, sql_2, 57, many=True)
    except:
        pass
    now = int(time.time())
    time1 = time.strftime('%m/%d %H:%M:%S', time.localtime(now))
    main = u'您于%s清除了%s课时全部的数据--2' % (time1, cid)
    Clear.objects.create(uid=uid, p_id=p_id, c_id=cid, l_id=lid, explain=main, add_time=now)
    return 1


def clear_c_l(p_id, uid, c_id, lid,user_book_id):
    """课时--关卡"""
    db_name = get_db_name(p_id)
    info = get_test(p_id, uid,user_book_id)
    if not info:
        return 0
    id = int(info.get('id'))

    level_status = 0 if int(info.get('level_status')) == 1 else 0
    clear_time = 0 if level_status == 0 else info.get('clear_time')
    update_time = int(time.time())
    data = json.loads(info.get('s_json_data'))
    n_lid = [l for l in range(lid, lid + 10) if 'lv_%s' % l in data.keys()]
    for o in n_lid:
        del data['lv_%s' % o]
    l_id = lid - 1 if lid > 1 else 1
    try:
        # 更新test表中字段
        sql_1 = """UPDATE test SET level_id={lid},level_status={status},position=0,
                        update_time={now},clear_time={clear_time},s_json_data='{data}' WHERE id={id}""".format(
            lid=l_id, status=level_status, now=update_time, id=id, clear_time=clear_time, data=str(json.dumps(data))
        )
        conn_db(db_name, sql_1, 57)
        sql_2 = get_level_sql(id, lid, iscurrent=False)
        conn_db(db_name, sql_2, 57, many=True)
        time1 = time.strftime('%m/%d %H:%M:%S', time.localtime(update_time))
        main = u'您于%s清除了%s课时%s关的数据--3' % (time1, c_id, lid)
        Clear.objects.create(uid=uid, p_id=p_id, c_id=c_id, l_id=lid, explain=main, add_time=update_time)
        return 1
    except:
        return 0


def clear_all(p_id, uid, c_id, l_id,user_book_id):
    """
    清除所有数据
    优先清除外键数据 最后清理test数据   只清除逻辑数据
    1 analysis analysis_statistics personalise personalise_status  先2后1
        update analysis_statistics set id=id+1000000,analysis_id=analysis_id+1000000 where analysis_id=(select id from analysis where user_id=2969 and user_book_id=22341)
        update analysis set id=id+1000000,user_id=user_id+1000000,user_book_id=user_book_id+1000000 where user_id=2969 and user_book_id=22341
        update personalise_status set id=id+1000000,analysis_id=analysis_id+1000000 where analysis_id=(select id from personalise where user_id=2969 and user_book_id=22341)
        update personalise set id=id+1000000,user_id=user_id+1000000,user_book_id=user_book_id+1000000 where user_id=2969 and user_book_id=22341
    2 knowledge_study method_study example_study appele_test
        UPDATE knowledge_study SET id=id+1000000,test_id=test_id+1000000 WHERE test_id in (select id from test where user_id=2969 and user_book_id=22341);
        UPDATE method_study SET id=id+1000000,test_id=test_id+1000000 WHERE test_id in (select id from test where user_id=2969 and user_book_id=22341);
        UPDATE example_study SET id=id+1000000,test_id=test_id+1000000 WHERE test_id in (select id from test where user_id=2969 and user_book_id=22341);
        UPDATE apply_test SET id=id+1000000,test_id=test_id+1000000 WHERE test_id in (select id from test where user_id=2969 and user_book_id=22341);
    3 mystic user_current_catalog user_extend weak
        update mystic set id=id+1000000,user_id=user_id+1000000,user_book_id=user_book_id+1000000 where user_id=2969 and user_book_id=22341;
        update user_current_catalog set id=id+1000000,user_id=user_id+1000000,user_book_id=user_book_id+1000000 where user_id=2969 and user_book_id=22341;
        update user_extend set id=id+1000000,user_id=user_id+1000000 where user_id=2969;
        update weak set id=id+1000000,uid=uid+1000000 where uid=2969;
    4 attendance_detail user_communication test
        update user_communication set id=id+1000000,stu_id=stu_id+1000000 where stu_id=stu_id and attendance_detail_id in (select id from attendance_detail where user_id=2969 and user_book_id=22341)
        update attendance_detail set id=id+1000000,user_id=user_id+1000000,user_book_id=user_book_id+1000000 where user_id=2969 and user_book_id=22341;
        UPDATE test SET id=id+1000000,user_id=user_id+1000000,user_book_id=user_book_id+1000000 WHERE id=2969 AND user_book_id=22341
    """
    db_name = get_db_name(p_id)
    # ************清除所有关卡数据
    sql1 = """select id from test where user_id={user_id} and user_book_id={user_book_id}""".format(user_id=uid,user_book_id=user_book_id)
    tids =[int(o.get('id')) for o in fetchall_to_many(db_name,sql1,57)]
    try:
        sql2 = """
            UPDATE knowledge_study SET id=id+{n},test_id=test_id+{n} WHERE test_id in ({tids});
            UPDATE method_study SET id=id+{n},test_id=test_id+{n} WHERE test_id in ({tids});
            UPDATE example_study SET id=id+{n},test_id=test_id+{n} WHERE test_id in ({tids});
            UPDATE apply_test SET id=id+{n},test_id=test_id+{n} WHERE test_id in ({tids});
        """.format(tids=','.join(map(str, tids)),n=n)
        conn_db(db_name,sql2,57,many=True)
        time.sleep(0.5)
    except:
        pass
    # print('清除所有关卡数据')
    # ***********清除学情分析，个性化作业
    try:
        sql3 = """
            update analysis_statistics set id=id+{n},analysis_id=analysis_id+{n} where analysis_id in (select id from analysis where user_id={user_id} and user_book_id={user_book_id});
            update personalise_statistics set id=id+{n},personalise_id=personalise_id+{n} where personalise_id in (select id from personalise where user_id={user_id} and user_book_id={user_book_id});
        """.format(n=n,user_id=uid,user_book_id=user_book_id)
        conn_db(db_name, sql3, 57, many=True)
        time.sleep(0.5)
    except:
        pass
    print('清除学情分析，个性化作业')
    # ***********清除独立部分
    try:
        sql4 = """
            update mystic set id=id+{n},user_id=user_id+{n},user_book_id=user_book_id+{n} where user_id={user_id} and user_book_id={user_book_id};
            update user_current_catalog set id=id+{n},user_id=user_id+{n},user_book_id=user_book_id+{n} where user_id={user_id} and user_book_id={user_book_id};
            update user_extend set id=id+{n},user_id=user_id+{n} where user_id={user_id};
            update weak set id=id+{n},uid=uid+{n} where uid={user_id};
        """.format(n=n,user_id=uid,user_book_id=user_book_id)
        conn_db(db_name, sql4, 57, many=True)
        time.sleep(0.5)
    except:
        pass
    print('清除独立部分')
    # ************清除最后关联表
    try:
        sql5 = """
            update personalise set id=id+{n},user_id=user_id+{n},user_book_id=user_book_id+{n} where user_id={user_id} and user_book_id={user_book_id};
            update analysis set id=id+{n},user_id=user_id+{n},user_book_id=user_book_id+{n} where user_id={user_id} and user_book_id={user_book_id};
            update user_communication set id=id+{n},stu_id=stu_id+{n} where stu_id=stu_id and attendance_detail_id in (select id from attendance_detail where user_id={user_id} and user_book_id={user_book_id});
            update attendance_detail set id=id+{n},user_id=user_id+{n},user_book_id=user_book_id+{n} where user_id={user_id} and user_book_id={user_book_id};
            UPDATE test SET id=id+{n},user_id=user_id+{n},user_book_id=user_book_id+{n} WHERE user_id={user_id} AND user_book_id={user_book_id};
        """.format(n=n,user_id=uid,user_book_id=user_book_id)
        conn_db(db_name, sql5, 57, many=True)
        time.sleep(0.5)
    except:
        pass
    print('清除最后关联表')

    UserBook.objects.filter(pk=user_book_id).update(start_catalog_id=0,last_catalog_id=0,used_lesson_num=0)
    time1 = time.strftime('%m/%d %H:%M:%S', time.localtime(int(time.time())))
    main = u'您于%s恢复了出厂设置--4' % (time1)
    Clear.objects.create(uid=uid, p_id=p_id, c_id=0, l_id=0, explain=main, add_time=int(time.time()))
    return 1
