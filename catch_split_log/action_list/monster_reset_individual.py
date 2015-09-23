# -*- coding:utf-8 -*-

"""
    固定每天抓取拆分日志到当前服务器
    要伴随服务器开启而开启
"""
import pickle
import datetime
import sys
import os
import stat
import urllib2
from util import game_define
from action.parse_action import log_parse
from util.logs_out_in_path import *
from util.logs_out_path_of_parse import get_parse_path


MONSTER_ACTION_LST = ['add_monster_list', 'remove_monster_list']
action_monster_lst = []

MONSTER_RESET_ACTION_LST = [game_define.EVENT_ACTION_RESET_INDIVIDUAL_MONSTER, game_define.EVENT_ACTION_STONE_RESET_INDIVIDUAL_MONSTER]

action_log_dict = dict()

def start(split_date):
    """
        获取并拆分一天的日志
    """
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST = get_parse_path(split_date)

    # 本地打开
    for _server_id in LOCAL_LOG_PATH_NAME_LST:
        read_file = LOCAL_LOG_PATH_NAME_LST[_server_id].format(cur_date=split_date)
        try:
            log_lines = open(read_file, 'r')
            print(split_date)

            if log_lines:
                global action_monster_lst
                global action_log_dict
                action_monster_lst = []
                action_log_dict = {}
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        continue

                    action_id = log_dict['action']
                    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(action_id, 'Err')

                    if log_dict['action'] in MONSTER_RESET_ACTION_LST:
                        # 插入列表 用来输出文件
                        if action_str in action_log_dict:
                            action_log_dict[action_str].append(log_dict)
                        else:
                            action_log_dict[action_str] = [log_dict]

                out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # 宠物洗练
                _output_MONSTER_RESET_INDIVIDUAL(out_put_file_path)
        except:
            pass


def _output_MONSTER_RESET_INDIVIDUAL(out_put_file_path):
    """
        宠物洗练
        # 宠物  {uid_}
        [_name, reset_50_user_num, reset_50_100_user_num, reset_100_200_user_num, reset_200_400_user_num, reset_400_800_user_num, reset_up_800_user_num]
    """
    print("MONSTER_RESET_INDIVIDUAL")
    global action_log_dict
    reset_individual_log_lst = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_RESET_INDIVIDUAL_MONSTER, 'Err')
    reset_individual_log_lst.extend(action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STONE_RESET_INDIVIDUAL_MONSTER, 'Err')
    reset_individual_log_lst.extend(action_log_dict.get(action_str, []))

    _dat = dict()
    for _log in reset_individual_log_lst:
        _monster_tid = _log['monster_tid']
        _user_uid = _log['uid']
        _user_reset_dict = _dat.get(_monster_tid, dict())
        _user_reset_dict[_user_uid] = _user_reset_dict.get(_user_uid, 0) + 1
        _dat[_monster_tid] = _user_reset_dict

    result = []
    for _tid, _user_reset_dict in _dat.items():
        # less_50 = 0
        # in_50_100 = 0
        # in_100_200 = 0
        # in_200_400 = 0
        # in_400_800 = 0
        # up_800 = 0
        _result = []
        reset_count = [0] * 21
        for _num in _user_reset_dict.values():
            if _num < 100:
                reset_count[_num/5] += 1
            else:
                reset_count[20] += 1
            # if _num < 50:
            #     less_50 += 1
            # elif 50 <= _num < 100:
            #     in_50_100 += 1
            # elif 100 <= _num < 200:
            #     in_100_200 += 1
            # elif 200 <= _num < 400:
            #     in_200_400 += 1
            # elif 400 <= _num < 800:
            #     in_400_800 += 1
            # elif 800 <= _num:
            #     up_800 += 1

        # result.append([_tid, less_50, in_50_100, in_100_200, in_200_400, in_400_800, up_800])
        _result.append(_tid)
        _result.extend(reset_count)
        result.append(_result)

    out_put_file = open(out_put_file_path + 'MONSTER_RESET_INDIVIDUAL', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


if __name__ == "__main__":
    start(sys.argv)