# -*- coding:utf-8 -*-

"""
    用户首日等级留存
查询日期	20101101
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

用户首日等级留存	"1.选取当天新登录的用户的最大等级统计，并计算这批用户的次日留存率
2.有效用户按登录用户计算"

等级 人数	占比 次日留存率
1	100	5.00%	31%
2	100	5.00%	32%
3	100	5.00%	33%
4	100	5.00%	34%
5	100	5.00%	35%
6	100	5.00%	36%
7	100	5.00%	37%
13	100	5.00%	43%
14	100	5.00%	44%
15	100	5.00%	45%
16	100	5.00%	46%
17	100	5.00%	47%
18	100	5.00%	48%
19	100	5.00%	49%
20	100	5.00%	50%
总计	2000	5.00%	45%
PS：本表用户数均取角色数
"""

import datetime

from util import daily_log_dat
from util import game_define


def get_table(search_date, channel_id=-1, server_id=-1):
    """
        获取用户首日等级留存
    """

    all_log_lst = daily_log_dat.get_new_log_lst(search_date, search_date + datetime.timedelta(days=1))

    if channel_id >= 0:
        all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        all_log_lst = daily_log_dat.filter_logs(all_log_lst, function=lambda x: x['server_id'] == server_id)

    # print("留存计算日 " + str((search_date + datetime.timedelta(days=1))))
    # print("留存日所有登录日志 2" + str(daily_log_dat.filter_logs(all_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['install'] == search_date and log['log_time'].date() == (search_date + datetime.timedelta(days=1)))))

    # 获取今天新创建用户登录日志
    today_new_user_login_log_lst = daily_log_dat.filter_logs(all_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['install'] == search_date and log['log_time'].date() == search_date)
    # 获取新创建用户列表
    today_new_user_lst = daily_log_dat.get_set_with_key(today_new_user_login_log_lst, 'uid')
    # print("登录用户列表 " + str(today_new_user_lst))
    # 获取次日登录的用户列表
    retained_login_log_lst = daily_log_dat.filter_logs(all_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['install'] == search_date and log['log_time'].date() == (search_date + datetime.timedelta(days=1)))
    retain_user_lst = daily_log_dat.get_set_with_key(retained_login_log_lst, 'uid')
    # print("留存用户列表 " + str(retain_user_lst))
    # # 留存用户
    # retain_use_uid_lst = daily_log_dat.get_set_with_key(all_login_log_lst, 'uid', function=lambda log:log['install'] == search_date)
    # # 获取新玩家当前最终等级
    uid_level_dict = daily_log_dat.split_log_users_level(all_log_lst)
    # print("用户等级分布 " + str(uid_level_dict))
    # # 获取今天登录的玩家列表 并且 昨天安装
    # retained_1_login_uid_set = daily_log_dat.get_set_with_key(all_log_lst, 'uid', function= lambda log:log['uid'] in retain_use_uid_lst)


    table_result = []
    for i in xrange(1,31):
        row = _get_row(i, uid_level_dict, today_new_user_lst, retain_user_lst)
        table_result.append(row)

    return table_result


def _get_row(level, uid_level_dict, today_new_user_lst, retain_user_lst):
    """
        获取行数据
        等级 人数	占比	次日留存率
    """
    # print("----------------"+str(level)+ "--------------------")
    uid_lst = [_uid for _uid, lv in uid_level_dict.items() if lv == level and _uid in today_new_user_lst]
    retained_uid_lst = [_uid for _uid, lv in uid_level_dict.items() if lv == level and _uid in retain_user_lst]
    # print("玩家 " + str(uid_lst))
    # print("留存玩家 " + str(retained_uid_lst))
    # 等级用户
    level_user_num = len(uid_lst)
    # 获取次日留存
    level_rate = str(_get_level_user_num_rate(level_user_num, len(today_new_user_lst))) + "%"

    retained_rate = str(_get_retained_1_login_rate(len(retained_uid_lst), level_user_num)) + "%"

    return [level, level_user_num, level_rate, retained_rate]

  # 获取比率
def _get_level_user_num_rate(level_user_num, total_user):
    """

    """
    if total_user <= 0:
        return 0
    return round(float(level_user_num) / float(total_user), 2) * 100


 # 获取比率
def _get_retained_1_login_rate(level_user_num, retained_1_login_uid_set):
    if retained_1_login_uid_set <= 0:
        return 0
    return  round(float(level_user_num) / float(retained_1_login_uid_set), 2) * 100