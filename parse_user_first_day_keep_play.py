# -*- coding:utf-8 -*-

"""
    解析所有列表
"""
import cPickle
import datetime
import sys
import os
import time
from util.logs_out_path_of_parse import get_parse_path
from util.dat_log_util import read_one_day_data
from util.save_out_put_fun import Los_Class
def start_parse(split_date):
    """
        获取并拆分一天的日志
    """
    LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST = get_parse_path(split_date)
    los = Los_Class(split_date,'tables','USER_FIRST_DAY_KEEP_PLAY')
    for _server_id in OUT_PUT_PATH_LST.keys():
        try:

            list_row_to_be_return = make_file(split_date,_server_id)
            los.save_one_server(list_row_to_be_return,_server_id)
        except:
            pass



def make_file(split_date,server_id):
    new_log_lst = read_one_day_data("USER_DETAIL",split_date,'tables',server_id,)


    user_num_dict = dict()
    lost_user_num_dict = dict()
    for dat in new_log_lst:
        for value in dat.values():
            cur_lv = value['level']
            if split_date == value['install']:
                user_num_dict[cur_lv] = user_num_dict.get(cur_lv, 0) + 1

    next_split_date = split_date+ datetime.timedelta(days=1)
    next_day_log_lst = read_one_day_data("USER_DETAIL",next_split_date,'tables',server_id,)
    #这里再查第二天的new_log_lst
    for dat in next_day_log_lst:
        for value in dat.values():
            cur_lv = value['level']
            if split_date == value['install'] and value['last_play_time'].date() == value['install']:
                lost_user_num_dict[cur_lv] = lost_user_num_dict.get(cur_lv, 0) + 1


    num_total = 0
    for _table_lv in xrange(1, 121):
        num_total += user_num_dict.get(_table_lv, 0)

    # 遍历全部等级
    table_row_lst = []
    for _table_lv in xrange(1, 121):
        # 停留人数
        user_num = user_num_dict.get(_table_lv, 0)
        # 流失人数
        lost_num = lost_user_num_dict.get(int(_table_lv), 0)
        # 留存人数
        stand_num = user_num - lost_num
        # 等级比率
        level_rate = str(_get_rate(user_num, num_total)* 100) + "%"
        # 留存人数比率
        level_lost_rate = str(_get_rate(stand_num , num_total) * 100) + "%"
        # 等级	停留人数	留存人数比率	等级流存率
        content = [_table_lv, user_num, level_rate, level_lost_rate]
        table_row_lst.append(content)
    return table_row_lst


def _get_rate(lost_num, arrive_num):
    if arrive_num <= 0:
        return 0

    return round(float(lost_num)/float(arrive_num), 2)
