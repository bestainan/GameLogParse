# -*- coding:utf-8 -*-


"""
    用户终身价值
开始日期	20101101	结束日期	20101101
分区查询	总/1区/2区	（默认总数、下拉菜单手动选择区服）
渠道标示	UC/91	（默认总数、下拉菜单手动选择渠道）				注：用户终身价值待商定


LTV	用户终身价值	某日新注册用户N人，他们在第M天的LTV值，即这N个人在这M天中的总充值额/N。（每天都分开算）


日期	新增登录用户	LTV-1	LTV-2	LTV-3	LTV-4	LTV-5	LTV-6	LTV-7	……	LTV15	LTV30	LTV60
2013/11/20	1000	10	11	12	13	14	15	16	17	18	19
2013/11/21	1000	10	11	12	13	14	15	16	17	18	19
2013/11/22	1000	10	11	12	13	14	15	16	17	18	19
2013/11/23	1000	10	11	12	13	14	15	16	17	18	19
2013/11/24	1000	10	11	12	13	14	15	16	17	18	19
2013/11/25	1000	10	11	12	13	14	15	16	17	18	19
2013/11/26	1000	10	11	12	13	14	15	16	17	18	19
2013/11/27	1000	10	11	12	13	14	15	16	17	18	19
2013/11/28	1000	10	11	12	13	14	15	16	17	18	19
2013/11/29	1000	10	11	12	13	14	15	16	17	18	19
PS：本表人数均取角色数
"""

import datetime

from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):
    """
        获取表格
    """
    # 获取搜索区间日志
    search_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)
    if channel_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['server_id'] == server_id)

    search_total_day = (search_end_date - search_start_date).days
    table_lst = []
    for i in xrange(search_total_day + 1):
        _search_date = search_start_date + datetime.timedelta(days=1 * i)
        #获取当天日志
        _row_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log:log['log_time'].date() == _search_date)

        # 获取新用户日志
        new_user_lst = daily_log_dat.get_set_with_key(_row_log_lst, 'uid', action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['install'] == _search_date)
        new_user_num = len(new_user_lst)

        ltv_day_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 30, 60]
        ltv_val_lst = []
        for ltv_days in ltv_day_lst:
            start_date =_search_date
            end_date = _search_date + datetime.timedelta(days=ltv_days)
            ltv_logs = daily_log_dat.get_new_log_lst(start_date, end_date)
            ltv_recharge_log_lst = daily_log_dat.filter_logs(ltv_logs, action=game_define.EVENT_ACTION_RECHARGE_PLAYER, function=lambda log:log['uid'] in new_user_lst)
            total_recharge_money = daily_log_dat.get_sum_int_with_key(ltv_recharge_log_lst, 'add_rmb')

            ltv_val = _get_ltv_value(new_user_num, total_recharge_money)
            ltv_val_lst.append(ltv_val)

        row_lst = [_search_date, new_user_num]
        row_lst.extend(ltv_val_lst)
        table_lst.append(row_lst)
    return table_lst



# 获取新用户日志
def _get_ltv_value(user_num, total_recharge_money):
    """
        获取ltv值
    """
    if user_num <= 0:
        return 0
    return  round(float(total_recharge_money) / float(user_num), 2)