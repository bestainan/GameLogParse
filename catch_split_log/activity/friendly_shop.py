#coding:utf-8

import os
import stat
import datetime
import sys
import cPickle
from config import game_config
from util.save_out_put_fun import Los_Class
from util import dat_log_util
from util.logs_out_in_path import OUT_PUT_PATH_LST
from util.logs_out_path_of_parse import get_parse_path
def start(search_date):
    """
        友好商店
    """
    O, OUT_PUT_PATH_LST = get_parse_path(search_date)
    for server_id in OUT_PUT_PATH_LST.keys():
        try:
            row_list = make_action_file(search_date,server_id)
            los = Los_Class(search_date,'tables','FRIENDLY_SHOP')
            los.save_one_server(row_list,server_id)
        except:
            pass

def make_action_file(search_date,server_id):
    table_lst = []
    computle = set()
    all_uid_count = set()
    try:
        all_list = dat_log_util.read_one_day_data('EVENT_ACTION_ACTIVITY_TIME_LIMITED_SHIFT_SHOP',search_date,'all_action',server_id)[0]
    except :
        print 'EVENT_ACTION_ACTIVITY_TIME_LIMITED_SHIFT_SHOP 不存在 或为空'
    try:
        rqui = dat_log_util.read_one_day_data('EVENT_ACTION_ROLE_LOGIN',search_date,'all_action',server_id)[0]
    except :
        print 'EVENT_ACTION_ROLE_LOGIN 不存在 或为空'

    for _num in rqui:
        computle.add(_num['dev_id'])
    computle = len(computle)
    result_dict = dict()
    for _lst in all_list:
        # 循环 出物品名字
        if len(_lst['add_item_list']):
            item_tid =game_config.get_item_config(int(_lst['add_item_list'][0]))['name']
            user_uid =_lst['uid']
            all_uid_count.add(_lst['uid'])
            if item_tid in result_dict:
                result_dict[item_tid]['item_num'] += 1
                result_dict[item_tid]['user_set'].add(user_uid)
            else:
                result_dict[item_tid] = {
                    'item_num': 1,
                    'user_set': {user_uid}
                }
    for _val in result_dict.values():
        user_num = len(_val['user_set'])
        _val['user_num'] = user_num
        _val.pop('user_set')
        _val['ex_pre'] = str(round(float(_val['user_num']) / float(computle),3)) + '%'
        _val['person_pre'] = str(round(float(_val['user_num']) / float(len(all_uid_count)))) + '%'

    for key in result_dict:
        table_lst.append([key,
                          result_dict[key]['item_num'],
                          result_dict[key]['user_num'],
                          result_dict[key]['ex_pre'],
                          result_dict[key]['person_pre'],
                          ])
    return table_lst

if __name__ =='__main__':
    start(sys.argv)