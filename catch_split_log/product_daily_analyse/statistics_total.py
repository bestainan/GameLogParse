# -*- coding:utf-8 -*-
"""
开始时间	20101101	结束时间	20101103

游戏区服	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91/当乐	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

统计总表
时间	活跃设备数	活跃用户数	新增注册设备数	新增注册用户数	登陆设备	登陆用户	活跃账户数	新增账户数	充值人数	新增充值人数	充值金额	新增充值金额	付费率	付费arppu	登录arpu	ACU	PCU	平均在线时长（分）	人均登入次数	次日留存	3日留存	7日留存	15日留存	30日留存
2010/11/1
2010/11/2
2010/11/3
…
总数
平均
活跃设备数=登录设备-新增设备
付费率=充值人数/登录设备
用户数=角色数
"""

import datetime

from util import mysql_util
from util import game_define
# from util import daily_log_dat


def get_table(row_date, channel_id=-1, server_id=-1):
    """
        获取统计总表
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    table_lst = []
    row_lst = []
    date_str = "_"+row_date.strftime("%Y%m%d")
    # 今天登录设备数
    today_device_num = mysql_util.get_today_num('dev_id','EVENT_ACTION_ROLE_LOGIN'+str(date_str),row_date,game_define.EVENT_ACTION_ROLE_LOGIN, channel_id, server_id)
    # 今天的登录用户数
    today_user_num = mysql_util.get_today_num('uid', 'EVENT_ACTION_ROLE_LOGIN'+str(date_str), row_date,game_define.EVENT_ACTION_ROLE_LOGIN, channel_id, server_id)
    # 今天新增用户数
    today_new_user_num = mysql_util.get_today_new_num('uid','EVENT_ACTION_ROLE_LOGIN'+str(date_str), row_date, channel_id, server_id)
    #新设备数
    # today_new_device_num = mysql_util.get_all_count('dev_id','EVENT_ACTION_ROLE_LOGIN'+str(date_str),row_date + datetime.timedelta(days=1), channel_id, server_id) - mysql_util.get_all_count('dev_id','EVENT_ACTION_ROLE_LOGIN',row_date, channel_id, server_id)
    today_new_device_num = mysql_util.get_today_new_num('dev_id', 'EVENT_ACTION_ROLE_LOGIN'+str(date_str), row_date, channel_id, server_id)
    # 新账户数
    # today_new_account_num = mysql_util.get_all_count('account_id','EVENT_ACTION_ROLE_LOGIN'+str(date_str),row_date + datetime.timedelta(days=1), channel_id, server_id) - mysql_util.get_all_count('account_id','EVENT_ACTION_ROLE_LOGIN',row_date, channel_id, server_id)
    today_new_account_num = mysql_util.get_today_new_num('account_id', 'EVENT_ACTION_ROLE_LOGIN'+str(date_str), row_date, channel_id, server_id)
    # print("today_new_account_num: "+str(today_new_account_num))
    # 今天的登录账户
    today_account_num = mysql_util.get_today_num('account_id','EVENT_ACTION_ROLE_LOGIN'+str(date_str),row_date,game_define.EVENT_ACTION_ROLE_LOGIN, channel_id, server_id)
    # print("today_account_num: "+str(today_account_num))
    # 今天充值人数
    # today_recharge_user_num = mysql_util.get_recharge_uid_num('uid',row_date, channel_id, server_id)
    today_recharge_user_num = mysql_util.get_recharge_uid_num('uid', 'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), row_date, channel_id, server_id)
    # 今天新增充值人数
    # today_new_recharge_user_num = mysql_util.get_new_recharge_user_num('uid',row_date, channel_id, server_id)
    today_new_recharge_user_num = mysql_util.get_new_recharge_user_num('uid', 'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), row_date, channel_id, server_id)
    # 充值金额
    today_recharge_rmb = mysql_util.get_sum('add_rmb',row_date, 'EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id, server_id)
    # 新增充值金额
    today_new_recharge_rmb = mysql_util.get_new_sum('add_rmb',row_date,'cur_rmb', 'add_rmb','EVENT_ACTION_RECHARGE_PLAYER'+str(date_str), game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id, server_id)
    # 今天登录事件次数
    today_login_action_num = mysql_util.get_all_count('id','EVENT_ACTION_ROLE_LOGIN'+str(date_str), row_date + datetime.timedelta(days=1), channel_id, server_id)
    # get_sum('uid',row_date,table_name= 'EVENT_ACTION_ROLE_LOGIN', action=game_define.EVENT_ACTION_ROLE_LOGIN)
    # 活跃设备数
    today_active_device_num = today_device_num - today_new_device_num
    # 活跃用户数
    today_active_user_num = today_user_num - today_new_user_num
    # 登录用户数
    today_login_user_num = today_user_num
    # 登录设备数
    today_login_device_num = today_device_num
    # 活跃账户数
    today_active_account_num = today_account_num - today_new_account_num

    # 付费率=充值人数/登录设备
    pay_rate = str(100*Division(today_recharge_user_num, today_login_device_num))+"%"
    # 付费arppu 充值金额/充值人数
    pay_arppu = Division(today_recharge_rmb, today_recharge_user_num)
    # 登录arpu 充值金额/登陆设备
    login_arpu = Division(today_recharge_rmb, today_login_device_num)
    # 半小时精度在线人数列表
    # online_user_num_lst = daily_log_dat.get_online_user_len_lst(row_date, today_log_lst)
    # online_user_num_lst = [0] * 48
    # 平均在线人数 acu
    # acu = _get_acu(online_user_num_lst)
    # 最高在线人数
    # pcu = _get_pcu(online_user_num_lst)
    # 平均在线时长
    # avg_online_time = _get_avg_online_time(online_user_num_lst, today_login_user_num)
    # 人均登入次数
    avg_login_count = _get_avg_login_count(today_login_action_num, today_login_user_num)

    row_lst.append(row_date.strftime('%Y-%m-%d'))
    row_lst.append(today_active_device_num)
    row_lst.append(today_active_user_num)
    row_lst.append(today_new_device_num)
    row_lst.append(today_new_user_num)
    row_lst.append(today_login_device_num)
    row_lst.append(today_login_user_num)
    row_lst.append(today_active_account_num)
    row_lst.append(today_new_account_num)
    row_lst.append(today_recharge_user_num)
    row_lst.append(today_new_recharge_user_num)
    row_lst.append(today_recharge_rmb)
    row_lst.append(today_new_recharge_rmb)
    row_lst.append(pay_rate)
    row_lst.append(pay_arppu)
    row_lst.append(login_arpu)
    # row_lst.append(acu)
    # row_lst.append(pcu)
    # row_lst.append(avg_online_time)
    row_lst.append(avg_login_count)
    table_lst.append(row_lst)

    return table_lst


def _get_acu(online_user_num_lst):
    """
        获取平均在线人数
        暂定半小时
    """
    if not online_user_num_lst:
        return 0
    return round(float(sum(online_user_num_lst))/float(len(online_user_num_lst)), 2)


def _get_pcu(online_user_num_lst):
    """
        获取最高在线人数
    """
    return max(online_user_num_lst)


def _get_avg_online_time(online_user_num_lst, today_user_num):
    """
        平均在线时长
    """
    #计算总时长
    if not today_user_num:
        return 0
    total_minus = max(online_user_num_lst) * 30
    return round(float(total_minus)/float(today_user_num), 2)


def _get_avg_login_count(today_login_num, today_user_num):
    """
        平均登录次数
    """
    if not today_user_num:
        return 0
    return round(float(today_login_num)/float(today_user_num), 2)


def Division(num_1, num2):
    if not num2:
        return 0
    return round(float(num_1)/float(num2), 4)

# start = datetime.datetime.strptime('2015-06-04', '%Y-%m-%d').date()
# end = datetime.datetime.strptime('2015-06-04', '%Y-%m-%d').date()
# get_table(start, end)







