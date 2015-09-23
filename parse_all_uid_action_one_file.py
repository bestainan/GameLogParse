#coding:utf-8
import cPickle
import datetime
import sys
import os
import time
from util import game_define
from util.logs_out_path_of_parse import get_parse_path
from action.parse_action import log_parse

CATCH_SQL_PAS = "Zgamecn6"
LOCAL_LOG_START_DATE = '2015-05-21'
EQUIP_ACTION_LST = ['add_equip_list', 'remove_equip_list']

# os.chmod(OUT_PUT_PATH, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)


def read_file(path):
    f = open(path,'r')
    line = f.readline()
    while line:
        yield line
        line = f.readline()
    f.close()

def start_parse(split_date):
    """
        获取并拆分一天的日志
    """
    LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST = get_parse_path(split_date)
    for server_id in LOCAL_LOG_PATH_NAME_LST.keys():
        print server_id

        try:
            url_path = LOCAL_LOG_PATH_NAME_LST[server_id].format(cur_date=split_date,)
            url = read_file(url_path)
            UID_FILE_NAME = OUT_PUT_PATH_LST[server_id].format(cur_date=str(split_date),
                                                           use_path='UID_ACTION_PATH')
            os.mkdir(UID_FILE_NAME)#主文件目录

            for _log_line in url:

                _log_line = _log_line.strip()
                log_dict = log_parse(_log_line)
                if log_dict:
                    insert_gm_logs_by_uid(log_dict,UID_FILE_NAME)
        except:
            pass

def insert_gm_logs_by_uid(log_line_dict,path):
    try:
        os.mkdir(path+str(log_line_dict['uid']))
    except:
        pass
    with open(path+str(log_line_dict['uid']) + os.sep +str(game_define.EVENT_LOG_ACTION_SQL_NAME_DICT[log_line_dict['action']]),'a+') as f:
        cPickle.dump(log_line_dict, f)


if __name__ == '__main__':
    a = time.time()
    if len(sys.argv) > 1:
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start_parse(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start_parse(split_date)
    print 'all_uid_action_one_file use time is: ', time.time() - a
