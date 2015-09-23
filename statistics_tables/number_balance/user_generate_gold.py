# -*- coding:utf-8 -*-

"""
金币产出消耗（部分情况根据后期修改）
开始日期	20101101	结束日期	20101101
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

日期 总计 冒险 按摩 礼包&签到 问答 邮件收取 钻石兑换 产出 消耗 剧情副本 精英副本 恶梦副本 淘金币出售 世界boss
2013/11/20	100000	100040
2013/11/21	150000	110000
2013/11/22	130000	140000
2013/11/23	90000	100000
2013/11/24	100000	90000
2013/11/25	90000	100000
2013/11/26	100000	90000
2013/11/27	90000	100000
2013/11/28	100000	90000
2013/11/29	90000	100000
2013/11/30	100000	90000

"""

import datetime

from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):
    """
        获取表格
    """
    # 获取搜索区间日志
    new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)

    search_days = (search_end_date - search_start_date).days
    table_lst = []
    head_lst = []
    head_name_lst = []
    for _day in xrange(search_days + 1):
        row_date = search_start_date + datetime.timedelta(days=_day)
        # 当天日志
        row_logs = daily_log_dat.filter_logs(new_log_lst, function=lambda log:log['log_time'].date() == row_date)
        # 获取不同事件的获取金币
        action_logs_dict = daily_log_dat.split_log_action_logs(row_logs)
        # print("action_logs_dict: "+str(action_logs_dict))
        add_gold_dict = dict()
        for _action,_logs in action_logs_dict.items():
            sum_add_gold = daily_log_dat.get_sum_int_with_key(_logs, 'add_gold')
            add_gold_dict[_action] = sum_add_gold
            if sum_add_gold and _action not in head_lst:
                head_lst.append(_action)
                head_name_lst.append(game_define.EVENT_LOG_ACTION_DICT[_action])
        # print("_day: "+str(_day)+"head_lst: "+str(head_lst))

    for _day in xrange(search_days + 1):
        row_date = search_start_date + datetime.timedelta(days=_day)
        # 当天日志
        row_logs = daily_log_dat.filter_logs(new_log_lst, function=lambda log:log['log_time'].date() == row_date)
        # 总产出金币数
        total_get_gold = daily_log_dat.get_sum_int_with_key(row_logs, 'add_gold')
        # 总消耗金币数
        total_cost_gold = daily_log_dat.get_sum_int_with_key(row_logs, 'cost_gold')
        # 获取不同事件的获取金币
        action_logs_dict = daily_log_dat.split_log_action_logs(row_logs)
        add_gold_dict = dict()
        for _action,_logs in action_logs_dict.items():
            sum_add_gold = daily_log_dat.get_sum_int_with_key(_logs, 'add_gold')
            add_gold_dict[_action] = sum_add_gold

        # 获取消耗
        row_lst = [
            row_date.strftime('%m/%d/%Y'),
            total_get_gold,
            total_cost_gold,
        ]

        for _act_id in head_lst:
            # print("_act_id: "+str(_act_id)+"add_gold_dict: "+str(add_gold_dict))
            if _act_id in add_gold_dict:
                row_lst.append(add_gold_dict.get(_act_id, 0))
            else:
                row_lst.append(0)
        # print("_day: "+str(_day)+"row_lst: "+str(row_lst))
        table_lst.append(row_lst)


    return table_lst,head_name_lst