# -*- coding:utf-8 -*-

"""
    固定每天抓取拆分日志到当前服务器
    要伴随服务器开启而开启
"""
import cPickle
import sys
import os
import stat
from util import game_define
from action.parse_action import log_parse
from util.logs_out_path_of_parse import get_parse_path
from config import game_config
from util.utility import read_file_last_line
from util.utility import READ_LINES

CUR_ACTION_LST = [game_define.EVENT_ACTION_STAGE_HERO_FAIL,game_define.EVENT_ACTION_STAGE_HERO_WIN, game_define.EVENT_ACTION_STAGE_MOP]     # 当前行为ID列表

cur_action_log_dict = dict()    # 当前行为字典
stage_result_dict = dict()
FILE_NAME = 'HARD_STAGE_CHALLENGE'

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
            print _server_id
            last_line_num = read_file_last_line(read_file)
            print "this file last line num is: ", last_line_num
            cur_line_num = 0
            err_num = 0
            _count = 0

            # 目录
            out_put_file_path = OUT_PUT_PATH[_server_id].format(cur_date=split_date, use_path="tables")
            if not os.path.exists(out_put_file_path):
                os.makedirs(out_put_file_path)
            os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
            os.chdir(out_put_file_path)

            if log_lines:
                global cur_action_log_dict, stage_result_dict
                cur_action_log_dict = {}
                stage_result_dict = {}
                for _log_line in log_lines:
                    cur_line_num += 1
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        err_num += 1
                        continue

                    if log_dict['action'] in CUR_ACTION_LST:
                        _count += 1
                        action_id = log_dict['action']
                        action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(action_id, 'Err')
                        # 插入列表 用来输出文件
                        if action_str in cur_action_log_dict:
                            cur_action_log_dict[action_str].append(log_dict)
                        else:
                            cur_action_log_dict[action_str] = [log_dict]

                    if _count >= READ_LINES:
                        # print "READ_LINES...... cur_line_num is: ", cur_line_num
                        update_data(cur_action_log_dict, split_date)  # 到达限制数量dump一次
                        cur_action_log_dict = {}
                        _count = 0

                    elif _count > 0 and last_line_num == cur_line_num:
                        print "last update_data......   last_line is: ", cur_line_num
                        update_data(cur_action_log_dict, split_date)  # 最后一次dump
                        cur_action_log_dict = {}
                        _count = 0

                print 'err_num is: ', err_num
                #困难副本 英雄副本
                _output_HARD_STAGE_CHALLENGE()
        except:
            pass

def update_data(log_dict, datetime):
    """
    困难关卡挑战 英雄
    # 副本名称	挑战数	通过数	扫荡次数	成功率
    """
    global stage_result_dict
    normal_stage_logs = []  # 困难副本
    mop_stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_HERO_FAIL, 'Err')
    normal_stage_logs.extend(log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_HERO_WIN, 'Err')
    normal_stage_logs.extend(log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_MOP, 'Err')
    mop_stage_logs.extend(log_dict.get(action_str, []))

    # 胜利失败关卡日志字典
    stage_id_logs_dict = dict()
    for _log in normal_stage_logs:
        _stage_id = int(_log['stage_index'])
        _dat_lst = stage_id_logs_dict.get(_stage_id, [])
        _dat_lst.append(_log)
        stage_id_logs_dict[_stage_id] = _dat_lst

    # 扫荡关卡字典
    mop_stage_id_logs_dict = dict()
    for _log in mop_stage_logs:
        _stage_id = int(_log['stage_index'])
        _dat_lst = mop_stage_id_logs_dict.get(_stage_id, [])
        _dat_lst.append(_log)
        mop_stage_id_logs_dict[_stage_id] = _dat_lst

    for _stage_id, logs in stage_id_logs_dict.items():

        cur_date = datetime.strftime('%m/%d/%Y')
        # 挑战数
        challenge_count = len(logs)
        # 通过数
        challenge_win_count = len([l for l in logs if l['action'] == game_define.EVENT_ACTION_STAGE_HERO_WIN])
        # 扫荡次数
        mop_count = len(mop_stage_id_logs_dict.get(_stage_id, []))
        #胜率
        win_rate = str(round(float(challenge_win_count)/float(challenge_count), 4)*100)+'%'
        if _stage_id in stage_result_dict:

            _mop_count = mop_count + stage_result_dict[_stage_id]['mop_count']
            _challenge_win_count = challenge_win_count + stage_result_dict[_stage_id]['challenge_win_count']
            _challenge_count = challenge_count + stage_result_dict[_stage_id]['challenge_count']
            _win_rate = str(round(float(challenge_win_count)/float(challenge_count), 4)*100)+'%'

            stage_result_dict[_stage_id].update({
                'cur_date': cur_date,
                'stage_id': _stage_id,
                'challenge_count': _challenge_count,
                'challenge_win_count': _challenge_win_count,
                'mop_count': _mop_count,
                'win_rate': _win_rate
            })
        else:
            stage_result_dict[_stage_id] = {
                'cur_date': cur_date,
                'stage_id': _stage_id,
                'challenge_count': challenge_count,
                'challenge_win_count': challenge_win_count,
                'mop_count': mop_count,
                'win_rate': win_rate
            }


def _output_HARD_STAGE_CHALLENGE():
    global stage_result_dict
    result = []
    for _stage_id, values in stage_result_dict.items():
        cur_date = values['cur_date']
        _stage_id = values['stage_id']
        challenge_count = values['challenge_count']
        challenge_win_count = values['challenge_win_count']
        mop_count = values['mop_count']
        win_rate = values['win_rate']
        result.append([cur_date, _stage_id, challenge_count, challenge_win_count, mop_count, win_rate])

    #排序
    result.sort(lambda x, y: cmp(x[1], y[1]))
    #副本名称
    for each_lst in result:
        # 副本信息
        stage_config = game_config.get_stages_config(int(each_lst[1]))
        # 副本名称
        stage_name = stage_config['stageInfo']+"_"+str(stage_config['id'])
        each_lst[1] = stage_name

    out_put_file = open(FILE_NAME, 'w')
    print(FILE_NAME)
    cPickle.dump(result, out_put_file)
    out_put_file.close()


# if __name__ == "__main__":
#     start(sys.argv)

