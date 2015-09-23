# -*- coding:utf-8 -*-

"""
    固定每天抓取拆分日志到当前服务器
    要伴随服务器开启而开启
"""
import time
import pickle
import cPickle
import datetime
import sys
import os
import stat
import math
from action.parse_action import log_parse
from util.logs_out_path_of_parse import get_parse_path
from util import utility

EQUIP_ACTION_LST = ['add_equip_list', 'remove_equip_list']
FILE_NAME = 'USER_EQUIP'

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

            #每个服务器初始状态
            last_line_num = utility.read_file_last_line(read_file)
            print"this file last line num is:",last_line_num
            cur_line_num = 0
            utility.global_log_lst = []
            err_num = 0
            out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date,use_path="tables")
            if not os.path.exists(out_put_file_path):
                os.makedirs(out_put_file_path)
            os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
            os.chdir(out_put_file_path)

            #开始读
            if log_lines:
                start = time.time()
                #打开文件
                file_path = open(FILE_NAME, 'w+')
                for _log_line in log_lines:
                    cur_line_num += 1
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        err_num += 1
                        continue

                    for key, val in log_dict.items():
                        if key in EQUIP_ACTION_LST:
                            dat = _insert_equip_change_log(log_dict['uid'], log_dict['log_time'], log_dict['platform_id'], log_dict['server_id'], log_dict['action'],log_dict['level'], key, val)
                            if dat:
                                utility.global_log_lst.extend(dat)

                    # TOD:1.限制读取条数
                    utility.read_limit(file_path, last_line_num, cur_line_num)
                print 'err_num is: ', err_num
                print FILE_NAME, " loop_dump use time is: ", time.time() - start
                del utility.global_log_lst[:]  # 快速删除大列表
                # 关闭文件
                file_path.close()

                # 装备产出
                _output_CREATE_EQUIP()
                # 装备消耗
                _output_CONSUME_EQUIP()
        except:
            pass


def _insert_equip_change_log(uid, log_time, channel_id, server_id, action, level, item_action,  equip_lst):
    """
        插入装备改变
        # 时间 物品ID 物品数量 用户ID 事件
    """
    if equip_lst and equip_lst != ['[]']:
        equip_lst = map(int, equip_lst)
        result = []
        for index in xrange(0, len(equip_lst), 2):
            _tid = equip_lst[index]
            if item_action == EQUIP_ACTION_LST[0]:
                _num = equip_lst[index + 1]
            else:
                _num = -equip_lst[index + 1]

            result.append({"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id, "action":action, "level": level, "tid":_tid, "num":_num})
        return result
    return None

# --------------------------------------------------装备相关统计------------------------------------------------------
def _output_CREATE_EQUIP():
    """
        装备产出
    """
    print("CREATE_EQUIP")
    _create_equip = dict()
    with open(FILE_NAME, 'r') as open_file:
        while True:
            try:
                _log_lst = cPickle.load(open_file)
                for log in _log_lst:
                    _num = log['num']
                    if _num > 0:
                        _item_tid = log['tid']
                        _action = log['action']
                        action_num_dict = _create_equip.get(_item_tid, dict())
                        action_num_dict[_action] = action_num_dict.get(_action, 0) + 1 * _num
                        _create_equip[_item_tid] = action_num_dict
            except:
                break

        result = []
        for _tid, _action_num_dict in _create_equip.items():
            result.append([_tid, _action_num_dict])

        out_put_file = open('CREATE_EQUIP', 'w')
        pickle.dump(result, out_put_file)
        out_put_file.close()


def _output_CONSUME_EQUIP():
    """
        装备消耗
    """
    print("CONSUME_EQUIP")
    _create_equip = dict()
    with open(FILE_NAME, 'r') as open_file:
        while True:
            try:
                _log_lst = cPickle.load(open_file)
                for log in _log_lst:
                    _num = log['num']
                    if _num < 0:
                        _item_tid = log['tid']
                        _action = log['action']
                        action_num_dict = _create_equip.get(_item_tid, dict())
                        action_num_dict[_action] = action_num_dict.get(_action, 0) + 1 * int(math.fabs(_num))
                        _create_equip[_item_tid] = action_num_dict
            except:
                break

        result = []
        for _tid, _action_num_dict in _create_equip.items():
            result.append([_tid, _action_num_dict])

        out_put_file = open('CONSUME_EQUIP', 'w')
        pickle.dump(result, out_put_file)
        out_put_file.close()


if __name__ == "__main__":
    start(sys.argv)

