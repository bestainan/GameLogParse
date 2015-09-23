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


def get_table(row_date, channel_id=-1, server_id=-1):
    """
        获取用户留存情况
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    table_lst = []
    row_lst = []
    rate_row_lst = []
    date_str = "_"+row_date.strftime('%Y%m%d')
    # 获取玩家安装游戏日期
    row_lst.append(row_date.strftime('%Y-%m-%d'))
    rate_row_lst.append(row_date.strftime('%Y-%m-%d')+'比率')
    for day in xrange(1, 31):
        install_date = row_date - datetime.timedelta(days=day)
        install_date_str = "_"+install_date.strftime('%Y%m%d')
        retained_num = mysql_util.get_retained_num('uid', 'EVENT_ACTION_ROLE_LOGIN'+str(date_str), install_date, row_date, game_define.EVENT_ACTION_ROLE_LOGIN, channel_id, server_id)
        today_new_user_num = mysql_util.get_today_new_num('uid', 'EVENT_ACTION_ROLE_LOGIN'+str(install_date_str), install_date, channel_id, server_id)
        row_lst.append(retained_num)
        retain_rate = Division(retained_num, today_new_user_num)
        rate_row_lst.append(str(retain_rate*100)+'%')
    table_lst.append(row_lst)
    table_lst.append(rate_row_lst)

    return table_lst


def Division(num_1, num2):
    if not num2:
        return 0
    return round(float(num_1)/float(num2), 4)