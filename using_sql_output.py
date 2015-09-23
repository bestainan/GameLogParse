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
from util.logs_out_path_of_parse import get_parse_path
from util.logs_out_in_path import LOG_PATH

def start(split_date):
    """
        获取并拆分一天的日志
    """
    startime=datetime.datetime.now()
    print 'using_sql_output解析开始',startime  ,'\n\n'
    # split_date = datetime.date.today() - datetime.timedelta(days=1)
    # if len(args) > 1:
    #     try:
    #         split_date_str = args[1]
    #         split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
    #     except:
    #         sys.stderr.write("Err: Use daily_catch_split_log %Y-%m-%d")
    #         sys.exit(1)
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST = get_parse_path(split_date)
    for _server_id in LOCAL_LOG_PATH_NAME_LST:
        out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
        if not os.path.exists(out_put_file_path):
            os.makedirs(out_put_file_path)
        os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

        start_time = datetime.datetime.now()
        print start_time

        # 统计总表
        _output_statistics_total(out_put_file_path, split_date, _server_id)

        # 用户留存
        _output_user_retain(out_put_file_path, split_date, _server_id)

        end_time = datetime.datetime.now()
        print end_time
        print end_time-start_time
    endtime=datetime.datetime.now()
    print 'using_sql_output解析结束',endtime
    print 'using_sql_output共花费时间',(endtime-startime).seconds,'秒' ,'\n\n'


    # -----------------------------------------------------产品每日概况-----------------------------------------------
from catch_split_log.product_daily_analyse import statistics_total
from catch_split_log.product_daily_analyse import user_retain


def _output_statistics_total(out_put_file_path, split_date, _server_id):
    print("STATISTICS_TOTAL")
    result = statistics_total.get_table(split_date, channel_id=-1, server_id=_server_id)

    out_put_file = open(out_put_file_path + 'STATISTICS_TOTAL', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_user_retain(out_put_file_path, split_date, _server_id):
    print("USER_RETAIN")
    result = user_retain.get_table(split_date, channel_id=-1, server_id=_server_id)

    out_put_file = open(out_put_file_path + 'USER_RETAIN', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


if __name__ == "__main__":
    start(sys.argv)
