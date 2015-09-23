# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import pickle
import os
import stat
import datetime
from util.logs_out_path_of_parse import get_parse_path
"""对用户好友的申请数量，通过数量进行统计
"""

def start(split_date):
    """
        获取并拆分一天的日志
    """
    # split_date = datetime.datetime.strptime("2015-06-05", "%Y-%m-%d").date()
    #split_date = datetime.date.today() - datetime.timedelta(days=1)
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST=get_parse_path(split_date)
    for log_path in OUT_PUT_PATH_LST.values():
        if os.path.exists(log_path.format(cur_date=split_date,use_path = 'all_action')):
            os.chmod(log_path.format(cur_date=split_date,use_path = 'all_action'), stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
            path=log_path.format(cur_date=split_date,use_path = 'all_action')+'EVENT_ACTION_BUDDY_APPLY_PLAYER'
            #print path
            f=pickle.load(open(path,'r'))
            apply_count =len(f)
            path=log_path.format(cur_date=split_date,use_path = 'all_action')+'EVENT_ACTION_BUDDY_ADD_PLAYER'
            #print path
            f=pickle.load(open(path,'r'))
            add_count = len(f)
            try:
                success_rate = str(round(float(add_count)/float(apply_count)*10000)/100)+'%'
            except:
                success_rate= '0%'
            dat_lst = [str(split_date), apply_count, add_count, success_rate]

            try:
                os.mkdir(log_path+"%s/tables/" % (split_date))
            except:
                pass
            if not os.path.exists(log_path.format(cur_date=split_date,use_path = 'all_action')):
                os.mkdir(log_path.format(cur_date=split_date,use_path = 'all_action'))
            OUT_PUT_FILE_PATH = log_path.format(cur_date=split_date,use_path = 'tables')+'FRIEND_COUNT'
            f=open(OUT_PUT_FILE_PATH, 'w')
            pickle.dump(dat_lst, f)

