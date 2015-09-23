# -*- coding:utf-8 -*-

"""
用户构成
开始时间	20101101	结束时间	20101103
游戏分区	所有	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

日期	活跃用户	用户流失	回流用户	注：回流用户统计方式需与cp商讨
2010/9/19	2970	20	20
2010/9/20	2971	30	30
总计	5941	50	50
PS：本表用户数均取角色数
"""

import os
import stat
import pickle
import datetime
from util import daily_log_dat
from util import mysql_util
from util.logs_out_path_of_parse import get_parse_path


def start(split_date):
    LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST = get_parse_path(split_date)
    for _server_id in OUT_PUT_PATH_LST:
        try:
            out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
            if not os.path.exists(out_put_file_path):
                os.makedirs(out_put_file_path)
            os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

            # 输出文件
            _output_user_structure(out_put_file_path, split_date, _server_id)
        except Exception, e:
            print("USER_STRUCTURE 解析错误 "), e
            pass


def _output_user_structure(out_put_file_path, split_date, _server_id):
    print("USER_STRUCTURE"), _server_id
    result = get_table(split_date, _server_id)

    out_put_file = open(out_put_file_path + 'USER_STRUCTURE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def get_table(search_date, server_id):

    # 搜索日期到今天的所有日志
    retained_day = search_date - datetime.timedelta(days=4)
    all_login_lst = []
    total_days = (search_date - retained_day).days+1
    for i in xrange(total_days):
        search_date = retained_day + datetime.timedelta(days=i)
        date_str = "_"+search_date.strftime('%Y%m%d')
        login_lst = mysql_util.get_role_action_lst('EVENT_ACTION_ROLE_LOGIN'+str(date_str), search_date, search_date, -1, server_id, None, None)
        all_login_lst.extend(login_lst)

    table_result = []
    cur_date = search_date
    # 今日全部日志
    today_login_lst = daily_log_dat.get_new_log_lst_with_log(all_login_lst, cur_date, cur_date)
    # 获取登录日志列表
    today_login_uid_lst = daily_log_dat.get_set_with_key(today_login_lst, 'uid')

    today_new_user_login_lst = daily_log_dat.filter_logs(today_login_lst, function=lambda log: log['install'] == cur_date)
    today_new_user_uid_num = daily_log_dat.get_set_num_with_key(today_new_user_login_lst, 'uid')
    # 登录用户数
    today_login_uid_num = len(today_login_uid_lst)
    # 活跃用户数
    today_active_uid_num = today_new_user_uid_num

    # 流失用户（3天内没登录）
    today_lost_uid_num = len(daily_log_dat.get_lost_user_set(all_login_lst, cur_date))
    # 回流用户（3天内没登录 但今天登录）
    login_back_num = len(daily_log_dat.get_lost_back_user_set(all_login_lst, cur_date))

    row = [cur_date.strftime("%m/%d/%Y"), today_login_uid_num, today_active_uid_num, today_lost_uid_num, login_back_num]
    table_result.append(row)

    return table_result
