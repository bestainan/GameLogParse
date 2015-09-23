# -*- coding:utf-8 -*-

"""
玩家首冲情况
查询时间	开始时间	20100920	结束时间	20100923
渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）

注：首冲玩家数量表示每日新增首冲人数统计
日期	6月人数	30元人数	98元人数	198元人数	328元人数	488元人数	2000元人数
20101010
20101010
20101010
20101010
20101010
PS：本表人数均取角色数

"""

import datetime

from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):

    new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)

    # 获取冲列表
    first_recharge_log = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER, function=lambda log:log['old_rmb'] == 0)

    # 获取日期数
    search_days = (search_end_date - search_start_date).days

    table_result = []
    for i in xrange(search_days+1):
        row = []
        cur_date = search_start_date + datetime.timedelta(days=i)
        # 获取当天充值日志
        this_day_recharge_log = daily_log_dat.filter_logs(first_recharge_log, function=lambda log: log['log_time'].date() == cur_date)
        # 插入数据
        row.append(cur_date.strftime('%m/%d/%Y'))

        for shop_id in xrange(1, 9):
            user_num = daily_log_dat.get_set_num_with_key(this_day_recharge_log, 'uid', function=lambda log:log['shop_index'] == shop_id)
            # 插入数据
            row.append(user_num)
        table_result.append(row)

    return table_result





