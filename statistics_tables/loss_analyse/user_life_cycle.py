# -*- coding:utf-8 -*-


"""
生命周期

查询日期	20101101	结束日期	20101101

分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

生命周期
1.计算用户经过多久的游戏时间（天）流失
2.20101101时间表示改日新增登录用户数"

日期	次日流失	2-3日流失	4-7日流失	8-14日流失	15-30日流失	31-90日流失	90-180日流失	181-1年流失	1年+
20101101	2970	20	20
20101102	2971	30	30
20101103	5941	50	50
PS：本表用户数均取角色数

"""

import datetime

from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):

    # 搜索日期到今天的所有日志
    retained_day = search_start_date - datetime.timedelta(days=3)
    all_log_lst = daily_log_dat.get_new_log_lst(retained_day, search_end_date)

    if channel_id >= 0:
        all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['server_id'] == server_id)

    # 获取全部登录日志
    all_login_log_lst = daily_log_dat.filter_logs(all_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN)
    # 获取玩家游戏天数字典
    user_play_day_dict = daily_log_dat.split_log_users_play_days(all_login_log_lst)
    # 展示日期数
    show_days = (search_end_date - search_start_date).days

    table_result = []
    for i in xrange(show_days+1):
        row_date = search_start_date + datetime.timedelta(days=i)
        # 获取所有流失用户
        lost_user_lst = daily_log_dat.get_lost_user_set(all_login_log_lst, row_date)

        row = _get_row(row_date, user_play_day_dict, lost_user_lst)
        table_result.append(row)
    return table_result


def _get_row(lost_end_date, player_play_day_dict, lost_user_lst):
    """
        日期	次日流失	2-3日流失	4-7日流失	8-14日流失	15-30日流失	31-90日流失	90-180日流失	181-1年流失	1年+
    """
    row = [
        lost_end_date.strftime("%m/%d/%Y"),
        _get_days_user_num(player_play_day_dict, lost_user_lst, 0, 1),
        _get_days_user_num(player_play_day_dict, lost_user_lst, 2, 3),
        _get_days_user_num(player_play_day_dict, lost_user_lst, 4, 7),
        _get_days_user_num(player_play_day_dict, lost_user_lst, 8, 14),
        _get_days_user_num(player_play_day_dict, lost_user_lst, 15, 30),
        _get_days_user_num(player_play_day_dict, lost_user_lst, 31, 90),
        _get_days_user_num(player_play_day_dict, lost_user_lst, 91, 180),
        _get_days_user_num(player_play_day_dict, lost_user_lst, 181, 360),
        _get_days_user_num(player_play_day_dict, lost_user_lst, 361, 9999999),
    ]

    return row


def _get_days_user_num(lost_player_player_day_dict, lost_user_lst, from_day, end_day):
    """
        获取指定天数用户数
    """
    num = 0
    for key,val in lost_player_player_day_dict.items():
        if key in lost_user_lst and from_day <= val <= end_day:
            num += 1
    return num







