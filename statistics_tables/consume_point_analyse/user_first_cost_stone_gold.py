# -*- coding:utf-8 -*-


"""
用户首次消费点分析
查询时间	开始时间	20100920	结束时间	20100923
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

首次钻石消费点								首次金币消费点

消费点	钻石数	人数	人数比率	钻石比率				消费点	金币数	人数	人数比率	钻石比率
十连抽								升级
单抽								进化
猜拳								猜拳
洗练								洗练
购买体力								购买体力
购买金币								购买金币
…								…
总数								总数
PS：本表人数均取角色数

"""

from util import daily_log_dat
from util import game_define


def get_cost_stone_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):
    """
        获取表格
    """
    table_lst = []

    search_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['server_id'] == server_id)

    # 获取排除新手引导的日志列表
    search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: log['action'] != game_define.EVENT_ACTION_FINISH_NEWBIE)
    search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: log['action'] != game_define.EVENT_ACTION_FINISH_GUIDE)

    # 获取首次消耗钻石的日志列表
    first_cost_stone_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: 'total_cost_stone' in log and log['total_cost_stone'] == log['cost_stone'])
    # 获取首次消耗钻石的所有用户
    first_cost_stone_user_num = daily_log_dat.get_set_num_with_key(first_cost_stone_log_lst, 'uid')
    # 总钻石数
    first_cost_stone_total_num = daily_log_dat.get_sum_int_with_key(first_cost_stone_log_lst, 'total_cost_stone')

    # 根据ID拆分日志
    action_logs_dict = dict()
    for _log in first_cost_stone_log_lst:
        # print("_log:"+str(_log))
        _action = _log['action']

        if _action in action_logs_dict:
            action_logs_dict[_action].append(_log)
        else:
            lst = [_log]
            action_logs_dict[_action] = lst

    for _action, _logs in action_logs_dict.items():
        user_num = daily_log_dat.get_set_num_with_key(_logs, 'uid')
        action_total_cost_stone = daily_log_dat.get_sum_int_with_key(_logs, 'cost_stone')
        action_name = game_define.EVENT_LOG_ACTION_DICT[_action]
        # 人数比率
        cur_user_num_rate = str(_get_rate(user_num, first_cost_stone_user_num)) + "%"
        # print("action_total_cost_stone: "+str(action_total_cost_stone)+"first_cost_stone_total_num: "+str(first_cost_stone_total_num))
        # 钻石比率
        first_cost_stone_rate = str(_get_rate(action_total_cost_stone, first_cost_stone_total_num)) + "%"
        row = [action_name, action_total_cost_stone, user_num, cur_user_num_rate, first_cost_stone_rate]
        table_lst.append(row)

    return table_lst


    # 获取比率
def _get_rate(cost, total):
    """
        获取ltv值
    """
    if total <= 0:
        return 0
    return  round(float(cost) / float(total), 2) * 100


def get_cost_gold_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):
    """
        获取表格
    """

    table_lst = []
    search_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)
    if channel_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['server_id'] == server_id)
    # 获取排除新手引导的日志列表
    search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: log['action'] != game_define.EVENT_ACTION_FINISH_NEWBIE)
    search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: log['action'] != game_define.EVENT_ACTION_FINISH_GUIDE)

    # 获取首次消耗钻石的日志列表
    first_cost_gold_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: 'total_cost_gold' in log and  log['total_cost_gold'] == log['cost_gold'])

    # 获取首次消耗钻石的所有用户
    first_cost_gold_user_num = daily_log_dat.get_set_num_with_key(first_cost_gold_log_lst, 'uid')
    # 总钻石数
    first_cost_gold_total_num = daily_log_dat.get_sum_int_with_key(first_cost_gold_log_lst, 'total_cost_gold')
    # print("first_cost_gold_log_lst:"+str(first_cost_gold_log_lst))
    # 根据ID拆分日志
    action_logs_dict = dict()
    for _log in first_cost_gold_log_lst:
        _action = _log['action']
        if _action in action_logs_dict:
            action_logs_dict[_action].append(_log)
        else:
            lst = [_log]
            action_logs_dict[_action] = lst

    for _action, _logs in action_logs_dict.items():
        user_num = daily_log_dat.get_set_num_with_key(_logs, 'uid')
        action_total_cost_gold = daily_log_dat.get_sum_int_with_key(_logs, 'cost_gold')
        action_name = game_define.EVENT_LOG_ACTION_DICT[_action]
        # 人数比率
        cur_user_num_rate = str(_get_rate(user_num, first_cost_gold_user_num)) + "%"
        # 钻石比率
        first_cost_stone_rate = str(_get_rate(action_total_cost_gold, first_cost_gold_total_num)) + "%"
        row = [action_name, action_total_cost_gold, user_num, cur_user_num_rate, first_cost_stone_rate]
        table_lst.append(row)

    return table_lst