# -*- coding:utf-8 -*-


"""
活动模块分析

日期	参与人数	总钓鱼次数	点击钓鱼界面次数	到达要求人数	参与率
2013/11/21
2013/11/22
2013/11/23
…

"""

import datetime


from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1, server_id=-1):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # 获取搜索区间日志
    new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)
    #获取符合条件的日志
    if register_start_date and register_end_date:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: register_start_date <= log['install'] <= register_end_date)

    # 截取日志到 副本事件
    stage_action_lst = [
        game_define.EVENT_ACTION_FISHING_ONCE,
        game_define.EVENT_ACTION_FISHING_LOOP,
    ]

    table_lst = []
    search_days = (search_end_date - search_start_date).days+1
    for _day in xrange(search_days):
        row_date = search_start_date + datetime.timedelta(days=_day)
        # print("-------------------" + str(row_date) + "-------------------")
        # 获取当天的日志
        row_logs = daily_log_dat.filter_logs(new_log_lst, function=lambda log: log['log_time'].date() == row_date)
        # 过滤出钓鱼日志
        stage_action_log_lst = daily_log_dat.filter_logs(row_logs,
                                                     function=lambda log: log['action'] in stage_action_lst)
        # print("钓鱼日志 " + str(stage_action_log_lst))
        # 日期
        row_date_str = row_date.strftime('%m/%d/%Y')
        # 参与人数
        join_user_num = daily_log_dat.get_set_num_with_key(stage_action_log_lst, 'uid')
        # 总钓鱼次数
        total_finish_num = daily_log_dat.get_sum_int_with_key(stage_action_log_lst, 'cost_fishing_count')
        # 行日期之前的 日志
        until_row_day_logs = daily_log_dat.filter_logs(new_log_lst, function=lambda log: log['log_time'].date() <= row_date)
        # 到达要求人数
        can_join_user_num = daily_log_dat.get_set_num_with_key(until_row_day_logs, 'uid', function=lambda log:log['level'] >= 15)
        # 参与率
        join_rate = 0
        if can_join_user_num:
            join_rate = round(float(join_user_num)/float(can_join_user_num), 2) * 100

        row_lst = [
            row_date_str,  # 日期
            join_user_num,  # 参与人数
            total_finish_num, # 总钓鱼次数
            can_join_user_num, # 到达要求人数
            str(join_rate) + "%" # 参与率
        ]
        table_lst.append(row_lst)
    return table_lst