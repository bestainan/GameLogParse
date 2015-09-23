# -*- coding:utf-8 -*-

"""
英雄洗练统计
注册时间	开始时间	20100919	结束时间	20100919
查询时间	开始时间	20100920	结束时间	20100923
渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）

英雄名称	50次以内	50-100	100-150	...
皮卡丘
妙蛙种子
…
"""



from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1,
              server_id=-1, player_min_level=1,
              player_max_level=999):
    #获取搜索区间日志
    new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)
    #获取符合条件的日志
    if register_start_date and register_end_date:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: register_start_date <= log['install'] <= register_end_date)

    # 适配等级
    if player_min_level and player_max_level:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: player_min_level <= x['level'] <= player_max_level)

    individual_action_lst = [
        game_define.EVENT_ACTION_RESET_INDIVIDUAL_MONSTER,
        game_define.EVENT_ACTION_STONE_RESET_INDIVIDUAL_MONSTER
    ]
    reset_individual_logs = daily_log_dat.filter_logs(new_log_lst, function=lambda log: log['action'] in individual_action_lst)

    table_lst = []
    monster_tid_dict = daily_log_dat.split_log_with_key_value(reset_individual_logs, 'monster_tid')

    for key in monster_tid_dict.keys():
        _tid = key
        _name = key
        if _tid in monster_tid_dict:
            _logs = monster_tid_dict[_tid]
            # 获取用户次数字典
            user_dict = daily_log_dat.split_log_with_key_value(_logs, 'uid')
            reset_50_user_num = get_reset_individual_user_num(user_dict, 1, 50)
            reset_50_100_user_num = get_reset_individual_user_num(user_dict, 51, 100)
            reset_100_200_user_num = get_reset_individual_user_num(user_dict, 101, 200)
            reset_200_400_user_num = get_reset_individual_user_num(user_dict, 201, 400)
            reset_400_800_user_num = get_reset_individual_user_num(user_dict, 401, 800)
            reset_up_800_user_num = get_reset_individual_user_num(user_dict, 801, 10000)

            row_lst = [_name, reset_50_user_num, reset_50_100_user_num, reset_100_200_user_num, reset_200_400_user_num, reset_400_800_user_num, reset_up_800_user_num]
            table_lst.append(row_lst)
    return table_lst


def get_reset_individual_user_num(user_dict, min_count, max_count):
    """
        获取指定次数区间内洗练的玩家次数
    """
    user_num = 0
    for _uid,_logs in user_dict.items():
        num = len(_logs)
        if min_count <= num <= max_count:
            user_num += 1
    return user_num