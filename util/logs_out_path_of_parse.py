#coding:utf-8
import datetime
from mysql import server_list
"""
    注：server 与 parse的此文件不一样 要各自修改!!
    注：server 与 parse的此文件不一样 要各自修改!!
    注：server 与 parse的此文件不一样 要各自修改!!
"""

def get_server_id_lst():
    """
        获取游戏服务器id列表 [10001,30001,10003,10004,10005,10006]
    """
    all_server_list = server_list.get_all_server(True)
    server_id_lst = []
    for item in all_server_list:
        server_id = int(item['id'])
        server_id_lst.append(server_id)
    return server_id_lst


def get_parse_path(split_date):
    if split_date >= datetime.date(2015, 06, 01):
        OUT_PUT_PATH_LST = {}
        LOCAL_LOG_PATH_NAME_LST = {}
        _lst = get_server_id_lst()
        for ser_id in _lst:
            OUT_PUT_PATH_LST[ser_id] = "/home/ubuntu/data/HaiMaLogParse/%s/{cur_date}/{use_path}/" % (ser_id)
            LOCAL_LOG_PATH_NAME_LST[ser_id] = "/home/ubuntu/data/HaiMaLogs/%s_{cur_date}/%s_{cur_date}_00000" % (ser_id, ser_id)

        # print 'ser_lst is: ', _lst, '\nOUT_PUT_PATH_LST is: ', OUT_PUT_PATH_LST, '\nLOCAL_LOG_PATH_NAME_LST', LOCAL_LOG_PATH_NAME_LST
        return LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST

    elif split_date <= datetime.date(2015, 05, 31):
        LOCAL_LOG_PATH_NAME_LST = {20003: "/home/ubuntu/data/FeiLiuLogs/PIKA_pc_event_{cur_date}/PIKA_pc_event_{cur_date}_00000"}
        OUT_PUT_PATH_LST = {20003: "/home/ubuntu/data/FeiLiuLogParse/fengce_data/{cur_date}/{use_path}/"}
        return LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST

LOG_PATH="/home/ubuntu/data/HaiMaLogParse/logs_check/"
