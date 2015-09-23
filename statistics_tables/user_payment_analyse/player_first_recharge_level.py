# -*- coding:utf-8 -*-

"""
角色首次充值等级
查询日期	20101101
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

角色首次充值等级	选取用户首次充值的等级统计，时间

首次金额占比： 首次充值金额/总体充值金额
首次人数占比： 首次充值人数/总体充值人数


日期2013-11-20
等级	首次充值人数	首次充值金额	总体充值人数	总体充值金额	首次金额占比	首次人数占比
1	100
2	100
3	100
4	100
总计	2000
PS：本表人数均取角色数
"""

import datetime

from util import daily_log_dat
from util import game_define


def get_table(search_date, channel_id=-1, server_id=-1):
    """
        角色首次充值等级
    """
    start_log_time = datetime.datetime.strptime(game_define.LOCAL_LOG_START_DATE, '%Y-%m-%d').date()
    # 全部日志
    all_log_lst = daily_log_dat.get_new_log_lst(start_log_time, search_date)

    if channel_id >= 0:
        all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['server_id'] == server_id)

    # 全部充值日志
    all_recharge_log_lst = daily_log_dat.filter_logs(all_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER)
    all_first_recharge_log_lst = daily_log_dat.filter_logs(all_recharge_log_lst, function=lambda log:log['old_rmb'] == 0)


    table_lst = []
    for _table_lv in xrange(1, 121):
        # 全部当前等级充值日志
        recharge_lv_log_lst = daily_log_dat.filter_logs(all_recharge_log_lst, function=lambda log: log['level'] == _table_lv)
        # 全部当前等级充值 用户ID列表
        recharge_lv_user_lst = daily_log_dat.get_set_with_key(recharge_lv_log_lst, 'uid')
        # 全部当前等级首次充值日志
        first_recharge_lv_log_lst = daily_log_dat.filter_logs(all_first_recharge_log_lst, function=lambda log: log['level'] == _table_lv)
        # 全部当前等级首次充值 用户ID列表
        first_recharge_lv_user_lst = daily_log_dat.get_set_with_key(first_recharge_lv_log_lst, 'uid')

        # 首次充值人数
        first_recharge_user_num = len(first_recharge_lv_user_lst)
        # 首次充值总金额
        first_recharge_total_money = daily_log_dat.get_sum_int_with_key(first_recharge_lv_log_lst, "add_rmb")
        # 总体充值人数
        recharge_user_num = len(recharge_lv_user_lst)
        # 总体充值金额
        recharge_total_money = daily_log_dat.get_sum_int_with_key(recharge_lv_log_lst, "add_rmb")
        # 首次金额占比
        first_recharge_money_rate = get_first_recharge_money_rate(first_recharge_total_money,recharge_total_money)
        # 首次人数占比
        first_recharge_user_rate = get_first_recharge_user_rate(first_recharge_user_num,recharge_user_num)

        row = [_table_lv, first_recharge_user_num, first_recharge_total_money, recharge_user_num, recharge_total_money, first_recharge_money_rate, first_recharge_user_rate]
        table_lst.append(row)
    return table_lst


def get_first_recharge_money_rate(first_recharge_total_money,recharge_total_money):
    """
    # 首次金额占比
    """
    if float(recharge_total_money) <= 0:
        return 0
    return round(float(first_recharge_total_money) / float(recharge_total_money),2)


def get_first_recharge_user_rate(first_recharge_user_num,recharge_user_num):
    """
    # 首次人数占比
    """
    if float(recharge_user_num) <= 0:
        return 0
    return round(float(first_recharge_user_num) / float(recharge_user_num),2)



