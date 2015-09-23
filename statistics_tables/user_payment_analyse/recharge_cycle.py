# -*- coding:utf-8 -*-

"""
    充值周期
查询日期	20101101 -
分区查询	总/1区/2区	（默认总数、下拉菜单手动选择区服）
渠道标示	UC/91	（默认总数、下拉菜单手动选择渠道）

充值周期	角色以注册时间开始，首次充值时间结束的周期

日期2013-11-20
天数	首次充值人数	首次充值金额	总体充值人数	总体充值金额	首次金额占比	首次人数占比
1日	100
2日	100
3日	100
4日	100
5日	100
6日	100
7日	100
15日	100
30日	100
30日以上	100
总计	100
PS：本表人数均取角色数

"""

import datetime

from util import daily_log_dat
from util import game_define


def get_table(search_from_date, search_to_date, channel_id=-1, server_id=-1):
    """
      充值周期
    """
    # 获取指定日期 所有日志
    all_log_lst = daily_log_dat.get_new_log_lst(search_from_date, search_to_date)

    if channel_id >= 0:
        all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['server_id'] == server_id)

    # 获取区间内所有新安装用户
    new_install_uid_lst = daily_log_dat.get_set_with_key(all_log_lst,'uid', function= lambda log:search_from_date <= log['install'] <= search_to_date)
    # 获取到今天为止的日志
    all_log_lst = daily_log_dat.get_new_log_lst(search_from_date, datetime.date.today())

    # 用指定日期新用户 获取所有充值日志
    all_recharge_log = daily_log_dat.filter_logs(all_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER, function=lambda log: log['uid'] in new_install_uid_lst)
    # 获取全部首冲日志
    all_first_recharge_log = daily_log_dat.filter_logs(all_recharge_log, function=lambda log: log['old_rmb'] == 0)

    table_result = []
    table_result.append(_get_day_distance_result('1日',all_recharge_log, all_first_recharge_log, 0, 1))
    table_result.append(_get_day_distance_result('2日',all_recharge_log, all_first_recharge_log, 1, 2))
    table_result.append(_get_day_distance_result('3日',all_recharge_log, all_first_recharge_log, 2, 3))
    table_result.append(_get_day_distance_result('4日',all_recharge_log, all_first_recharge_log, 3, 4))
    table_result.append(_get_day_distance_result('5日',all_recharge_log, all_first_recharge_log, 4, 5))
    table_result.append(_get_day_distance_result('6日',all_recharge_log, all_first_recharge_log, 5, 6))
    table_result.append(_get_day_distance_result('7日',all_recharge_log, all_first_recharge_log, 6, 7))
    table_result.append(_get_day_distance_result('7-15日',all_recharge_log, all_first_recharge_log, 7, 15))
    table_result.append(_get_day_distance_result('15-30日',all_recharge_log, all_first_recharge_log, 15, 30))
    table_result.append(_get_day_distance_result('30日以上',all_recharge_log, all_first_recharge_log, 30))

    return table_result


def _get_day_distance_result(desc, recharge_log, first_recharge_log, from_day, to_day=99999):
    """
        获取行数据
    """
    #获取 第N天就充值的玩家UID列表

    days_recharge_log_lst = daily_log_dat.filter_logs(recharge_log, function=lambda log: from_day <= (log['log_time'].date() - log['install']).days < to_day)
    days_first_recharge_log_lst = daily_log_dat.filter_logs(first_recharge_log, function=lambda log: from_day <= (log['log_time'].date() - log['install']).days < to_day)
    # 获取人数
    total_user_num = daily_log_dat.get_set_num_with_key(days_recharge_log_lst, 'uid')
    first_total_user_num = daily_log_dat.get_set_num_with_key(days_first_recharge_log_lst, 'uid')
    # 获取充值总金额
    total_money = daily_log_dat.get_sum_int_with_key(days_recharge_log_lst, 'add_rmb')
    first_total_money = daily_log_dat.get_sum_int_with_key(days_first_recharge_log_lst, 'add_rmb')

    # 获取比率
    money_rate = _get_money_rate(first_total_money, total_money)
    user_rate = _get_user_rate(first_total_user_num, total_user_num)
    return [desc, first_total_user_num, first_total_money, total_user_num, total_money, money_rate, user_rate]


  # 获取比率
def _get_money_rate(first_total_money, total_money):
    """

    """
    if total_money <= 0:
        return 0
    return round(float(first_total_money) / float(total_money), 2)


  # 获取比率
def _get_user_rate(first_total_user_num, total_user_num):
    """

    """
    if total_user_num <= 0:
        return 0
    return round(float(first_total_user_num) / float(total_user_num), 2)















