# -*- coding:utf-8 -*-

"""
    固定每天抓取拆分日志到当前服务器
    要伴随服务器开启而开启
    注：联盟数据统计
    1.如果断天 或少收集数据 数据开始会不准确 以后会越来越准确
    2.'union_real_number' 没有 'member_lst' 长度为1 的数据就只有自己

    ############################################################期望格式
    #                       key                         联盟等级    联盟真实数量        联盟名称                                     联盟等级                           联盟真实成员数量              联盟uid              联盟成员列表     数据会越来越准确           联盟副本
    ###    筛选 最后格式为 {3023: {'server_id': 10001,'level':1,'union_real_number': 5 ，'name': '\xe9\xa6\x99\xe8\xbe\xa3\xe8\x9f?', 'level': 1, 'platform_id': 999999, 'union_real_number': 48, 'union_uid': 3023, 'member_lst': [1000102411,1000102400],'stage':{'2015-05-20':[8001,64545,8002,46468],'2015-05-21':[7001,62404,7002,6544,7003,66444]}}
    ############################################################现在格式
    #                       key                         联盟等级  联盟真实数量             联盟名称                                     联盟等级                           联盟真实成员数量              联盟uid              联盟成员列表
    ###    筛选 最后格式为 {3023: {'server_id': 10001,'level':1,'union_real_number': 5 ， 'name': '\xe9\xa6\x99\xe8\xbe\xa3\xe8\x9f?', 'level': 1, 'platform_id': 999999, 'union_real_number': 48, 'union_uid': 3023, 'member_lst': [1000102411,1000102400]}
    ############################################################现有问题

    1.联盟副盟主 没有罢免副盟主的aciton  所以副盟主成员列表统计不正确 应该创建有这个事件
    3.副本信息没统计

"""
import time
import pickle
import datetime
import sys
import os
import stat
import urllib2
import math
from mysql import mysql
from util import game_define
from action.parse_action import log_parse
from util.logs_out_path_of_parse import get_parse_path
import copy

# 飞流mysql 飞流日志服务器地址
CATCH_SQL_HOST = "556418a8f30f9.sh.cdb.myqcloud.com:6080"
LOG_SERVER_PATH = "http://115.159.77.250:8086/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"

# ZGAME 海马日志服务器地址
# CATCH_SQL_HOST = "555ff729cffb0.sh.cdb.myqcloud.com:6200"
# LOG_SERVER_PATH = "http://115.159.69.65:8086/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"

CATCH_SQL_PAS = "Zgamecn6"

LOCAL_LOG_START_DATE = '2015-05-21'

OUT_PUT_FILE_DIRECTORY = "tables"
OUT_PUT_FILE_NAME = "UNION_DETAIL"
OUT_PUT_FILE_NAME_TWO = "UNION_HALL"

# mysql 队列
mysql_queue = []

# 联盟详细信息
union_detail_dict_global = dict()
#需要过滤掉的数据 例如：申请加入 与联盟数据无关
UNION_FILTER_ACTION_LST = [
    game_define.EVENT_ACTION_UNION_APPLY_JOIN,
]
#需要移除key值数据 例如：解散联盟
union_pop_key_lst_global = []
UNION_REMVOE_KEY_ACTION_LST = [
    game_define.EVENT_ACTION_UNION_DISMISS,
]
#需要过滤 但需要收集部分数据
UNION_NEED_FILTER_UID_ACTION_LST = [
    game_define.EVENT_ACTION_UNION_EXIT,
]

def start(split_date):
    """
        获取并拆分一天的日志 没数据
    """
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST = get_parse_path(split_date)

    for index in LOCAL_LOG_PATH_NAME_LST:
        try:
            # 本地打开
            start_time = time.time()
            read_file = LOCAL_LOG_PATH_NAME_LST[index].format(cur_date=split_date)
            log_lines = open(read_file, 'r')
            print split_date, " ", index
            end_time = time.time() - start_time
            print "open file time is :", end_time

            if log_lines:
                global union_detail_dict_global

                # 抓取昨天的union_detail_dict_global
                yesterday_union_detail_file_path = OUT_PUT_PATH_LST[index].format(cur_date=(split_date - datetime.timedelta(days=1)), use_path=OUT_PUT_FILE_DIRECTORY)
                if os.path.exists(yesterday_union_detail_file_path + OUT_PUT_FILE_NAME):
                    os.chdir(yesterday_union_detail_file_path)
                    open_file = open(OUT_PUT_FILE_NAME, 'r')
                    union_detail_dict_global = pickle.load(open_file)
                    open_file.close()
                # print "yesterday file is" + OUT_PUT_FILE_NAME,"lens is: ", len(union_detail_dict_global), "  date is:", yesterday_union_detail_file_path, "\n"
                start_time = time.time()
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    #解析错误返回false 跳过本行
                    if not log_dict:
                        continue
                    # 联盟等级统计
                    _insert_union_statistics(log_dict)
                end_time = time.time() - start_time
                print "compute time is :", end_time

                out_put_file_path = OUT_PUT_PATH_LST[index].format(cur_date=split_date, use_path=OUT_PUT_FILE_DIRECTORY)
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # start_time = time.time()
                # #TODO  在需要时 输出到mysql 已注释需重改
                # # _output_user_detail_to_mysql(split_date)
                # end_time = time.time() - start_time
                # print "mysql  time is :", end_time, "\n"

                start_time = time.time()
                # 联盟详细信息
                _output_UNION_DETAIL(out_put_file_path, index)
                #调用筛选函数
                end_time = time.time() - start_time
                print "file output time is :", end_time, "\n\n"
        except:
            print "error----",index


def _output_UNION_DETAIL(out_put_path, index):
    """
        输出联盟详细信息
    """
    global union_pop_key_lst_global
    global union_detail_dict_global
    #在输出详细信息前 输出联盟殿堂数据 并移除解散的联盟
    _output_UNION_HALL(out_put_path, index)

    out_put_file = open(out_put_path + OUT_PUT_FILE_NAME, 'w')
    print OUT_PUT_FILE_NAME
    pickle.dump(union_detail_dict_global, out_put_file)
    out_put_file.close()
    time.sleep(1)
    #下个服务器需要清空全局变量 在每次循环最后执行
    golbal_clear()


def golbal_clear():
    global union_detail_dict_global
    global union_pop_key_lst_global

    union_detail_dict_global.clear()
    union_pop_key_lst_global = []


def _output_UNION_HALL(out_put_path, index):
    global union_detail_dict_global
    global union_pop_key_lst_global
    start_time = time.time()

    #计算联盟殿堂数据
    # _temp_detail_dit = copy.deepcopy(union_detail_dict_global)
    # _temp_pop_key_lst = copy.deepcopy(union_pop_key_lst_global)
    _temp_detail_dit = union_detail_dict_global
    _temp_pop_key_lst = union_pop_key_lst_global
    union_total_num = len(_temp_detail_dit)                                 # 联盟总数
    union_dismiss_num = len(_temp_pop_key_lst)                              # 联盟解散数量

    #注：因为需要计算数据 所以在此pop解散联盟 python中赋值是引用  要副本可以用copy.deepcopy深拷贝
    for U_uid in _temp_pop_key_lst:
        _temp_detail_dit.pop(U_uid)

    #获得存在等级列表 筛选数据
    level_lst = []
    for key, value in _temp_detail_dit.items():
        level_lst.append(value.get('level', 1))
    level_lst = list(set(level_lst))
    level_lst.sort()

    # 计算联盟等级成员数量 与 总数量
    union_member_total_num = 0
    for level in level_lst:
        union_member_num = 0
        for key, value in _temp_detail_dit.items():
            if level == value.get('level', 1):
                if -1 == value.get('union_real_number', -1):
                    union_member_num += len(value['member_lst'])
                else:
                    union_member_num += value['union_real_number']

        union_member_total_num += union_member_num

    # 输出结果列表
    output_lst = []
    for level in level_lst:
        union_member_num = 0
        union_num = 0
        for key, value in _temp_detail_dit.items():
            if level == value.get('level', 1):                                  # 是当前等级 收集联盟数量 与总数量
                if -1 == value.get('union_real_number', -1):                    # 没有真实成员数量
                    union_member_num += len(value['member_lst'])
                    union_num += 1
                else:                                                           # 有真实成员数量
                    union_member_num += value['union_real_number']
                    union_num += 1

        union_member_rate = round(float(union_member_num)/float(union_member_total_num), 2)     # 联盟成员占比
        union_rate = round(float(union_num)/float(union_total_num), 2)                          # 联盟占比

        each_level_lst = [
            level,                                      # 联盟等级
            union_num,                                  # 联盟存在数量
            union_member_num,                           # 联盟成员数量
            union_dismiss_num,                          # 联盟解散数量
            str(union_rate*100)+'%',                    # 联盟占比
            str(union_member_rate*100)+'%',             # 联盟成员占比
            index,                                      # 服务器id
        ]
        output_lst.append(each_level_lst)

    out_put_file = open(out_put_path + OUT_PUT_FILE_NAME_TWO, 'w')
    print OUT_PUT_FILE_NAME_TWO
    pickle.dump(output_lst, out_put_file)
    out_put_file.close()
    time.sleep(1)
    end_time = time.time() - start_time
    print "file output time is :", end_time
    # print(output_lst), 'HALL '


def _insert_union_statistics(log_dict):
    """
        计算联盟等级 所有事件中都会有联盟等级
    """
    global union_detail_dict_global
    _union_server_id = log_dict['server_id']
    _union_platform_id = log_dict['platform_id']
    _uid = log_dict['uid']
    _union_uid = log_dict.get('union_uid', 0)
    _member_lst = []

    if _union_uid and log_dict['action'] not in UNION_FILTER_ACTION_LST:
        if _union_uid in union_detail_dict_global:
            #先提前公有数据
            union_detail_dict_global[_union_uid].update({
                'union_uid': _union_uid,
                'server_id': _union_server_id,
                'platform_id': _union_platform_id,
            })
        else:
            _member_lst.append(_uid)
            union_detail_dict_global[_union_uid] = {
                'union_uid': _union_uid,
                'server_id': _union_server_id,
                'platform_id': _union_platform_id,
                'member_lst': _member_lst
            }
        #再插入可能存在数据
        if 'union_name' in log_dict:
            union_detail_dict_global[_union_uid]['name'] = log_dict['union_name']
        if 'union_level' in log_dict:
            union_detail_dict_global[_union_uid]['level'] = log_dict['union_level']
        # 联盟成员列表
        if 'uid' in log_dict:
            union_detail_dict_global[_union_uid]['member_lst'].append(log_dict['uid'])
            union_detail_dict_global[_union_uid].update({'member_lst': list(set(union_detail_dict_global[_union_uid]['member_lst']))})
        # 副手列表
        if 'union_new_leader' in log_dict:
            lst = union_detail_dict_global[_union_uid].get('union_new_leader', [])
            lst.append(log_dict['union_new_leader'])
            union_detail_dict_global[_union_uid].update({'union_new_leader': lst})
            union_detail_dict_global[_union_uid]['member_lst'].append(log_dict['uid'])
            union_detail_dict_global[_union_uid]['member_lst'].append(log_dict['union_new_leader'])
            union_detail_dict_global[_union_uid].update({'member_lst': list(set(union_detail_dict_global[_union_uid]['member_lst']))})

            # union_detail_dict_global[_union_uid].update({'union_new_leader': list(set(union_detail_dict_global[_union_uid]['union_real_number']))})
        # 联盟当前真实的成员数量 注：假如中间停服 数据开始不对（例如：已有公会成员的成员不登录（即收集不到成员信息））
        if 'union_cur_number' in log_dict:
            union_detail_dict_global[_union_uid]['union_real_number'] = log_dict['union_cur_number']
        #TODO 添加联盟当天开启副本列表
        #TODO 副盟主罢免

        # 联盟添加成员 union_new_member
        if 'union_new_member' in log_dict:
            union_detail_dict_global[_union_uid]['member_lst'].append(log_dict['union_new_member'])
            union_detail_dict_global[_union_uid].update({'member_lst': list(set(union_detail_dict_global[_union_uid]['member_lst']))})

        #成员列表 remove
        # 联盟删除成员 union_kick_member
        if 'union_kick_member' in log_dict:
            # print "num", log_dict['union_kick_member'],"_uiion_uid",log_dict['union_uid']
            #更新 （去重 并移除提出
            lst = union_detail_dict_global[_union_uid]['member_lst']
            if log_dict['union_kick_member'] in lst:
                _tmp_lst = list(set(union_detail_dict_global[_union_uid]['member_lst']))
                _tmp_lst.remove(log_dict['union_kick_member'])
                union_detail_dict_global[_union_uid].update({'member_lst': _tmp_lst})

        # 成员自动退出
        if log_dict['action'] in UNION_NEED_FILTER_UID_ACTION_LST:
            union_detail_dict_global[_union_uid]['member_lst'].remove(log_dict['uid'])
            union_detail_dict_global[_union_uid].update({'member_lst': list(set(union_detail_dict_global[_union_uid]['member_lst']))})

        #联盟id pop key
        # 解散联盟
        if log_dict['action'] in UNION_REMVOE_KEY_ACTION_LST:
            print "today have union_dismiss, union_id is: ", log_dict['union_uid']
            global union_pop_key_lst_global
            union_pop_key_lst_global.append(log_dict['union_uid'])
            union_pop_key_lst_global = list(set(union_pop_key_lst_global))


# def _start_insert_to_mysql():
#     """
#         插入mysql
#     """
#     mysql_connect = mysql.Connection(CATCH_SQL_HOST, 'manager', 'root', CATCH_SQL_PAS)
#
#     sleep_time = float(1) / float(500)
#
#     while len(mysql_queue):
#         queue_num = len(mysql_queue)
#         # print("准备插入mysql当前队列长度 " + str(queue_num))
#         _sql = ''
#         for i in xrange(min(queue_num, 500)):
#             _sql += mysql_queue.pop()
#         if _sql:
#             mysql_connect.execute(_sql)
#         time.sleep(sleep_time)
#
#
# def _output_user_detail_to_mysql(split_date):
#     """
#         输出用户详细信息到mysql
#     """
#     # 整合mysql语句
#     for user_dict in union_detail_dict_global.values():
#         if user_dict['install'] == split_date:
#             key_lst = user_dict.keys()
#             val_lst = [user_dict[key] for key in key_lst]
#             for index in xrange(len(val_lst)):
#                 val = val_lst[index]
#                 if isinstance(val, datetime.datetime) or isinstance(val, datetime.date):
#                     val_lst[index] = "'%s'" % str(val)
#                 else:
#                     val_lst[index] = str(val)
#
#             key_str = ','.join(key_lst)
#             val_str = ','.join(val_lst)
#             sql = "INSERT INTO union_detail (%s) VALUES (%s);" % (key_str, val_str)
#             mysql_queue.append(sql)
#         else:
#             key_lst = user_dict.keys()
#             val_lst = [user_dict[key] for key in key_lst]
#             for index in xrange(len(val_lst)):
#                 val = val_lst[index]
#                 if isinstance(val, datetime.datetime) or isinstance(val, datetime.date):
#                     val_lst[index] = "'%s'" % str(val)
#                 else:
#                     val_lst[index] = str(val)
#
#             key_val_lst = []
#             for index in xrange(len(key_lst)):
#                 _key = key_lst[index]
#                 _val = val_lst[index]
#                 key_val = "%s=%s" % (_key, _val)
#                 key_val_lst.append(key_val)
#
#             key_val_str = ', '.join(key_val_lst)
#             sql = "UPDATE union_detail SET %s WHERE uid=%s;" % (key_val_str, user_dict['uid'])
#             mysql_queue.append(sql)
#     # _start_insert_to_mysql()


if __name__ == "__main__":
    start(sys.argv)
