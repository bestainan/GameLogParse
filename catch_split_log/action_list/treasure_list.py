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
from util.logs_out_in_path import *
from util.logs_out_path_of_parse import get_parse_path

TREASURE_FRAGMENT_ACTION_LST = ['add_treasure_frag_list','remove_treasure_frag_list']
TREASURE_ACTION_LST = ['add_treasure_list', 'treasure_level_up_material', 'treasure_phase_up_material']

def start(split_date):
    """
        获取并拆分一天的日志
    """
    LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST = get_parse_path(split_date)

    # 本地打开
    for _server_id in LOCAL_LOG_PATH_NAME_LST:
        try:
            read_file = LOCAL_LOG_PATH_NAME_LST[_server_id].format(cur_date=split_date)
            log_lines = open(read_file, 'r')
            print(split_date)

            action_treasure_fragment_lst = []
            action_treasure_lst = []

            if log_lines:
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        continue

                    for key, val in log_dict.items():
                        if key in TREASURE_FRAGMENT_ACTION_LST:
                            dat = _insert_treasure_frag(log_dict['uid'], log_dict['log_time'], log_dict['server_id'], log_dict['platform_id'], log_dict['action'], log_dict['level'], key, val)
                            if dat:
                                action_treasure_fragment_lst.extend(dat)
                        elif key in TREASURE_ACTION_LST:
                            dat = _insert_treasure(log_dict['uid'], log_dict['log_time'], log_dict['server_id'], log_dict['platform_id'], log_dict['action'], log_dict['level'], key, val)
                            if dat:
                                action_treasure_lst.extend(dat)

                out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # 宝物碎片
                print("USER_TREASURE_FRAGMENT")
                out_put_file = open(out_put_file_path + 'USER_TREASURE_FRAGMENT', 'w')
                pickle.dump(action_treasure_fragment_lst, out_put_file)
                out_put_file.close()
                # del action_treasure_fragment_lst
                time.sleep(0.1)

                # 宝物输出
                print("USER_TREASURE")
                out_put_file = open(out_put_file_path + 'USER_TREASURE', 'w')
                pickle.dump(action_treasure_lst, out_put_file)
                out_put_file.close()
                # del action_treasure_lst
                time.sleep(0.1)
        except:
            pass


def _insert_treasure_frag(uid, log_time, channel_id, server_id, action, level, item_action,  treasure_frag_lst):
    """
        插入宝物碎片数据
    """
    if treasure_frag_lst:
        treasure_frag_lst = map(int, treasure_frag_lst)
        result = []
        for index in xrange(0, len(treasure_frag_lst), 2):
            _tid = treasure_frag_lst[index]
            if item_action == TREASURE_FRAGMENT_ACTION_LST[0]:
                _num = treasure_frag_lst[index + 1]
            else:
                _num = -treasure_frag_lst[index + 1]

            result.append({"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id, "action":action,"level":level, "tid":_tid, "num":_num})
        return result
    return None


def _insert_treasure(uid, log_time, channel_id, server_id, action, level, item_action,  treasure_lst):
    """
        插入宝物碎片数据
    """
    if treasure_lst:
        treasure_lst = map(int, treasure_lst)
        result = []
        for index in xrange(0, len(treasure_lst), 2):
            _tid = treasure_lst[index]
            if item_action == TREASURE_ACTION_LST[0]:
                _num = treasure_lst[index + 1]
            else:
                if index + 1 < len(treasure_lst):
                    _num = -treasure_lst[index + 1]
                else:
                    _num = -1

            result.append({"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id, "action":action, "level":level, "tid":_tid, "num":_num})
        return result
    return None


if __name__ == "__main__":
    start(sys.argv)

