# -*- coding:utf-8 -*-
"""
    豪华签到次数 必须在所有action 解析完后运行
"""
import time
import datetime
import sys
import pickle
import os
import stat
from util.logs_out_path_of_parse import get_parse_path

READ_FILE_FLODER = 'all_action'
READ_FILE_NMAE = 'EVENT_ACTION_RECHARGE_PLAYER'
READ_FILE_NMAE_TWO = 'EVENT_ACTION_ACTIVITY_REGIST_RECHARGE'
OUT_PUT_FILE_NAME = 'LUXURY_SIGN'
OUT_PUT_FLODER = 'tables'

def start(split_date):
    """
    读取已拆分好的日志
    """
    LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST = get_parse_path(split_date)

    for index in OUT_PUT_PATH_LST:
        try:
            print split_date, " ", index, READ_FILE_FLODER, "\n"
            # 本地打开
            read_file = OUT_PUT_PATH_LST[index].format(cur_date=split_date, use_path=READ_FILE_FLODER) + READ_FILE_NMAE
            read_file_two = OUT_PUT_PATH_LST[index].format(cur_date=split_date, use_path=READ_FILE_FLODER) + READ_FILE_NMAE_TWO
            start_time = time.time()
            new_recharge_lst = new_sign_lst = []
            if os.path.exists(read_file):
                file = open(read_file, 'r')
                new_recharge_lst = pickle.load(file)  # 获取搜索区间日志 当天充值记录 uid唯一 且  充值金额>=6元个数
                file.close()

            if os.path.exists(read_file_two):
                file_two = open(read_file_two, 'r')
                new_sign_lst = pickle.load(file_two)  # 获取搜索区间日志 豪华签到 用来统计人数
                file_two.close()

            end_time = time.time() - start_time
            print "open and load flie time is:", end_time

            table_lst = []
            if new_sign_lst and new_recharge_lst:
                start_time = time.time()
                #求得签到人数
                _sign_num = len(new_sign_lst)
                _total_lst = []
                #筛选充值金额大于6元
                for each in new_recharge_lst:
                    if each['add_rmb'] >= 6:
                        _total_lst.append(each['uid'])
                _table_lst_num = len(set(_total_lst))

                row_lst = [
                    split_date.strftime('%m/%d/%Y'),
                    _sign_num,
                    _table_lst_num,
                    division(_sign_num, _table_lst_num),
                    index,#服务器id
                ]
                table_lst.append(row_lst)

                end_time = time.time() - start_time
                print "compute flie time is:", end_time
            #目录
            floder_path = OUT_PUT_PATH_LST[index].format(cur_date=split_date, use_path=OUT_PUT_FLODER)
            if not os.path.exists(floder_path):
                os.makedirs(floder_path)
            os.chmod(floder_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

            start_time = time.time()
            # 输出豪华签到
            out_put_file = open(floder_path + OUT_PUT_FILE_NAME, 'w')
            print OUT_PUT_FILE_NAME
            pickle.dump(table_lst, out_put_file)
            out_put_file.close()
            end_time = time.time() - start_time
            print "output flie time is:", end_time
        except:
            pass

def division(num_1, num2):
    if not num2:
        return 0
    return str(round(float(num_1)/float(num2), 4)*100) + "%"

if '__main__' == __name__:
    start(sys.argv)