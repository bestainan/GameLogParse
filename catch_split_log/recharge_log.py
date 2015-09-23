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
import urllib2
import time
from util import game_define
from action.parse_action import log_parse

# 飞流mysql 飞流日志服务器地址
# CATCH_SQL_HOST = "556418a8f30f9.sh.cdb.myqcloud.com:6080"
# LOG_SERVER_PATH = "http://115.159.77.250:8086/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"

# ZGAME 海马日志服务器地址
CATCH_SQL_HOST = "555ff729cffb0.sh.cdb.myqcloud.com:6200"
LOG_SERVER_PATH = "http://115.159.69.65:8086/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"

CATCH_SQL_PAS = "Zgamecn6"

LOCAL_LOG_START_DATE = '2015-05-21'
#输出文件目录
OUT_PUT_PATH = "/opt/HaiMaGameLogParse/data/"
# OUT_PUT_PATH = "/opt/GameLogParse/data/"
# OUT_PUT_PATH = os.getcwd() + "/data/"

#拆分文件目录
LOCAL_LOG_PATH_NAME = "/data/HaiMaLogs/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"
# LOCAL_LOG_PATH_NAME = "/opt/HaiMaGameLogParse/log_tmp/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"
# LOCAL_LOG_PATH_NAME = "/opt/GameLogParse/log_tmp/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"
# LOCAL_LOG_PATH = os.getcwd() + "/log_tmp/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"

CUR_ACTION_LST = [game_define.EVENT_ACTION_RECHARGE_PLAYER]#外部 充值id

def start(args):
    """
        获取并拆分一天的日志
    """
    start_time = time.time()
    # split_date = datetime.date.today() - datetime.timedelta(days=1)
    split_date = datetime.datetime.strptime("2015-06-05", "%Y-%m-%d").date()
    if len(args) > 1:
        try:
            split_date_str = args[1]
            split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        except:
            sys.stderr.write("Err: Use daily_catch_split_log %Y-%m-%d")
            sys.exit(1)

    # 本地打开
    read_file = LOCAL_LOG_PATH_NAME % (split_date, split_date)
    log_lines = open(read_file, 'r')
    print(split_date)

    if log_lines:
        result = []
        for _log_line in log_lines:
            _log_line = _log_line.strip()
            log_dict = log_parse(_log_line)

            if log_dict['action'] in CUR_ACTION_LST:
                result.append(log_dict)

        os.chmod(OUT_PUT_PATH, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
        out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
        if not os.path.exists(out_put_file_path):
            os.makedirs(out_put_file_path)
        #外部充值数据
        out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
        out_put_file = open(out_put_file_path + 'EVENT_ACTION_RECHARGE_PLAYER', 'w')
        pickle.dump(result, out_put_file)
        out_put_file.close()

        end_time = time.time() - start_time
        print "use time is :", end_time

if __name__ == "__main__":
    start(sys.argv)

# start(['2015-06-05', '2015-06-05'])