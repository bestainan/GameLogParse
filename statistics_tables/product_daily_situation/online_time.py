# -*- coding:utf-8 -*-

"""
在线时间统计表
"""
import datetime

from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):
    """

    """
    start_log_time = datetime.datetime.strptime(game_define.LOCAL_LOG_START_DATE, '%Y-%m-%d').date()
    # 获取搜索区间日志
    new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.get_log_lst_with_channel(new_log_lst, channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.get_log_lst_with_server(new_log_lst, server_id)

    now_date = datetime.date.today()
    # 总天数
    table_lst = []
    total_days = (search_end_date - search_start_date).days + 1
    for i in xrange(total_days):
        row_lst = []
        # 每行的日期
        row_date = search_start_date + datetime.timedelta(days=i)

        # 获取今天全部日志
        today_log_lst = daily_log_dat.get_new_log_lst_with_log(new_log_lst, start_log_time, row_date)
        # 今日游戏玩家列表
        today_login_user = daily_log_dat.get_user_uid_lst(today_log_lst)
        # 获取玩家时间段分布（5分钟）
        online_user_uid_lst = daily_log_dat.get_online_user_uid_lst(row_date, today_log_lst, 5)
        # 当前时间段Index
        now = datetime.datetime.now()
        minutes = now.hour * 60 + now.minute
        cur_online_lst_index = minutes / 5
        online_time_result = _parse_user_online_time(today_login_user, online_user_uid_lst)

        # 日期
        show_date_str= row_date.strftime('%Y-%m-%d')
        # 今日总登录用户数
        today_login_user_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid')
        # 当前实时在线
        cur_online_num = len(online_user_uid_lst[cur_online_lst_index])
        # 当日峰值在线
        today_max_online_num = _max_online_num_today(online_user_uid_lst)
        # 	5分钟以内
        online_5 = _get_online_user_num(online_time_result, 0, 5)
        # 	5-10分钟
        online_5_10 = _get_online_user_num(online_time_result, 5, 10)
        # 	10-15分钟
        online_10_15 = _get_online_user_num(online_time_result, 10, 15)
        # 	15-20分钟
        online_15_20 = _get_online_user_num(online_time_result, 15, 20)
        # 	20-25分钟
        online_20_25 = _get_online_user_num(online_time_result, 20, 25)
        # 	25-30分钟
        online_25_30 = _get_online_user_num(online_time_result, 25, 30)
        # 	30-35分钟
        online_30_35 = _get_online_user_num(online_time_result, 30, 35)
        # 	35-40分钟
        online_35_40 = _get_online_user_num(online_time_result, 35, 40)
        # 	40-45分钟
        online_40_45 = _get_online_user_num(online_time_result, 40, 45)
        # 	45-50分钟
        online_45_50 = _get_online_user_num(online_time_result, 45, 50)
        # 	50-55分钟
        online_50_55 = _get_online_user_num(online_time_result, 50, 55)
        # 	55-60分钟
        online_55_60 = _get_online_user_num(online_time_result, 55, 60)
        # 	60-90分钟
        online_60_90 = _get_online_user_num(online_time_result, 60,90)
        # 	90-120分钟
        online_90_120 = _get_online_user_num(online_time_result, 90,120)
        # 	120分钟以上
        online_120_99999 = _get_online_user_num(online_time_result, 120, 99999)

        row_lst.append(show_date_str)
        row_lst.append(today_login_user_num)
        row_lst.append(cur_online_num)
        row_lst.append(today_max_online_num)
        row_lst.append(online_5)
        row_lst.append(online_5_10)
        row_lst.append(online_10_15)
        row_lst.append(online_15_20)
        row_lst.append(online_20_25)
        row_lst.append(online_25_30)
        row_lst.append(online_30_35)
        row_lst.append(online_35_40)
        row_lst.append(online_40_45)
        row_lst.append(online_45_50)
        row_lst.append(online_50_55)
        row_lst.append(online_55_60)
        row_lst.append(online_60_90)
        row_lst.append(online_90_120)
        row_lst.append(online_120_99999)
        table_lst.append(row_lst)
    return table_lst


def _max_online_num_today(online_user_uid_lst):
    """
        当日峰值在线
    """
    num_lst = [len(uid_lst) for uid_lst in online_user_uid_lst]
    return max(num_lst)

def _parse_user_online_time(today_login_user, online_user_uid_lst):
    """
        计算玩家登录时长
        Return：
            {
                uid: online_minute,
                uid: online_minute,
                uid: online_minute
            }
    """
    online_time_result = dict()

    for _uid in today_login_user:
        # 获取区间数
        online_count = 0
        for online_uid_set in online_user_uid_lst:
            if _uid in online_uid_set:
                online_count += 1
        _uid_online_minute = online_count * 5
        online_time_result[_uid] = _uid_online_minute
    # print("online_time_result " + str(online_time_result))
    return online_time_result

def _get_online_user_num(online_time_result, start_minute, end_minute):
    """
        获取人数
    """
    user_lst = [key for key,val in online_time_result.items() if start_minute < val <= end_minute]
    return len(user_lst)