#coding:utf-8
import pickle
import os
from util.logs_out_path_of_parse import get_parse_path


def walk_uid_file(search_data,server_id,use_path):
    # 遍历目录下所有文件
    # 'd:'+os.sep+'UID'
    # 返回文件绝对路径列表
    # 10003/2015-05-31/all_action/file_name

    LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST = get_parse_path(search_data)
    file_list = []
    cur_date = OUT_PUT_PATH_LST[server_id].format(
        cur_date=search_data,
        use_path=use_path,
    )
    for dirname, subdirlist, filelist in os.walk(cur_date):
        for i in filelist:
            file_list.append(dirname + i)
    return file_list

#正在改路径 todo
def read_one_day_data(file_name,search_date,use_path,server_id):

    dat_lst = []
    LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST = get_parse_path(search_date)
    CATCH_LOGS_DAT = OUT_PUT_PATH_LST[server_id].format(cur_date=search_date,use_path=use_path) + file_name
    print CATCH_LOGS_DAT
    if os.path.exists(CATCH_LOGS_DAT):
        with open(CATCH_LOGS_DAT,'r') as f:
            dat_dict = pickle.load(f)
            dat_lst.extend([dat_dict])
    return dat_lst


