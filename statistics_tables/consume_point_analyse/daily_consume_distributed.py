# -*- coding:utf-8 -*-

"""
日常消费点分布
注册时间	开始时间	20100919	结束时间	20100920					"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"
查询时间	开始时间	20100920	结束时间	20100923
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

钻石消费点分布								金币消费点分布

消费点	钻石数	人数	次数	参与率	钻石消耗占比	人数占比		消费点	金币数	人数	次数	参与率	金币消耗占比	人数占比
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


def get_cost_stone_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1, server_id=-1):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # 获取搜索区间日志
    search_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)
    if channel_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['server_id'] == server_id)
    #获取符合条件的日志

    if register_start_date and register_end_date:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: register_start_date <= log['install'] <= register_end_date)

    table_lst = []
     # 全部消耗钻石日志
    all_login_log_lst = daily_log_dat.filter_logs(search_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN)
    all_cost_stone_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: 'cost_stone' in log)

    # 获取所有消耗钻石玩家UID
    uid_num = daily_log_dat.get_set_num_with_key(all_cost_stone_log_lst, 'uid')
    # 获取所有消耗钻石玩家设备lst
    device_num = daily_log_dat.get_set_num_with_key(all_login_log_lst, 'dev_id')

    # 消耗钻石总数
    total_cost_stone = daily_log_dat.get_sum_int_with_key(all_cost_stone_log_lst, 'cost_stone')

    # 根据ID拆分日志
    action_logs_dict = dict()
    for _log in all_cost_stone_log_lst:
        _action = _log['action']
        if _action in action_logs_dict:
            action_logs_dict[_action].append(_log)
        else:
            lst = [_log]
            action_logs_dict[_action]=lst

    for _action, _logs in action_logs_dict.items():
        user_num = daily_log_dat.get_set_num_with_key(_logs, 'uid')
        action_total_cost_stone = daily_log_dat.get_sum_int_with_key(_logs, 'cost_stone')
        action_name = game_define.EVENT_LOG_ACTION_DICT[_action]
        action_cost_num = len(_logs)
        # 参与率
        # print("参与率 " + str(user_num) + "  " + str(device_num))
        take_part_rate = str(_get_rate(user_num, device_num)) + "%"
        # 人数比率
        # print("人数比率 " + str(user_num) + "  " + str(uid_num))
        cur_user_num_rate = str(_get_rate(user_num, uid_num)) + "%"
        # 钻石比率
        first_cost_stone_rate = str(_get_rate(action_total_cost_stone, total_cost_stone)) + "%"
        row = [action_name, action_total_cost_stone, user_num, action_cost_num, take_part_rate, first_cost_stone_rate, cur_user_num_rate]
        table_lst.append(row)

    return table_lst

    # 获取比率
def _get_rate(cost, total):
    """
        获取ltv值
    """
    if total <= 0:
        return 0
    return round(float(cost) / float(total), 2) * 100


def get_cost_gold_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1, server_id=-1):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # 获取搜索区间日志
    search_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['server_id'] == server_id)
    #获取符合条件的日志
    if register_start_date and register_end_date:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: register_start_date <= log['install'] <= register_end_date)

    table_lst = []
     # 全部消耗金币日志
    all_login_log_lst = daily_log_dat.filter_logs(search_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN)
    all_cost_gold_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: 'cost_gold' in log)
    # 获取所有消耗钻石玩家UID
    uid_num = daily_log_dat.get_set_num_with_key(all_cost_gold_log_lst, 'uid')
    # 获取所有消耗钻石玩家设备lst
    device_num = daily_log_dat.get_set_num_with_key(all_login_log_lst, 'dev_id')

    # 消耗钻石总数
    total_cost_gold = daily_log_dat.get_sum_int_with_key(all_cost_gold_log_lst, 'cost_gold')

    # 根据ID拆分日志
    action_logs_dict = dict()
    for _log in all_cost_gold_log_lst:
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
        action_cost_num = len(_logs)
        # 参与率
        # print("参与率 " + str(user_num) + "  " + str(device_num))
        take_part_rate = _get_rate(user_num, device_num)
        # 人数比率
        # print("人数比率 " + str(user_num) + "  " + str(uid_num))
        cur_user_num_rate = _get_rate(user_num, uid_num)
        # 钻石比率
        first_cost_gold_rate = _get_rate(action_total_cost_gold, total_cost_gold)
        row = [action_name, action_total_cost_gold, user_num, action_cost_num, take_part_rate, first_cost_gold_rate, cur_user_num_rate]
        table_lst.append(row)
    return table_lst






