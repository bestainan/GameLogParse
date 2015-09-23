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

STAMINA_COST_LST = [game_define.EVENT_ACTION_STAGE_NORMAL_WIN, game_define.EVENT_ACTION_STAGE_HERO_WIN,
                    game_define.EVENT_ACTION_STAGE_MOP, game_define.EVENT_ACTION_GET_CATCH_MONSTER_RESULT,
                    game_define.EVENT_ACTION_TRIAL_BATTLE_WIN, game_define.EVENT_ACTION_TRIAL_BATTLE_FAIL]

uid_stamina_dict = dict()

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
                global uid_stamina_dict
                uid_stamina_dict = {}
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        continue

                    if log_dict['action'] in STAMINA_COST_LST and 'cost_stamina' in log_dict:
                        # 插入列表 用来输出文件
                        _user_uid = log_dict['uid']
                        _cost_stamina = log_dict['cost_stamina']
                        uid_stamina_dict[_user_uid] = uid_stamina_dict.get(_user_uid, 0) + int(_cost_stamina)
                        # if user_uid in uid_stamina_dict:
                        #     uid_stamina_dict[user_uid] += log_dict['cost_stamina']
                        # else:
                        #     uid_stamina_dict[user_uid] = log_dict['cost_stamina']

                out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # 体力消耗
                _output_STAMINA_COST(out_put_file_path, split_date)
        except:
            pass


def _output_STAMINA_COST(out_put_file_path, split_date):
    """
        体力消耗
        [日期, reset_50_user_num, reset_50_100_user_num, reset_100_200_user_num, reset_200_400_user_num, reset_400_800_user_num, reset_up_800_user_num]
    """
    print("STAMINA_COST")
    global uid_stamina_dict

    result = []
    less_120 = 0
    in_120_240 = 0
    in_240_360 = 0
    in_360_480 = 0
    in_480_600 = 0
    in_600_720 = 0
    in_720_840 = 0
    up_840 = 0
    for _num in uid_stamina_dict.values():
        if _num < 120:
            less_120 += 1
        elif 120 <= _num < 240:
            in_120_240 += 1
        elif 240 <= _num < 360:
            in_240_360 += 1
        elif 360 <= _num < 480:
            in_360_480 += 1
        elif 480 <= _num < 600:
            in_480_600 += 1
        elif 600 <= _num < 720:
            in_600_720 += 1
        elif 720 <= _num < 840:
            in_720_840 += 1
        elif 840 <= _num:
            up_840 += 1

    result.append([split_date.strftime("%Y-%m-%d"), less_120, in_120_240, in_240_360, in_360_480, in_480_600, in_600_720, in_720_840, up_840])

    out_put_file = open(out_put_file_path + 'STAMINA_COST', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


if __name__ == "__main__":
    start(sys.argv)