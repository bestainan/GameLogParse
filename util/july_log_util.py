# -*- coding:utf-8 -*-

import datetime
import cPickle
import pickle
import os
from util import game_define
# from util.logs_out_path_of_date import May_CATCH_LOGS_DAT_LST
# from util.logs_out_path_of_date import June_CATCH_LOGS_DAT_LST
from util.logs_out_path_of_parse import July_CATCH_LOGS_DAT_LST

def read_file(action, from_date, to_date, server_id=10003, folder='all_action'):
    dat_lst = []
    if os.path.exists(July_CATCH_LOGS_DAT_LST[server_id]):
        total_days = (to_date - from_date).days + 1
        for i in xrange(total_days):
            # 每行的日期
            dat_dict = dict()
            cur_date = from_date + datetime.timedelta(days=i)
            file_path = July_CATCH_LOGS_DAT_LST[server_id].format(cur_date=cur_date, use_path=folder)+game_define.EVENT_LOG_ACTION_SQL_NAME_DICT[action]
            print file_path
            if os.path.exists(file_path):
                out_put_file = open(file_path, 'r')
                dat_dict = pickle.load(out_put_file)
                dat_lst.extend(dat_dict)
                out_put_file.close()
            # print dat_dict

    return dat_lst

def read_file_with_filename(file_name, from_date, to_date, server_id=10003, folder='all_action'):
    dat_lst = []
    total_days = (to_date - from_date).days + 1
    for i in xrange(total_days):
        dat_dict = dict()
        # 每行的日期
        cur_date = from_date + datetime.timedelta(days=i)
        file_path = July_CATCH_LOGS_DAT_LST[server_id].format(cur_date=cur_date, use_path=folder) + file_name
        print file_path
        if os.path.exists(file_path):
            out_put_file = open(file_path, 'r')
            dat_dict = pickle.load(out_put_file)
            dat_lst.extend(dat_dict)
            out_put_file.close()
        # print "ss",dat_dict

    return dat_lst

def read_file_with_filename_dict(file_name, from_date, to_date, server_id=10003, folder='all_action'):
    dat_dict_all = dict()
    total_days = (to_date - from_date).days + 1
    for i in xrange(total_days):
        # 每行的日期
        dat_dict = dict()
        cur_date = from_date + datetime.timedelta(days=i)
        file_path = July_CATCH_LOGS_DAT_LST[server_id].format(cur_date=cur_date, use_path=folder) + file_name
        print file_path
        if os.path.exists(file_path):
            out_put_file = open(file_path, 'r')
            dat_dict = pickle.load(out_put_file)
            for key, value in dat_dict.items():
                dat_dict_all.setdefault(key, []).extend(value)
            out_put_file.close()
        # print "ss",dat_dict

    return dat_dict_all


def read_file_with_user_level_state(file_name, from_date, to_date, server_id=10003, folder='tables'):
    dat_lst = []
    if os.path.exists(July_CATCH_LOGS_DAT_LST[server_id]):
        total_days = (to_date - from_date).days + 1
        for i in xrange(total_days):
            dat_dict = dict()
            # 每行的日期
            cur_date = from_date + datetime.timedelta(days=i)
            file_path = July_CATCH_LOGS_DAT_LST[server_id].format(cur_date=cur_date, use_path=folder) + file_name
            print file_path
            if os.path.exists(file_path):
                out_put_file = open(file_path, 'r')
                dat_dict = pickle.load(out_put_file)
                dat_lst.extend([dat_dict])
                out_put_file.close()
            # print dat_dict
    return dat_lst

def read_file_dict_with_filename(file_name, search_date, server_id=10003, folder='tables'):
    dat_dict = dict()
    if os.path.exists(July_CATCH_LOGS_DAT_LST[server_id]):
        file_path = July_CATCH_LOGS_DAT_LST[server_id].format(cur_date=search_date, use_path=folder) + file_name
        print file_path
        if os.path.exists(file_path):
            out_put_file = open(file_path, 'r')
            dat_dict = cPickle.load(out_put_file)
            out_put_file.close()
            # print dat_dict
    return dat_dict

#TODO:在此之上不要修改 在此之下添加自己函数
def read_action_single_file(file_name,uid,event,sreach_data, server_id=10003, folder='tables'):
    folder = file_name
    dat_lst = []
    event_id = int(event.split('-')[0])
    action_file = July_CATCH_LOGS_DAT_LST[server_id].format(cur_date=sreach_data, use_path=folder)+"{uid}/{file_name}"\
        .format(uid=uid, file_name=game_define.EVENT_LOG_ACTION_SQL_NAME_DICT[event_id])

    if os.path.exists(action_file):
        out_put_file = open(action_file, 'r')
        dat_lst = cPickle.load(out_put_file)
    return dat_lst

def walk_uid_file(from_date, to_date, server_id=10003, folder='tables'):
    # 遍历目录下所有文件
    # 'd:'+os.sep+'UID'
    # 返回文件绝对路径列表
    folder = 'ALL_USER_ACTION'
    file_list = []
    total_days = (to_date - from_date).days + 1
    for i in xrange(total_days):
        cur_date = from_date + datetime.timedelta(days=i)
        cur_date = July_CATCH_LOGS_DAT_LST[server_id].format(cur_date=cur_date, use_path=folder)

        for dirname, subdirlist, filelist in os.walk(cur_date):
            for i in filelist:
                file_list.append(dirname + os.sep + i)
    return file_list


def cpickle_load_one_day(sreach_data,file_name, server_id=10003, folder='tables'):
    dat_lst = []
    if os.path.exists(July_CATCH_LOGS_DAT_LST[server_id]):
        action_file = July_CATCH_LOGS_DAT_LST[server_id].format(cur_date=sreach_data, use_path=file_name) + file_name
        print action_file
        if os.path.exists(action_file):
            out_put_file = open(action_file, 'r')
            dat_lst = cPickle.load(out_put_file)
    return dat_lst


def read_file_double_lst(file_name, from_date, to_date, server_id=10003, folder='tables'):
    dat_lst1 = []
    dat_lst2 = []
    total_days = (to_date - from_date).days + 1
    for i in xrange(total_days):
        tmp_lst = []
        # 每行的日期
        cur_date = from_date + datetime.timedelta(days=i)
        file_path = July_CATCH_LOGS_DAT_LST[server_id].format(cur_date=cur_date, use_path=folder) + file_name
        print file_path
        if os.path.exists(file_path):
            out_put_file = open(file_path, 'r')
            tmp_lst = pickle.load(out_put_file)
            dat_lst1.extend(tmp_lst[0])
            dat_lst2.extend([tmp_lst[1]])   # 表头 只取一个最合适的
            out_put_file.close()
        # print tmp_lst

    return dat_lst1, dat_lst2
