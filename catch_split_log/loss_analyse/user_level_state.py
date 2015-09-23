# -*- coding:utf-8 -*-

"""
    固定每天抓取拆分日志到当前服务器
    要伴随服务器开启而开启
"""
import time
import pickle
import datetime
import sys
import os
import stat
import urllib2
import math
from action.parse_action import log_parse
from util.logs_out_path_of_parse import get_parse_path

# 玩家等级分布
user_level_dict = dict()
# 当天所有新安装的用户
users_new_install_set = set()
users_new_install_num = 0
# 所有活跃用户（当天登录的非新玩家）
user_active_set = set()
user_active_num = 0


def start(split_date):
    """
        获取并拆分一天的日志
    """
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST = get_parse_path(split_date)

    # 本地打开
    for _server_id in LOCAL_LOG_PATH_NAME_LST:
        try:
            read_file = LOCAL_LOG_PATH_NAME_LST[_server_id].format(cur_date=split_date)
            log_lines = open(read_file, 'r')
            print(split_date)

            if log_lines:
                global user_level_dict
                global user_active_set
                global users_new_install_set
                user_level_dict = {}
                user_active_set = set()
                users_new_install_set = set()
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        continue

                    # 插入活跃用户
                    if log_dict['install'] != split_date:
                        user_active_set.add(log_dict['uid'])
                    else:
                        users_new_install_set.add(log_dict['uid'])

                    # 插入玩家等级分布
                    user_level = log_dict['level']
                    user_uid = log_dict['uid']

                    if user_level > user_level_dict.get(user_uid, 0):
                        user_level_dict[user_uid] = user_level

                _calculate_global()

                out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # 流失分析- 玩家等级
                _output_USER_LEVEL_STATE(out_put_file_path)

                # 用户等级情况
                _output_USER_LEVEL_ARRIVE(out_put_file_path)
        except Exception, e:
            print e


def _calculate_global():
    """
        全局数据计算
    """
    #计算活跃玩家数量
    global user_active_num
    global user_active_set
    user_active_num = len(user_active_set)

    global users_new_install_num
    global users_new_install_set
    users_new_install_num = len(users_new_install_set)


def _output_USER_LEVEL_STATE(out_put_file_path):
    """
        用户等级分布
        # 登录用户数  新增用户数  等级用户数
    """
    print("USER_LEVEL_STATE")
    global users_new_install_num
    global user_active_num
    result = []
    new_user_num = users_new_install_num
    active_num = user_active_num
    # 登录用户数
    login_user_num = active_num + new_user_num
    result.append(login_user_num)
    result.append(new_user_num)

    # 等级用户数
    for lv in xrange(1, 121):
        _user_num = 0
        for _l in user_level_dict.values():
            if _l == lv:
                _user_num += 1
        result.append(_user_num)

    out_put_file = open(out_put_file_path + 'USER_LEVEL_STATE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_USER_LEVEL_ARRIVE(out_put_file_path):
    """
        用户等级情况
        # uid:level
    """
    print("USER_LEVEL_ARRIVE")

    out_put_file = open(out_put_file_path + 'USER_LEVEL_ARRIVE', 'w')
    pickle.dump(user_level_dict, out_put_file)
    out_put_file.close()


if __name__ == "__main__":
    start(sys.argv)
