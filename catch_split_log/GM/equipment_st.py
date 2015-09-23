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
import pickle
import os
import datetime
from util import game_define
# from util.logs_out_path_of_date import get_parse_path
# from util.logs_out_in_path import OUT_PUT_PATH_LST
from util.logs_out_path_of_parse import get_parse_path
# from catch_split_log.GM import equipment_strengthening_record_sj


def start(split_date):
    """
        获取并拆分一天的日志
    """

    O, OUT_PUT_PATH_LST = get_parse_path(split_date)
    # 装备强化记录
    _output_equipment_strengthening_record(split_date, OUT_PUT_PATH_LST)



#-----------------------------------装备强化记录----------------------------------------
def _output_equipment_strengthening_record(split_date, OUT_PUT_PATH_LST):
    #OUT_PUT_PATH_LST=get_parse_path(split_date)
    for server1 in OUT_PUT_PATH_LST:
        try:
            out_put_file_path = OUT_PUT_PATH_LST[server1].format(cur_date=split_date, use_path='tables')     # 存储文件路径
            if not os.path.exists(out_put_file_path):                                  # 如果path存在返回 True，如果path不存在  返回False
                os.makedirs(out_put_file_path)                                              # 可以生成多层递归目录
            os.chmod(out_put_file_path,stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)  #对于拥有者执行的权限     os.chmod:改变文件权限模式

            print("EQUIPMENT_ST_RECORD")
            out_put_file_path1 = OUT_PUT_PATH_LST[server1].format(cur_date=split_date, use_path='all_action')
            result = get_table(split_date,out_put_file_path1)

        # out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
            out_put_file = open(out_put_file_path + 'EQUIPMENT_ST_RECORD', 'w')                 # 写文本文件，open后边必须根colse   output = open（’data‘， ’w‘）
            print out_put_file
            pickle.dump(result, out_put_file)          # pickle.dump(obj,file,[protocol])。将对象obj，保存到file文件中。。。     即将result输出的数据，保存在out_put_file就是EQUIPMENT_ST_RECORD里面
            out_put_file.close()                       # 输出文件。。。这里的close 是和open对应的，不可丢
        except:
            pass


    #open('D:\\132.txt' 'r')  表示只读这个文件。\  是转义符，只有将其转义才能得到符号‘\'.    必须保证文件存在
    #open('D:\\123.txt' 'w')  表示写入这个文件。  以此类推。   写目录要至少保证存取路径存在，文件可以不存在
    #open('123.txt' 'r')      表示只读文件，，但是因为没有添加路径，所以会读取当前python运行的当前目录下寻找该文件名的文件。        必须保证文件存在


def read_file_with_filename(file_name, from_date, path):
    dat_lst = []
    if os.path.exists(path):                                  #判断，如果path存在则返回True。如果不存在就返回False。

        # for i in xrange(total_days):
        dat_dict = dict()
        # 每行的日期
        cur_date = from_date
        file_path = path + file_name
        if os.path.exists(path):
            out_put_file = open(file_path, 'r')
            dat_dict = pickle.load(out_put_file)
            dat_lst.extend(dat_dict)
            out_put_file.close()
        # print dat_dict

    return dat_lst


def get_table(start_date,path):

    row_lst = []
    new_log_lst = read_file_with_filename("EVENT_ACTION_EQUIP_LEVEL_UP_MULTI", start_date, path)
    new_log_lst1 = read_file_with_filename("EVENT_ACTION_EQUIP_LEVEL_UP", start_date, path)
    _lst = []
    _lst.extend(new_log_lst)
    _lst.extend(new_log_lst1)

    for each_item in _lst:
        log_time = each_item['log_time'].strftime("%Y-%m-%d %H:%M:%S")
        uid = each_item['uid']
        action_name = game_define.EVENT_LOG_ACTION_DICT[each_item['action']]
        cost_gold = each_item['cost_gold']
        cost_item_list = each_item['cost_item_list'][1]
        row_list_append = [log_time,uid,action_name,cost_gold,cost_item_list]
        row_lst.append(row_list_append)

    return row_lst

if __name__ == '__main__':
    if len(sys.argv) > 1:
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start(split_date)