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
from mysql import mysql
from util import game_define
from action.parse_action import log_parse
from util.logs_out_path_of_parse import get_parse_path

user_cur_stone_dict = dict()
user_cur_gold_dict = dict()
# 所有活跃用户（当天登录的非新玩家）
user_active_set = set()
user_active_num = 0


def start(split_date):
    """
        获取并拆分一天的日志
    """
    # split_date = datetime.date.today() - datetime.timedelta(days=1)
    # split_date = datetime.datetime.strptime("2015-5-31", "%Y-%m-%d").date()
    # if len(args) > 1:
    #     try:
    #         split_date_str = args[1]
    #         split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
    #     except:
    #         sys.stderr.write("Err: Use daily_catch_split_log %Y-%m-%d")
    #         sys.exit(1)
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST = get_parse_path(split_date)
    # 本地打开
    for _server_id in LOCAL_LOG_PATH_NAME_LST:
        try:
            read_file = LOCAL_LOG_PATH_NAME_LST[_server_id].format(cur_date=split_date)
            log_lines = open(read_file, 'r')
            print(split_date)

            if log_lines:
                global user_active_set, user_cur_gold_dict, user_cur_stone_dict, user_active_num
                user_active_set = set()
                user_active_num = 0
                user_cur_gold_dict = {}
                user_cur_stone_dict = {}
                for _log_line in log_lines:
                    _log_line = _log_line.strip()

                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        continue

                    # 插入活跃用户
                    if log_dict['install'] != split_date:
                        user_active_set.add(log_dict['uid'])

                    # 计算玩家当前金币数
                    _insert_user_hold_gold(log_dict)
                    # 计算玩家当前钻石数
                    _insert_user_hold_stone(log_dict)

                _calculate_global()

                out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # 玩家持有金币数
                _output_USER_HOLD_GOLD(out_put_file_path)
                time.sleep(0.1)
                # 玩家持有钻石数
                _output_USER_HOLD_STONE(out_put_file_path)
                time.sleep(0.1)
        except:
            pass


def _calculate_global():
    """
        全局数据计算
    """
    #计算活跃玩家数量
    global user_active_num
    global user_active_set
    user_active_num = len(user_active_set)


def _insert_user_hold_stone(log_dict):
    """
         计算玩家拥有钻石
    """
    if 'cur_stone' in log_dict:
        global user_cur_stone_dict
        user_uid = log_dict['uid']
        cur_stone = log_dict['cur_stone']
        log_time = log_dict['log_time']

        _old_dat_dict = user_cur_stone_dict.get(user_uid, dict())
        if 'log_time' not in _old_dat_dict or _old_dat_dict.get('log_time') < log_time:
            _old_dat_dict['log_time'] = log_time
            _old_dat_dict['cur_stone'] = cur_stone
            user_cur_stone_dict[user_uid] = _old_dat_dict


def _insert_user_hold_gold(log_dict):
    """
         计算玩家拥有钻石
    """
    if 'cur_gold' in log_dict:
        global user_cur_gold_dict
        user_uid = log_dict['uid']
        cur_gold = log_dict['cur_gold']
        log_time = log_dict['log_time']

        _old_dat_dict = user_cur_gold_dict.get(user_uid, dict())
        if 'log_time' not in _old_dat_dict or _old_dat_dict.get('log_time') < log_time:
            _old_dat_dict['log_time'] = log_time
            _old_dat_dict['cur_gold'] = cur_gold
            user_cur_gold_dict[user_uid] = _old_dat_dict


# --------------------------------------------------数值平衡------------------------------------------------------
def _output_USER_HOLD_GOLD(out_put_file_path):
    """
         玩家持有金币数
    """
    print("USER_HOLD_GOLD")
    global user_active_num
    total_gold = sum([_val['cur_gold'] for _val in user_cur_gold_dict.values()])
    total_user = len(user_cur_gold_dict.keys())

    _dat = dict()
    _dat['total_gold'] = total_gold
    _dat['total_user'] = total_user
    _dat['active_user'] = user_active_num

    out_put_file = open(out_put_file_path + 'USER_HOLD_GOLD', 'w')
    pickle.dump(_dat, out_put_file)
    out_put_file.close()


def _output_USER_HOLD_STONE(out_put_file_path):
    """
        玩家持有钻石数
    """
    print("USER_HOLD_STONE")
    total_stone = sum([_val['cur_stone'] for _val in user_cur_stone_dict.values()])
    total_user = len(user_cur_stone_dict.keys())
    global user_active_num

    _dat = dict()
    _dat['total_stone'] = total_stone
    _dat['total_user'] = total_user
    _dat['active_user'] = user_active_num

    out_put_file = open(out_put_file_path + 'USER_HOLD_STONE', 'w')
    pickle.dump(_dat, out_put_file)
    print(_dat)
    out_put_file.close()


