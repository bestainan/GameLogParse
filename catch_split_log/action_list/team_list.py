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

            action_team_lst = []

            if log_lines:
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        continue

                    for key, val in log_dict.items():
                        if key == 'team_list':
                            dat = _insert_user_team(log_dict['uid'], log_dict['log_time'], log_dict['server_id'], log_dict['platform_id'], log_dict['team_list'])
                            if dat:
                                action_team_lst.extend(dat)

                out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # 输出队伍
                print("USER_TEAM")
                out_put_file = open(out_put_file_path + 'USER_TEAM', 'w')
                pickle.dump(action_team_lst, out_put_file)
                out_put_file.close()
                # del action_team_lst
                time.sleep(0.1)
        except:
            pass


def _insert_user_team(uid, log_time, channel_id, server_id, team_lst):
    """
        插入玩家队伍信息
    """
    if team_lst:
        team_lst = map(int, team_lst)
        team_monster_num = len(team_lst) / 3
        monster_team_key = ""
        dat = {"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id}
        for index in range(0, team_monster_num):
            _num = index + 1
            monster_team_key += ",monster_%s,star_%s,level_%s" % (_num, _num, _num)
            dat.update({
                "monster_%s" % _num : team_lst[index * 3],
                "star_%s" % _num : team_lst[index * 3 + 1],
                "level_%s" % _num : team_lst[index * 3 + 2]
            })
        return [dat]
    return None


if __name__ == "__main__":
    start(sys.argv)

