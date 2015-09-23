# -*- coding:utf-8 -*-

"""
    固定每天抓取拆分日志到当前服务器
    要伴随服务器开启而开启
"""
import time
import cPickle
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
from util.logs_out_path_of_parse import LOG_PATH

# ZGAME 海马日志服务器地址
CATCH_SQL_HOST = "5591fa7bbdf6e.sh.cdb.myqcloud.com:5804"

CATCH_SQL_PAS = "Zgamecn6"

# mysql 队列
# mysql_queue = []

# 用户详细信息
user_detail_dict = dict()


def start_parse(split_date):
    """
        获取并拆分一天的日志
    """
    err = open(LOG_PATH+"%s/%s" % ("Error", split_date), 'a+')
    nor = open(LOG_PATH+"%s/%s" % ("Normal", split_date), 'a+')
    sys.stdout = nor
    startime = datetime.datetime.now()
    print 'user_detail解析开始', startime
    LOCAL_LOG_PATH_NAME, OUT_PUT_PATH = get_parse_path(split_date)
    # 本地打开
    for _server_id in LOCAL_LOG_PATH_NAME:
        try:
            sys.stdout = nor
            read_file = LOCAL_LOG_PATH_NAME[_server_id].format(cur_date=split_date)
            log_lines = open(read_file, 'r')
            print(split_date)

            if log_lines:
                global user_detail_dict
                user_detail_dict = {}
                # 抓取昨天的user_detail_dict
                yesterday_user_detail_file_path = OUT_PUT_PATH[_server_id].format(cur_date=(split_date - datetime.timedelta(days=1)), use_path='tables')
                if os.path.exists(yesterday_user_detail_file_path + 'USER_DETAIL'):
                    open_file = open(yesterday_user_detail_file_path + 'USER_DETAIL', 'r')
                    user_detail_dict = cPickle.load(open_file)
                    open_file.close()

                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)

                    # 插入玩家等级分布
                    if not log_dict:
                        continue
                    user_level = log_dict['level']
                    user_uid = log_dict['uid']
                    user_vip_level = log_dict['vip_level']
                    user_install = log_dict['install']
                    user_server_id = log_dict['server_id']
                    user_platform_id = log_dict['platform_id']
                    user_last_player_time = log_dict['log_time']

                    # 插入玩家详细数据
                    if user_uid in user_detail_dict:
                        user_detail_dict[user_uid].update({
                            'uid': user_uid,
                            'install': user_install,
                            'server_id': user_server_id,
                            'platform_id': user_platform_id,
                            'level': user_level,
                            'vip_level': user_vip_level,
                            'last_play_time': user_last_player_time,
                        })
                    else:
                        user_detail_dict[user_uid] = {
                            'uid': user_uid,
                            'install': user_install,
                            'server_id': user_server_id,
                            'platform_id': user_platform_id,
                            'level': user_level,
                            'vip_level': user_vip_level,
                            'last_play_time': user_last_player_time,
                        }
                    if 'cur_rmb' in log_dict:
                        user_detail_dict[user_uid]['rmb'] = log_dict['cur_rmb']
                    if 'cur_gold' in log_dict:
                        user_detail_dict[user_uid]['gold'] = log_dict['cur_gold']
                    if 'cur_stone' in log_dict:
                        user_detail_dict[user_uid]['stone'] = log_dict['cur_stone']
                    if 'cur_arena_emblem' in log_dict:
                        user_detail_dict[user_uid]['emblem'] = log_dict['cur_arena_emblem']
                    if "cur_gym_point" in log_dict:
                        user_detail_dict[user_uid]['gym_point'] = log_dict['cur_gym_point']
                    if 'cur_world_boss_point' in log_dict:
                        user_detail_dict[user_uid]['world_boss_point'] = log_dict['cur_world_boss_point']

                out_put_file_path = OUT_PUT_PATH[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # 输出到mysql
                # _output_user_detail_to_mysql(split_date)
                print "time is:", split_date, "the server is : ", _server_id
                # 用户详细信息
                _output_USER_DETAIL(out_put_file_path)
        except Exception, e:
            sys.stdout = err
            print datetime.datetime.now(), 'User_detail', "  Error:", e, "\n"
            pass

    sys.stdout = nor
    endtime = datetime.datetime.now()
    print 'user_detail解析结束', endtime
    print 'user_detial共花费时间', (endtime-startime).seconds, '秒', '\n\n'


# def _output_user_detail_to_mysql(split_date):
#     """
#         输出用户详细信息到mysql
#     """
#     # 整合mysql语句
#     for user_dict in user_detail_dict.values():
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
#             sql = "INSERT INTO user_detail (%s) VALUES (%s);" % (key_str, val_str)
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
#             sql = "UPDATE user_detail SET %s WHERE uid=%s;" % (key_val_str, user_dict['uid'])
#             mysql_queue.append(sql)
#     _start_insert_to_mysql()


def _output_USER_DETAIL(out_put_file_path):
    """
        输出用户详细信息
    """
    print("USER_DETAIL")
    global user_detail_dict
    _user_detail_dict = user_detail_dict

    out_put_file = open(out_put_file_path + 'USER_DETAIL', 'w')
    cPickle.dump(_user_detail_dict, out_put_file)
    out_put_file.close()


# def _start_insert_to_mysql():
#     """
#         插入mysql
#     """
#     mysql_connect = mysql.Connection(CATCH_SQL_HOST, 'manager_haima', 'root', CATCH_SQL_PAS)
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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start_parse(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start_parse(split_date)

