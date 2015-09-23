# -*- coding:utf-8 -*-

"""
钻石商城物品购买
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

购买物品	钻石数	人数	次数	参与率	钻石消耗占比	人数占比
太阳石
精华
装备碎片
…

PS：本表人数均取角色数
"""

from util import daily_log_dat

from util import game_define


def get_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1, server_id=-1):
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
    # print("new_log_lst111: "+str(new_log_lst))
    # 全部钻石商城物品购买日志
    all_stone_shop_log_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_STONE_SHOP_BUY)
    # print("all_stone_shop_log_lst: "+str(all_stone_shop_log_lst))
    # 获取所有钻石商城物品玩家设备
    device_lst = daily_log_dat.get_set_with_key(all_stone_shop_log_lst, 'dev_id')

    # 获取所有钻石商城物品购买日志玩家UID
    all_uid_lst = daily_log_dat.get_set_with_key(all_stone_shop_log_lst, 'uid')

    # 消耗钻石总数
    total_cost_stone = daily_log_dat.get_sum_int_with_key(all_stone_shop_log_lst, 'cost_stone')

    # 根据ID拆分日志
    item_logs_dict = dict()
    for _log in all_stone_shop_log_lst:
        _item_info = _log['add_item_list']
        _item_tid = _item_info[0]

        if _item_tid in item_logs_dict:
            item_logs_dict[_item_tid].append(_log)
        else:
            lst = [_log]
            item_logs_dict[_item_tid] = lst

    table_lst = []
    for _item_tid, _log in item_logs_dict.items():

        user_num = daily_log_dat.get_set_num_with_key(_log, 'uid')
        # 购买物品
        # item_config = game_config.get_item_config(int(_item_tid))

        event_log_act = _item_tid
        # 钻石数
        cost_stone = daily_log_dat.get_sum_int_with_key(_log, 'cost_stone')
        # 次数
        cost_num = len(_log)
        # 参与率
        take_part_rate = _get_rate(user_num, len(device_lst))
        # 钻石比率
        first_cost_stone_rate = _get_rate(cost_stone, total_cost_stone)
        # 人数比率
        cur_user_num_rate = _get_rate(user_num, len(all_uid_lst))

        row = [event_log_act, cost_stone, user_num, cost_num, take_part_rate, first_cost_stone_rate, cur_user_num_rate]
        table_lst.append(row)

    return table_lst

    # 获取比率
def _get_rate(cost, total):
    """
        获取ltv值
    """
    if total <= 0:
        return 0
    return round(float(cost) / float(total), 2)
