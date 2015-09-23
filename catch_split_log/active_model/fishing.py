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
from util.logs_out_path_of_parse import get_parse_path
from config import game_config


CUR_ACTION_LST = [game_define.EVENT_ACTION_FISHING_ONCE, game_define.EVENT_ACTION_FISHING_LOOP]     # 当前行为ID表
cur_action_log_dict = dict()    # 当前行为字典
cur_user_level_dict = dict()    # 当前等级字典

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
                global cur_action_log_dict
                global cur_user_level_dict
                cur_action_log_dict = {}
                cur_user_level_dict = {}
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        continue
                    action_id = log_dict['action']
                    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(action_id, 'Err')

                    if log_dict['action'] in CUR_ACTION_LST:
                        # 插入列表 用来输出文件
                        if action_str in cur_action_log_dict:
                            cur_action_log_dict[action_str].append(log_dict)
                        else:
                            cur_action_log_dict[action_str] = [log_dict]
                    user_level = log_dict['level']
                    user_uid = log_dict['uid']
                    if user_level > cur_user_level_dict.get(user_uid, 0):
                        cur_user_level_dict[user_uid] = user_level

                out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # 钓鱼
                _output_FISHING(out_put_file_path)
        except:
            pass


def _output_FISHING(out_put_file_path):
    """
        钓鱼
        参与人数	总钓鱼次数	到达要求人数	参与率
    """
    print("FISHING")
    fishing_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_FISHING_ONCE, 'Err')
    fishing_logs.extend(cur_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_FISHING_LOOP, 'Err')
    fishing_logs.extend(cur_action_log_dict.get(action_str, []))

    join_user_num = len(set([log['uid'] for log in fishing_logs]))

    fishing_count = sum([log['cost_fishing_count'] for log in fishing_logs])

    open_level = game_config.get_game_config_val_int("OpenLevelFishing")
    can_join_user_num = len(set([_uid for _uid, _lv in cur_user_level_dict.items() if _lv >= open_level]))

    rate = round(float(join_user_num)/ float(can_join_user_num), 2)

    result = [join_user_num, fishing_count, can_join_user_num, rate]

    out_put_file = open(out_put_file_path + 'FISHING', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


if __name__ == "__main__":
    start(sys.argv)