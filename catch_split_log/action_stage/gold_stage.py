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

CUR_ACTION_LST = [game_define.EVENT_ACTION_STAGE_GOLD_WIN, game_define.EVENT_ACTION_STAGE_GOLD_FAIL]    # 当前行为ID列表
cur_action_log_dict = dict()    # 当前行为字典
cur_user_level_dict = dict()    # 当前等级字典

def start(split_date):
    """
        获取并拆分一天的日志
    """
    # 本地打开
    LOCAL_LOG_PATH_NAME , OUT_PUT_PATH = get_parse_path(split_date)
    for _server_id in LOCAL_LOG_PATH_NAME:
        try:
            read_file = LOCAL_LOG_PATH_NAME[_server_id].format(cur_date=split_date)
            log_lines = open(read_file, 'r')
            print(split_date)

            if log_lines:
                global cur_action_log_dict, cur_user_level_dict
                cur_user_level_dict = {}
                cur_action_log_dict = {}

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

                out_put_file_path = OUT_PUT_PATH[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                #金币副本
                _output_GOLD_STAGE_CHALLENGE(split_date,out_put_file_path)
        except:
            pass


def _output_GOLD_STAGE_CHALLENGE(split_date,out_put_file_path):
    """
        经验关卡挑战数据
         # 参与人数 参与次数  完成人数 总完成次数 到达要求人数 参与率 成功率

    """
    print("GOLD_STAGE_CHALLENGE")
    normal_stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_GOLD_WIN, 'Err')
    normal_stage_logs.extend(cur_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_GOLD_FAIL, 'Err')
    normal_stage_logs.extend(cur_action_log_dict.get(action_str, []))

    # 胜利失败关卡日志字典
    stage_id_logs_dict = dict()
    for _log in normal_stage_logs:
        _stage_id = _log['stage_index']
        _dat_lst = stage_id_logs_dict.get(_stage_id, [])
        _dat_lst.append(_log)
        stage_id_logs_dict[_stage_id] = _dat_lst

    open_level = game_config.get_game_config_val_int("OpenLevelStageGold")
    can_join_user_num = len(set([_uid for _uid, _lv in cur_user_level_dict.items() if _lv >= open_level]))

    result = []
    for _stage_id, logs in stage_id_logs_dict.items():
        cur_date = split_date.strftime('%m/%d/%Y')
        # 参与人数
        challenge_user_count = len(set([l['uid'] for l in logs]))
        # 参与次数
        challenge_count = len(logs)
        # 总完成次数
        challenge_win_count = len([l for l in logs if l['action'] == game_define.EVENT_ACTION_STAGE_GOLD_WIN])
        # 完成人数
        challenge_win_user_count = len(set([l['uid'] for l in logs if l['action'] == game_define.EVENT_ACTION_STAGE_GOLD_WIN]))
        #胜率
        win_rate = str(round(float(challenge_win_count)/float(challenge_count), 2)*100)+'%'

        # 参与率
        join_rate = str(round(float(challenge_user_count)/float(can_join_user_num), 2)*100)+'%'
        result.append([cur_date,_stage_id, challenge_user_count, challenge_count,  challenge_win_user_count, challenge_win_count, can_join_user_num, join_rate, win_rate])

    #排序
    result.sort(lambda x,y:cmp(x[1],y[1]))
    #副本名称
    for each_lst in result:
        # 副本信息
        stage_config = game_config.get_stages_config(int(each_lst[1]))
        # 副本名称
        stage_name = stage_config['stageInfo']+"_"+str(stage_config['id'])
        each_lst[1] = stage_name

    out_put_file = open(out_put_file_path + 'GOLD_STAGE_CHALLENGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()



# if __name__ == "__main__":
#     start(sys.argv)

# start(['2015-06-05', '2015-06-05'])