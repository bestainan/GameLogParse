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
from mysql import mysql_connection
from util.logs_out_path_of_parse import get_parse_path
from action.parse_action import log_parse

def start(split_date):
    """
        获取并拆分一天的日志
    """
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST = get_parse_path(split_date)
    # 等级排行榜
    _output_rank_list(split_date, OUT_PUT_PATH_LST)


# def search(start_date_date, server_id):
#     '''
#     查询最后时间点的所有数据
#
#     '''
#     connect = mysql_connection.get_log_mysql_connection_haima()
#     sql = ("select uid,level from user_detail where last_play_time >= '%s' and last_play_time < '%s' and server_id = '%s'") %(start_date_date, start_date_date + datetime.timedelta(days=1), server_id)
#     print sql
#     return connect.query(sql)

# def search(start_date_date, server_id, path):
#     read_file_path = path[server_id].format(cur_date=start_date_date, use_path='tables')
#     read_file = open(read_file_path + 'user_detail', 'r')
#     user_detail_dict = pickle.load(read_file)

def get_table(start_date_date, server_id, path):
    row_list = {}

    read_file_path = path[server_id].format(cur_date=start_date_date, use_path='tables')
    read_file = open(read_file_path + 'USER_DETAIL', 'r')
    user_detail_dict = pickle.load(read_file)
    # all_search_day_dic = search(start_date_date, server_id, path)
    # print all_search_day_dic

    for user_uid, dic_list in user_detail_dict.items():
        if dic_list['uid'] not in row_list:
            row_list[dic_list['uid']] = dic_list['level']
        else:
            if row_list[dic_list['uid']] >= dic_list['level']:
                row_list[dic_list['uid']] = dic_list['level']

    # for dic_list in user_detail_dict:
    #     if dic_list['uid'] not in row_list:
    #         row_list[dic_list['uid']] = dic_list['level']
    #     else:
    #         if row_list[dic_list['uid']] >= dic_list['level']:
    #             row_list[dic_list['uid']] = dic_list['level']
    # print row_list
    row_list = sorted(row_list.items(),key=lambda d:d[1], reverse=True)                             #reverse实现降序排列，
    top_num = xrange(1,len(row_list))
    new_list_row = []
    for row,num in zip(row_list,top_num):
        new_list_row.append((num,row[0],row[1]))
    # print new_list_row
    return new_list_row
# search(datetime.date(2015,05,21))


#-----------------------------------等级排行榜---------------------------------------


def _output_rank_list(split_date, OUT_PUT_PATH_LST):
    for server in OUT_PUT_PATH_LST:
        try:
            out_put_file_path = OUT_PUT_PATH_LST[server].format(cur_date=split_date, use_path='tables')
            print out_put_file_path
            if not os.path.exists(out_put_file_path):
                os.makedirs(out_put_file_path)
            os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

            print("OK")
            print("LEVEL_RANK_LIST")
            result = get_table(split_date, server_id=server, path=OUT_PUT_PATH_LST)
            #out_put_file_path = OUT_PUT_PATH_LST['server'] + str(split_date) + "/tables/"    #/zgame/HaiMaLogParse/10003/
            out_put_file = open(out_put_file_path + 'LEVEL_RANK_LIST', 'w')
            pickle.dump(result, out_put_file)
            out_put_file.close()
        except:
            print "ASDLKASHDKGASDOIGASD"

#
# if __name__ == "__main__":
#     start(sys.argv)




