# -*- coding:utf-8 -*-

"""
新增K日收益统计
注册时间	2010.9.19	结束时间	2010.9.26
游戏分区	所有	（可以查单区，默认所有区）
渠道名称	所有	（可以查单独的渠道，默认所有渠道）

日期	新增设备	第1天	第2天	第3天	第4天	第5天	第6天	第7天	第15日	第30日	30日以上
2010/9/19	124	3000	3000	3000	3000	3000	3000	3000
2010/9/20	125	3000	3000	3000	3000	3000	3000	3000
2010/9/21	126	3000	3000	3000	3000	3000	3000
2010/9/22	127	3000	3000	3000	3000	3000
2010/9/23	128	3000	3000	3000	3000
2010/9/24	129	3000	3000	3000
2010/9/25	130	3000	3000
2010/9/26	131	3000
*指定日期内的注册用户，在注册以后的K日内收益的累计值
*第1天为注册当天、之后天数自然延展
PS：本表人数均取角色数
"""

import datetime

from util import daily_log_dat
from util import game_define


def get_table(register_star_date, register_end_date, channel_id=-1, server_id=-1):
    """
        新增K日收益统计
    """
    # 搜索日期到今天的所有日志
    all_log_lst = daily_log_dat.get_new_log_lst(register_star_date, datetime.date.today())

    if channel_id >= 0:
        all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['server_id'] == server_id)

    # 全部充值日志
    all_recharge_log_lst = daily_log_dat.filter_logs(all_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER)

    row_days = (register_end_date - register_star_date).days

    table_lst = []
    for _day in xrange(row_days):
        row_date = register_star_date + datetime.timedelta(days=_day)
        # 获取新用户
        row_new_user_uid_lst = daily_log_dat.get_set_with_key(all_log_lst, 'uid',action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['install'] == row_date)
        # 获取新增设备
        new_device_num = daily_log_dat.get_set_num_with_key(all_log_lst, 'dev_id',action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['install'] == row_date)
        # 获取充值总额
        recharge_date = row_date + datetime.timedelta(days=1)
        total_rmb_1 = daily_log_dat.get_sum_int_with_key(all_recharge_log_lst, 'add_rmb', function=lambda log:log['log_time'].date() == recharge_date and log['uid'] in row_new_user_uid_lst)
        recharge_date = row_date + datetime.timedelta(days=2)
        total_rmb_2 = daily_log_dat.get_sum_int_with_key(all_recharge_log_lst, 'add_rmb', function=lambda log:log['log_time'].date() == recharge_date and log['uid'] in row_new_user_uid_lst)
        recharge_date = row_date + datetime.timedelta(days=3)
        total_rmb_3 = daily_log_dat.get_sum_int_with_key(all_recharge_log_lst, 'add_rmb', function=lambda log:log['log_time'].date() == recharge_date and log['uid'] in row_new_user_uid_lst)
        recharge_date = row_date + datetime.timedelta(days=4)
        total_rmb_4 = daily_log_dat.get_sum_int_with_key(all_recharge_log_lst, 'add_rmb', function=lambda log:log['log_time'].date() == recharge_date and log['uid'] in row_new_user_uid_lst)
        recharge_date = row_date + datetime.timedelta(days=5)
        total_rmb_5 = daily_log_dat.get_sum_int_with_key(all_recharge_log_lst, 'add_rmb', function=lambda log:log['log_time'].date() == recharge_date and log['uid'] in row_new_user_uid_lst)
        recharge_date = row_date + datetime.timedelta(days=6)
        total_rmb_6 = daily_log_dat.get_sum_int_with_key(all_recharge_log_lst, 'add_rmb', function=lambda log:log['log_time'].date() == recharge_date and log['uid'] in row_new_user_uid_lst)
        recharge_date_7 = row_date + datetime.timedelta(days=7)
        total_rmb_7 = daily_log_dat.get_sum_int_with_key(all_recharge_log_lst, 'add_rmb', function=lambda log:log['log_time'].date() == recharge_date_7 and log['uid'] in row_new_user_uid_lst)
        recharge_date_15 = row_date + datetime.timedelta(days=15)
        total_rmb_7_15 = daily_log_dat.get_sum_int_with_key(all_recharge_log_lst, 'add_rmb', function=lambda log:recharge_date_7 < log['log_time'].date() <= recharge_date_15 and log['uid'] in row_new_user_uid_lst)
        recharge_date_30 = row_date + datetime.timedelta(days=30)
        total_rmb_15_30 = daily_log_dat.get_sum_int_with_key(all_recharge_log_lst, 'add_rmb', function=lambda log:recharge_date_15 < log['log_time'].date() <= recharge_date_30 and log['uid'] in row_new_user_uid_lst)
        total_rmb_30_up = daily_log_dat.get_sum_int_with_key(all_recharge_log_lst, 'add_rmb', function=lambda log:recharge_date_30 < log['log_time'].date() and log['uid'] in row_new_user_uid_lst)

        row = []
        row.append(row_date.strftime('%Y-%m-%d'))
        row.append(new_device_num)
        row.append(total_rmb_1)
        row.append(total_rmb_2)
        row.append(total_rmb_3)
        row.append(total_rmb_4)
        row.append(total_rmb_5)
        row.append(total_rmb_6)
        row.append(total_rmb_7)
        row.append(total_rmb_7_15)
        row.append(total_rmb_15_30)
        row.append(total_rmb_30_up)

        table_lst.append(row)
    return table_lst