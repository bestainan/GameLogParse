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


MONSTER_ACTION_LST = ['add_monster_list', 'remove_monster_list']
action_monster_lst = []


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
                action_monster_lst = []
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        continue

                    for key, val in log_dict.items():
                        if key in MONSTER_ACTION_LST:
                            dat = _insert_monster_change_log(log_dict['uid'], log_dict['log_time'], log_dict['platform_id'], log_dict['server_id'], log_dict['action'],log_dict['level'], key, val)
                            if dat:
                                action_monster_lst.extend(dat)

                out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # 输出怪
                print("USER_MONSTER")
                out_put_file = open(out_put_file_path + 'USER_MONSTER', 'w')
                pickle.dump(action_monster_lst, out_put_file)
                out_put_file.close()
                # del action_monster_lst
                time.sleep(0.1)

                # 宠物产出
                _output_CREATE_MONSTER(out_put_file_path)
                # 宠物消耗
                _output_REMOVE_MONSTER(out_put_file_path)
        except:
            pass


def _insert_monster_change_log(uid, log_time, channel_id, server_id, action, level, item_action,  monster_lst):
    """
        插入宠物改变
        # 时间 物品ID 物品数量 用户ID 事件
    """
    if monster_lst:
        monster_lst = map(int, monster_lst)
        result = []
        for index in xrange(0, len(monster_lst), 3):
            _tid = monster_lst[index]
            _star = monster_lst[index + 1]
            if item_action == MONSTER_ACTION_LST[0]:
                _num = monster_lst[index + 2]
            else:
                _num = -monster_lst[index + 2]
            result.append({"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id, "action":action, "level": level, "tid":_tid, "num":_num, "star": _star})
        return result
    return None


# --------------------------------------------------宠物相关统计------------------------------------------------------
def _output_CREATE_MONSTER(out_put_file_path):
    """
        宠物产出
        宠物 星级 action...

    """
    print("CREATE_MONSTER")
    global action_monster_lst
    _create_monster = dict()
    for log in action_monster_lst:
        _num = log['num']
        if _num > 0:
            _monster_tid = log['tid']
            _star = log['star']
            _action = log['action']
            key_monster = "%s_%s" % (_monster_tid, _star)
            action_num_dict = _create_monster.get(key_monster, dict())
            action_num_dict[_action] = action_num_dict.get(_action, 0) + 1 * _num
            _create_monster[key_monster] = action_num_dict
    result = []
    for key, _action_num_dict in _create_monster.items():
        key_lst = map(int, key.split('_'))
        _tid = key_lst[0]
        _star = key_lst[1]
        result.append([_tid, _star, _action_num_dict])

    out_put_file = open(out_put_file_path + 'CREATE_MONSTER', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_REMOVE_MONSTER(out_put_file_path):
    """
        宠物消耗
    """
    print("REMOVE_MONSTER")
    global action_monster_lst
    _create_monster = dict()
    for log in action_monster_lst:
        _num = log['num']
        if _num < 0:

            _monster_tid = log['tid']
            _star = log['star']
            _action = log['action']
            key_monster = "%s_%s" % (_monster_tid, _star)
            action_num_dict = _create_monster.get(key_monster, dict())
            action_num_dict[_action] = action_num_dict.get(_action, 0) + 1 * int(math.fabs(_num))
            _create_monster[key_monster] = action_num_dict
    result = []
    for key, _action_num_dict in _create_monster.items():
        key_lst = map(int, key.split('_'))
        _tid = key_lst[0]
        _star = key_lst[1]
        result.append([_tid, _star, _action_num_dict])

    out_put_file = open(out_put_file_path + 'REMOVE_MONSTER', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


if __name__ == "__main__":
    start(sys.argv)

