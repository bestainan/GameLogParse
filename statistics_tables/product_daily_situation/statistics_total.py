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

from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):
    """
        获取统计总表
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    start_log_time = datetime.datetime.strptime(game_define.LOCAL_LOG_START_DATE, '%Y-%m-%d').date()
    # 获取搜索区间日志
    new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)



    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)

    # pay_code_log_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER)
    # pay_code_res = dict()
    # for log in pay_code_log_lst:
    #     plat = game_define.PLAT_FORM_NAME_DICT[log['platform_id']]
    #     if plat in pay_code_res:
    #         pay_code_res[plat].append(log['order_id'])
    #     else:
    #         pay_code_res[plat] = [log['order_id']]
    # print("订单 " + str(pay_code_res))

    # 总天数
    table_lst = []
    total_days = (search_end_date - search_start_date).days + 1
    for i in xrange(total_days):
        row_lst = []
        # 每行的日期
        row_date = search_start_date + datetime.timedelta(days=i)
        row_yesterday_date = row_date - datetime.timedelta(days=1)
        # print("-------------------------------"+str(row_date)+"---------------------------------------------")
        #　获取到昨天的全部日志
        until_yesterday_all_log_lst = daily_log_dat.get_new_log_lst(start_log_time, row_yesterday_date)
        # # 获取上一天开始的所有设备数
        until_yesterday_all_device = daily_log_dat.get_set_with_key(until_yesterday_all_log_lst, 'dev_id')
        # # 到昨天为止登录用户数
        # # yesterday_all_user_num = daily_log_dat.get_set_num_with_key(yesterday_all_log_lst, 'uid')
        # # # 到昨天为止的登录账户
        # # yesterday_all_account_num = daily_log_dat.get_set_num_with_key(yesterday_all_log_lst, 'account_id')
        # # # 到昨天为止充值人数
        # # yesterday_all_recharge_user_num = daily_log_dat.get_set_num_with_key(yesterday_all_log_lst, 'uid', game_define.EVENT_ACTION_RECHARGE_PLAYER)
        #
        # # 获取到今天的所有日志
        # until_today_all_log_lst = daily_log_dat.get_new_log_lst(start_log_time, row_date)
        # # 到今天为止所有设备数
        # until_today_all_device_num = daily_log_dat.get_set_num_with_key(until_today_all_log_lst, 'dev_id')
        # # # 到今天为止的登录用户数
        # # today_all_user_num = daily_log_dat.get_set_num_with_key(today_all_log_lst, 'uid')
        # # # 到今天为止的登录账户
        # # today_all_account_num = daily_log_dat.get_set_num_with_key(today_all_log_lst, 'account_id')
        # # # 到今天为止充值人数
        # # # today_all_recharge_user_num = daily_log_dat.get_set_num_with_key(today_all_log_lst, 'uid', game_define.EVENT_ACTION_RECHARGE_PLAYER)

        # 今天的日志
        today_log_lst = daily_log_dat.get_new_log_lst_with_log(new_log_lst, row_date, row_date)
        # 今天登录设备数
        today_device_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'dev_id')
        # 今天的登录用户数
        today_user_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid')
        # 今天新增用户数
        today_new_user_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid', function=lambda log:log['install'] == row_date)
        #新设备数
        today_new_device_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'dev_id', action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['dev_id'] not in until_yesterday_all_device)
        # 新账户数
        today_new_account_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'account_id', action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['install'] == row_date)
        # 今天的登录账户
        today_account_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'account_id')
        # 今天充值人数
        today_recharge_user_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_RECHARGE_PLAYER)
        # 今天新增充值人数
        today_new_recharge_user_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_RECHARGE_PLAYER, lambda log:log['cur_rmb']== log['add_rmb'])
        # 充值金额
        today_recharge_rmb = daily_log_dat.get_sum_int_with_key(today_log_lst, 'add_rmb', game_define.EVENT_ACTION_RECHARGE_PLAYER)
        # 新增充值金额
        today_new_recharge_rmb = daily_log_dat.get_sum_int_with_key(today_log_lst, 'add_rmb', game_define.EVENT_ACTION_RECHARGE_PLAYER, lambda log:log['cur_rmb']== log['add_rmb'])
        # 今天登录事件次数
        today_login_action_num = daily_log_dat.get_list_num_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_ROLE_LOGIN)


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
        # print("-------------------------------"+str(row_date)+"---------------------------------------------")
        # print("充值玩家 " + str(daily_log_dat.get_set_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_RECHARGE_PLAYER)))
        # print("新增充值玩家 " + str(daily_log_dat.get_set_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_RECHARGE_PLAYER, lambda log:log['cur_rmb']== log['add_rmb'])))
        # print("充值金额列表 " + str(daily_log_dat.get_list_with_key(today_log_lst, 'add_rmb', game_define.EVENT_ACTION_RECHARGE_PLAYER)))
        # print("新增充值金额列表 " + str(daily_log_dat.get_list_with_key(today_log_lst, 'add_rmb', game_define.EVENT_ACTION_RECHARGE_PLAYER, lambda log:log['cur_rmb']== log['add_rmb'])))

        # 付费率=充值人数/登录设备
        pay_rate = Division(today_recharge_user_num, today_login_device_num)
        # 付费arppu 充值金额/充值人数
        pay_arppu = Division(today_recharge_rmb, today_recharge_user_num)
        # 登录arpu 充值金额/登陆设备
        login_arpu = Division(today_recharge_rmb, today_login_device_num)
        # 半小时精度在线人数列表
        online_user_num_lst = daily_log_dat.get_online_user_len_lst(row_date, today_log_lst)
        # 平均在线人数 acu
        acu = _get_acu(online_user_num_lst)
        # 最高在线人数
        pcu = _get_pcu(online_user_num_lst)
        # 平均在线时长
        avg_online_time = _get_avg_online_time(online_user_num_lst, today_login_user_num)
        # 人均登入次数
        avg_login_count = _get_avg_login_count(today_login_action_num, today_login_user_num)

        # 获取玩家安装游戏日期
        install_date = row_date - datetime.timedelta(days=1)
        retained_1_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_ROLE_LOGIN, lambda log:log['install'] == install_date)
        install_date = row_date - datetime.timedelta(days=3)
        retained_3_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_ROLE_LOGIN, lambda log:log['install'] == install_date)
        install_date = row_date - datetime.timedelta(days=7)
        retained_7_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_ROLE_LOGIN, lambda log:log['install'] == install_date)
        install_date = row_date - datetime.timedelta(days=15)
        retained_15_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_ROLE_LOGIN, lambda log:log['install'] == install_date)
        install_date = row_date - datetime.timedelta(days=30)
        retained_30_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_ROLE_LOGIN, lambda log:log['install'] == install_date)

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
        row_lst.append(acu)
        row_lst.append(pcu)
        row_lst.append(avg_online_time)
        row_lst.append(avg_login_count)
        row_lst.append(retained_1_num)
        row_lst.append(retained_3_num)
        row_lst.append(retained_7_num)
        row_lst.append(retained_15_num)
        row_lst.append(retained_30_num)
        table_lst.append(row_lst)

    # print("table_lst " + str(table_lst))
    return table_lst







#
#
#
#
# def get_row_dat(line_time, channel_id=-1, server_id=-1):
#     """
#         获取表格行数据
#         line_time 日期 date
#
#     """
#
#     # 区间日志
#     start_log_time = datetime.datetime.strptime(game_define.LOCAL_LOG_START_DATE, '%Y-%m-%d').date()
#     yesterday_time = line_time - datetime.timedelta(days=1)
#
#     new_log_lst = daily_log_dat.get_new_log_lst(start_log_time, yesterday_time)
#
#     if channel_id:
#         new_log_lst = daily_log_dat.get_log_lst_with_channel(new_log_lst, channel_id)
#     if server_id:
#         new_log_lst = daily_log_dat.get_log_lst_with_server(new_log_lst, server_id)
#
#     today_log_lst = daily_log_dat.get_new_log_lst(line_time, line_time)
#     today_recharge_log_lst = daily_log_dat.get_recharge(today_log_lst)
#     today_first_recharge_log_lst = daily_log_dat.get_first_recharge_log_lst(today_recharge_log_lst)
#
#     # 获取上一天开始的所有设备名
#     old_device_lst = daily_log_dat.get_device_lst(new_log_lst)
#     # 获取当天设备名
#     today_device_lst = daily_log_dat.get_device_lst(today_log_lst)
#     # 获取新设备数
#     new_device_set = {dev for dev in today_device_lst if dev not in old_device_lst}
#     #获取登录用户列表
#     user_lst = daily_log_dat.get_user_uid_lst(today_log_lst)
#     # 获取新增用户
#     new_user_lst = daily_log_dat.get_user_uid_lst_with_create_player(today_log_lst)
#     # 获取老账号列表
#     old_account_lst = daily_log_dat.get_account_num(new_log_lst)
#     # 获取今天登录账号
#     today_account_lst = daily_log_dat.get_account_num(today_log_lst)
#     # 获取新增账号列表
#     new_account_set = {account for account in today_account_lst if account not in old_account_lst}
#     #充值人数
#     today_recharge_uid_lst = daily_log_dat.get_recharge_user(today_log_lst)
#     # 新增充值玩家
#     today_first_recharge_user_uid_lst = daily_log_dat.get_user_uid_lst(today_first_recharge_log_lst)
#     # 今天充值总额
#     today_recharge_rmb_num = daily_log_dat.get_recharge_total_money(today_recharge_log_lst)
#     # 今天新增充值RMB数
#     today_new_recharge_rmb_num = daily_log_dat.get_recharge_total_money(today_first_recharge_log_lst)
#     # 半小时精度在线人数列表
#     online_user_num_lst = daily_log_dat.get_online_user_len_lst(line_time, today_log_lst)
#     # 人均登录次数
#     today_login_lst = daily_log_dat.get_login_log(today_log_lst)
#     #---------------次日留存获取-----------
#     # 获取玩家安装游戏日期
#     install_date = line_time - datetime.timedelta(days=1)
#     # 获取今天登录的玩家列表 并且 昨天安装
#     retained_1_login_uid_set = daily_log_dat.get_login_uid_set_with_install(install_date, today_log_lst)
#     #3日留存
#     install_date = line_time - datetime.timedelta(days=3)
#     retained_3_login_uid_set = daily_log_dat.get_login_uid_set_with_install(install_date, today_log_lst)
#     #7日留存
#     install_date = line_time - datetime.timedelta(days=7)
#     retained_7_login_uid_set = daily_log_dat.get_login_uid_set_with_install(install_date, today_log_lst)
#     #15日留存
#     install_date = line_time - datetime.timedelta(days=15)
#     retained_15_login_uid_set = daily_log_dat.get_login_uid_set_with_install(install_date, today_log_lst)
#     #30日留存
#     install_date = line_time - datetime.timedelta(days=30)
#     retained_30_login_uid_set = daily_log_dat.get_login_uid_set_with_install(install_date, today_log_lst)
#
#     result = dict()
#     result['time'] = line_time.strftime('%Y-%m-%d')
#     result['active_device_num'] = _get_active_device_num(today_device_lst, new_device_set)
#     result['active_user_num'] = _get_active_user_num(user_lst, new_user_lst)
#     result['new_device_num'] = _get_new_device_num(new_device_set)
#     result['new_register_user_num'] = _get_new_register_user_num(new_user_lst)
#     result['login_device_num'] = _get_login_device_num(today_device_lst)
#     result['login_user_num'] = _get_login_user_num(user_lst)
#     result['active_account_num'] = _get_active_account_num(today_account_lst, new_account_set)
#     result['new_account_num'] = _get_new_account_num(new_account_set)
#     result['recharge_num'] = _get_recharge_num(today_recharge_uid_lst)
#     result['new_recharge_num'] = _get_new_recharge_num(today_first_recharge_user_uid_lst)
#     result['today_recharge_rmb_num'] = today_recharge_rmb_num
#     result['today_new_recharge_rmb_num'] = today_new_recharge_rmb_num
#     result['recharge_rate'] = _get_recharge_rate(len(today_recharge_uid_lst), len(today_device_lst))
#     result['recharge_arppu'] = _get_recharge_arppu(today_recharge_rmb_num, len(today_recharge_uid_lst))
#     result['login_arpu'] = _get_login_arpu(today_recharge_rmb_num, len(today_device_lst))
#     result['acu'] = _get_acu(online_user_num_lst)
#     result['pcu'] = _get_pcu(online_user_num_lst)
#     result['avg_online_time'] = _get_avg_online_time(online_user_num_lst, len(user_lst))
#     result['avg_login_count'] = _get_avg_login_count(len(today_login_lst), len(user_lst))
#     result['1_retained'] = len(retained_1_login_uid_set)
#     result['3_retained'] = len(retained_3_login_uid_set)
#     result['7_retained'] = len(retained_7_login_uid_set)
#     result['15_retained'] = len(retained_15_login_uid_set)
#     result['30_retained'] = len(retained_30_login_uid_set)
#
#     return [result['time'],
#             result['active_device_num'],
#             result['active_user_num'] ,
#             result['new_device_num'],
#             result['new_register_user_num'],
#             result['login_device_num'] ,
#             result['login_user_num'] ,
#             result['active_account_num'],
#             result['new_account_num'],
#             result['recharge_num'],
#             result['new_recharge_num'] ,
#             result['today_recharge_rmb_num'],
#             result['today_new_recharge_rmb_num'] ,
#             result['recharge_rate'],
#             result['recharge_arppu'],
#             result['login_arpu'],
#             result['acu'],
#             result['pcu'],
#             result['avg_online_time'] ,
#             result['avg_login_count'] ,
#             result['1_retained'] ,
#             result['3_retained'],
#             result['7_retained'] ,
#             result['15_retained'] ,
#             result['30_retained']
#             ]


# def _get_active_device_num(today_device_lst, new_device_set):
#     """
#         获取活跃设备数
#         登录设备 - 新增设备
#         line_time 当前表格行的日期
#     """
#     # print("_get_active_device_num today_device_lst:"+str(today_device_lst)+" new_device_set:"+str(new_device_set))
#     # print("_get_active_device_num len(today_device_lst):"+str(len(today_device_lst))+" len(new_device_set):"+str(len(new_device_set)))
#     return len(today_device_lst) - len(new_device_set)


# def _get_active_user_num(user_lst, new_user_lst):
#     """
#         获取活跃用户数
#         登录用户数 - 新增用户数
#         line_time 当前表格行的日期
#     """
#     return len(user_lst) - len(new_user_lst)


# def _get_new_device_num(new_device_set):
#     """
#         获取新注册设备数
#     """
#     return len(new_device_set)


# def _get_new_register_user_num(new_user_lst):
#     """
#         新用户数量
#     """
#     return len(new_user_lst)


# def _get_login_device_num(today_device_lst):
#     """
#         获取登录设备数
#     """
#     return len(today_device_lst)

#
# def _get_login_user_num(user_lst):
#     """
#         获取登录用户数量
#     """
#     return len(user_lst)


# def _get_active_account_num(today_account_lst, new_account_set):
#     """
#         活跃账号数
#     """
#     return len(today_account_lst) - len(new_account_set)

#
# def _get_new_account_num(new_account_set):
#     """
#         获取新增账号数
#     """
#     return len(new_account_set)


# def _get_recharge_num(today_recharge_lst):
#     """
#         获取充值人数
#     """
#     return len(today_recharge_lst)


# def _get_recharge_rmb_num():
#     """
#         获取充值数值
#     """
#     return


# def _get_new_recharge_num(today_new_recharge_lst):
#     """
#         新增充值人数
#     """
#     return len(today_new_recharge_lst)


# def _get_recharge_rate(recharge_num, device_num):
#     """
#         付费率
#         充值人数 / 登录设备数
#     """
#     if device_num == 0:
#         return 0
#     return round(float(recharge_num)/float(device_num), 2)


# def _get_recharge_arppu(today_recharge_rmb_num, today_recharge_num):
#     """
#         获取充值arppu
#         充值金额/充值人数
#     """
#     if not today_recharge_num:
#         return 0
#     return round(float(today_recharge_rmb_num)/float(today_recharge_num), 2)


# def _get_login_arpu(today_recharge_rmb_num, login_device_num):
#     """
#         登录arpu
#         充值金额/登陆设备
#     """
#     if not login_device_num:
#         return 0
#     return round(float(today_recharge_rmb_num)/float(login_device_num), 2)


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
    return round(float(num_1)/float(num2), 2)









