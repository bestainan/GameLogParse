#coding:utf-8
import cPickle
import datetime
import sys
from util.logs_out_path_of_parse import get_parse_path
from util.save_out_put_fun import Los_Class
first, second, third, fourth= 0,0,0,0
# 飞流mysql 飞流日志服务器地址
CATCH_SQL_PAS = "Zgamecn6"
LOCAL_LOG_START_DATE = '2015-05-21'
EQUIP_ACTION_LST = ['add_equip_list', 'remove_equip_list']
action_equip_lst = []
from mysql import mysql_connection

def start(search_date):
    """
    充值排行
    """


    LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST = get_parse_path(search_date)

    print(search_date)
    for server_id in OUT_PUT_PATH_LST.keys():

        try:

            list_row_to_be_return = make_action_file(search_date,server_id)
            los = Los_Class(search_date,'tables','SORT_RMB')
            los.save_one_server(list_row_to_be_return,server_id)
        except:
            pass

def search(search_data,server_id):
    '''
    查询时间段内的所有数据

    '''
    connect = mysql_connection.get_log_mysql_connection_haima()
    sql = r"select uid,add_rmb from EVENT_ACTION_RECHARGE_PLAYER_{search_data_no} where log_time > date'{search_data}' and log_time < date_add('{search_data}', interval 1 day) and server_id = {server_id};"\
        .format(
        search_data = search_data,
        server_id = server_id,
        search_data_no = str(search_data).replace('-','')
    )
    return connect.query(sql)

def make_action_file(search_date,server_id):
    row_list = {}
    one_day_dic = search(search_date,server_id)
    for dic_list in one_day_dic:
        if dic_list['uid'] not in row_list:
            row_list[dic_list['uid']] = dic_list['add_rmb']
        else:
            row_list[dic_list['uid']] += dic_list['add_rmb']

    row_list = sorted(row_list.items(),key = lambda d:d[1], reverse=True)
    top_num = range(1,len(row_list)+1)
    new_list_row = []
    for row,num in zip(row_list,top_num):
        new_list_row.append([num,row[0],row[1]])
    return new_list_row

if __name__ == '__main__':
    if len(sys.argv) > 1:
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start(split_date)










