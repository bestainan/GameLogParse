# -*- coding:utf-8 -*-

"""
    首次游戏时长
查询日期	20101101
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

首次游戏时长	"1.选取当日新登录用户。从第一次发送请求为开始时间，离线前最后一个请求为结束时间
2.有效用户按登录用户计算"

游戏时长	人数	占比
0-15s	100	8.33%
15-30s	100	8.33%
30s-1m	100	8.33%
1m-2m	100	8.33%
2m-3m	100	8.33%
3m-5m	100	8.33%
5m-10m	100	8.33%
10m-15m	100	8.33%
15m-30m	100	8.33%
30m-60m	100	8.33%
60m-120m	100	8.33%
大于120m	100	8.33%
总计	1200
PS：本表用户数均取角色数
"""

from util import daily_log_dat


def get_table(search_date, channel_id=-1, server_id=-1):
    """
        获取首次游戏时间长度
    """
    new_log_lst = daily_log_dat.get_new_log_lst(search_date, search_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)


    # 获取指定日期新用户
    new_use_uid_lst = daily_log_dat.get_set_with_key(new_log_lst, 'uid', function=lambda log:log['install'] == search_date)
    # 获取新玩家的所有日志
    new_user_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log:log['uid'] in new_use_uid_lst)
    user_online_time_dict = _get_online_time_dict(new_user_log_lst, new_use_uid_lst)
    # print("user_online_time_dict: "+str(user_online_time_dict))

    table_dat = []
    table_dat.append(_get_row_dat("0-15s", user_online_time_dict, 0, 15))
    table_dat.append(_get_row_dat("15-30s", user_online_time_dict, 15, 30))
    table_dat.append(_get_row_dat("30s-1m", user_online_time_dict, 30, 60))
    table_dat.append(_get_row_dat("1m-2m", user_online_time_dict, 60, 120))
    table_dat.append(_get_row_dat("2m-3m", user_online_time_dict, 120, 180))
    table_dat.append(_get_row_dat("3m-5m", user_online_time_dict, 180, 300))
    table_dat.append(_get_row_dat("5m-10m", user_online_time_dict, 300, 600))
    table_dat.append(_get_row_dat("10m-15m", user_online_time_dict, 600, 900))
    table_dat.append(_get_row_dat("15m-30m", user_online_time_dict, 900, 1800))
    table_dat.append(_get_row_dat("30m-60m", user_online_time_dict, 1800, 3600))
    table_dat.append(_get_row_dat("60m-120m", user_online_time_dict, 3600, 7200))
    table_dat.append(_get_row_dat("大于120m", user_online_time_dict, 7200))
    # print("table_dat: "+str(table_dat))
    return table_dat


def _get_online_time_dict(new_user_log_lst, new_use_uid_lst):
    """
        获取行数据
        new_user_log_lst 所有新用户日志数据
        new_use_uid_lst 所有新用户UID
    """
    user_online_time_dict = dict()
    # 遍历所有用户
    for _uid in new_use_uid_lst:
        online_time = daily_log_dat.get_user_online_time(new_user_log_lst, _uid)
        user_online_time_dict[_uid] = online_time
    return user_online_time_dict


def _get_row_dat(desc, user_online_time_dict, from_seconds, to_seconds=0):
    """
        获取行数据
    """
    user_num = 0
    total_num = len(user_online_time_dict)
    for key,time in user_online_time_dict.items():
        if to_seconds:
            if from_seconds < time <= to_seconds:
                user_num += 1
        else:
            if from_seconds < time:
                user_num += 1

    return [desc, user_num, str(_get_user_num_rate(user_num, total_num)) + "%"]

 # 获取比率
def _get_user_num_rate(user_num, total_num):
    """

    """
    if total_num <= 0:
        return 0
    return  round(float(user_num) * 100 /float(total_num),2)
