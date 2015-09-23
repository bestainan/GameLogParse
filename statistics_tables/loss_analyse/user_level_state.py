# -*- coding:utf-8 -*-


"""
    每日玩家等级表现
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923

"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"


游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

每日玩家等级表现

时间	登陆用户数	新增用户数	1	2	3	4	5	6	7	8	9	10	11	…
20101103	1419 		124	125	126	127	128	129	130	131	132	133	134
20101104	1419 		124	125	126	127	128	129	130	131	132	133	134
20101105	1419 		124	125	126	127	128	129	130	131	132	133	134
20101106	1419 		124	125	126	127	128	129	130	131	132	133	134
20101107	1419 		124	125	126	127	128	129	130	131	132	133	134
20101108	1419 		124	125	126	127	128	129	130	131	132	133	134
20101109	1419 		124	125	126	127	128	129	130	131	132	133	134
注：1.以上条件代表，2010年09月19日-2010年09月20日产生的角色，在2010年11月3日-2010年11月09日之间每天的登陆用户（去重）等级分布情况
        2.若不输入注册时间，则以上条件代表，在2010年11月3日-2010年11月09日之间每天的所选区服内登陆用户（去重）等级分布情况
PS：本表用户数均取角色数

"""

import datetime

from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1, server_id=-1, player_min_lv=1, player_max_lv=120):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)
    #获取符合条件的日志
    if register_start_date and register_end_date:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: register_start_date <= log['install'] <= register_end_date)

    # 获取日期数
    search_days = (search_end_date - search_start_date).days
    table_result = []
    for i in xrange(search_days+1):
        cur_date = search_start_date + datetime.timedelta(days=i)

        # 今日全部登录日志
        today_login_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['log_time'].date() == cur_date)
        ##
        # 昨天全部登陆日志
        yesterday_login_lst = daily_log_dat.filter_logs(yesterday_login_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log: log['log_time'].date() == cur_date - 1)
        ##


        # 用户uid列表
        today_login_uid_lst = daily_log_dat.get_set_with_key(today_login_lst, 'uid')
        today_new_user_uid_lst = daily_log_dat.get_set_with_key(today_login_lst, 'uid', function=lambda log:log['install'] == cur_date)

        #获取用户当前等级字典
        uid_level_dict = dict()
        for _uid in today_login_uid_lst:
            _lv = daily_log_dat.get_max_int_with_key(today_login_lst, 'level', function=lambda log:log['uid'] == _uid)
            uid_level_dict[_uid] = _lv


        # 登录用户数
        today_login_uid_num = len(today_login_uid_lst)
        # 新增用户数
        today_new_uid_num = len(today_new_user_uid_lst)
        # 等级用户数
        level_user_num_lst = []
        for _lv in xrange(player_min_lv, player_max_lv + 1):
            user_num = get_level_user_num(uid_level_dict, _lv)
            level_user_num_lst.append(user_num)

        row = [cur_date.strftime('%Y-%m-%d'), today_login_uid_num, today_new_uid_num]
        row.extend(level_user_num_lst)
        table_result.append(row)

    return table_result



def get_level_user_num(uid_level_dict, level):
    """
        获取等级玩家数量
    """
    num = 0
    for _level in uid_level_dict.values():
        if _level == level:
            num += 1
    return num
