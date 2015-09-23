#coding:utf-8

import datetime
import sys
import os
import stat
import cPickle
import pickle
from util import dat_log_util
from util.save_out_put_fun import Los_Class
from util.logs_out_path_of_parse import get_server_id_lst


def start(search_date):
    """
        消费排行
    """
    print(search_date)
    los = Los_Class(search_date,'tables','EXPENSE_SORT')

    for server_id in get_server_id_lst():
        try:
            list_row_to_be_return = make_action_file(search_date,server_id)
            los.save_one_server(list_row_to_be_return,server_id)
        except:
            pass

def make_action_file(sreach_data,server_id):
    #遍历所有玩家文件夹
    #查询事件文件中是否有关键字cost_stone（消耗钻石）
    row_list = dict()
    action_file_abs_path = dat_log_util.walk_uid_file(sreach_data,server_id,'all_action')
    for file in action_file_abs_path:
        if 'EVENT_ACTION' in file:
            with open(file,'r') as f:
                action_file = pickle.load(f)
                for action in action_file:
                    if 'cost_stone' in action.keys() and action['cost_stone'] != 0:
                        if action['uid'] not in row_list:
                            row_list[action['uid']] = action['cost_stone']
                        else:
                            row_list[action['uid']] += action['cost_stone']

    table_lst = []
    row_list = sorted(row_list.items(), key=lambda d: d[1], reverse=True)
    top_num = xrange(1, len(row_list))
    for row,num in zip(row_list, top_num):
        row_list_append = ((num, row[0], row[1]))
        table_lst.append(row_list_append)
    return table_lst


if __name__ == '__main__':
    if len(sys.argv) > 1:
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start(split_date)













