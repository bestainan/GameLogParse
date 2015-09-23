# -*- coding:utf-8 -*-

"""
    玩家金币持有（活跃用户）
开始时间	20100920	结束时间	20100923
渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）

表格说明：以下情况会根据《我爱皮卡丘》产出进行调整，具体调整情况须与cp协商
时间	持有数量	玩家数量	活跃玩家总数
20101919
20101919
20101919
PS：本表玩家数量均取角色数
"""

import datetime

from util import daily_log_dat


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1, player_min_level=1,
              player_max_level=999):
    # 获取搜索区间日志
    new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)

    # 适配等级
    new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: player_min_level <= x['level'] <= player_max_level)

    # 获取用户表
    # uid_lst = daily_log_dat.get_set_with_key(new_log_lst, 'uid')

    search_days = (search_end_date - search_start_date).days

    table_lst = []
    for _day in xrange(search_days + 1):
        row_date = search_start_date + datetime.timedelta(days=_day)

        row_logs = daily_log_dat.filter_logs(new_log_lst, function=lambda log: log['log_time'].date() == row_date)
        #拆分玩家金币日志
        user_key_dict = daily_log_dat.split_log_users_last_stone(row_logs)

        # 获取玩家总金币数
        total_stone = sum([val for val in user_key_dict.values()])
        total_user = len(user_key_dict)
        active_user = daily_log_dat.get_set_num_with_key(row_logs, 'uid', function=lambda log:log['install'] != row_date)
        row_lst = [row_date.strftime('%m/%d/%Y'), total_stone, total_user, active_user]
        table_lst.append(row_lst)

    return table_lst



