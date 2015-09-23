# -*- coding:utf-8 -*-

"""
    游戏管理员操作日志解析
"""
import pickle
import datetime
import sys
import os
import stat
from game_manager.action_gm.parse_action_gm import gm_log_parse
from util import game_define


LOCAL_LOG_PATH_NAME = "/home/ubuntu/data/HaiMaLogs/game_manager_{cur_date}/game_manager_{cur_date}_00000"
OUT_PUT_PATH = "/home/ubuntu/data/ManagerLogParse/{cur_date}/{use_path}/"

all_manager_log_dict = dict()


def start(split_date):
    """
        获取并拆分一天的日志
    """
    start_time = datetime.datetime.now()
    print 'manager_operation解析开始', start_time, '\n\n'
    # 本地打开
    read_file = LOCAL_LOG_PATH_NAME.format(cur_date=split_date)
    log_lines = open(read_file, 'r')
    print(read_file)

    if log_lines:
        global all_manager_log_dict
        for _log_line in log_lines:
            _log_line = _log_line.strip()
            log_dict = gm_log_parse(_log_line)
            if not log_dict:
                print _log_line
                continue

            account = log_dict['account']
            # action_str = game_define.GM_LOG_ACTION_NAME_DICT.get(action_id, 'Err')

            # 插入列表 用来输出文件
            if account in all_manager_log_dict:
                all_manager_log_dict[account].append(log_dict)
            else:
                all_manager_log_dict[account] = [log_dict]

        out_put_file_path = OUT_PUT_PATH.format(cur_date=split_date, use_path="operation")
        if not os.path.exists(out_put_file_path):
            os.makedirs(out_put_file_path)
        os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

        _output_all_managers(out_put_file_path)
    log_lines.close()

    end_time = datetime.datetime.now()
    print 'manager_operation解析结束', end_time
    print 'manager_operation共花费时间', (end_time - start_time).seconds, '秒', '\n\n'


def _output_all_managers(out_put_file_path):
    """
        输出成文件，每个管理员一个文件
    """
    global all_manager_log_dict
    for account in all_manager_log_dict:
        if account:
            print(str(account) + " output start")

            out_put_file = open(out_put_file_path + str(account), 'w')
            pickle.dump(all_manager_log_dict[account], out_put_file)
            out_put_file.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start(split_date)
