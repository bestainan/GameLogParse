# -*- coding:utf-8 -*-

"""
道具产出、消耗统计（日新增英雄情况）

注册时间	开始时间	20100919	结束时间	20100919			"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃玩家信息
3.查询玩家等级区间可以调整，最小等级1级无法调整"

查询时间	开始时间	20100920	结束时间	20100923

渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）
英雄名称		产出							消耗	收邮件	礼包	GM指令
种类	星级	手工激活	钻石单抽	钻石十连抽	普通副本产出	精英副本产出	抓宠	创建角色	转化
皮卡丘	1星
皮卡丘	2星
…	…
妙蛙种子	1星
妙蛙种子	2星
…	…

"""

from util import daily_log_dat
from util import game_define


def get_create_table(search_start_date, search_end_date, item_tid_lst, register_start_date=None, register_end_date=None, channel_id=-1,
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

    create_item_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: is_item_tid_in_key(log, 'add_item_list', item_tid_lst))

    # 用装备TID 拆分日志
    item_tid_dict = dict()
    action_set = set()
    for _log in create_item_log_lst:
        add_item_list = _log['add_item_list']
        action_set.add(_log['action'])
        for i in range(0, len(add_item_list), 2):
            _tid = add_item_list[i]
            # _num = add_equip_list[i + 1]
            _key = _tid
            if _key in item_tid_dict:
                item_tid_dict[_key].append(_log)
            else:
                item_tid_dict[_key] = [_log]

    # 遍历所有的怪
    table_lst = []
    head_name_lst = []
    for _tid in item_tid_lst:
        row_lst = []

        _name =_tid
        _key = _tid
        _log_lst = item_tid_dict.get(_key, [])
        if _log_lst:
            # 遍历当前的怪星级的日志
            action_log_dict = daily_log_dat.split_log_action_logs(_log_lst)
            # 获取各种action的数量
            row_lst.append(_name)
            for _act in action_set:
                row_lst.append(len(action_log_dict.get(_act, [])))
                head_name_lst.append(game_define.EVENT_LOG_ACTION_DICT[_act])
            table_lst.append(row_lst)
    return head_name_lst, table_lst


def get_consume_table(search_start_date, search_end_date, item_tid_lst, register_start_date=None, register_end_date=None, channel_id=-1,
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

    cost_item_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: is_item_tid_in_key(log, 'cost_item_list', item_tid_lst))

    # 用装备TID 拆分日志
    item_tid_dict = dict()
    action_set = set()
    for _log in cost_item_log_lst:
        cost_item_list = _log['cost_item_list']
        action_set.add(_log['action'])
        for i in range(0, len(cost_item_list), 2):
            _tid = cost_item_list[i]
            # _num = add_equip_list[i + 1]
            _key = _tid
            if _key in item_tid_dict:
                item_tid_dict[_key].append(_log)
            else:
                item_tid_dict[_key] = [_log]

    # 遍历所有的怪
    table_lst = []
    head_name_lst = []
    for _tid in item_tid_lst:
        row_lst = []
        _name = _tid
        _key = _tid
        _log_lst = item_tid_dict.get(_key, [])
        if _log_lst:
            # 遍历当前的怪星级的日志
            action_log_dict = daily_log_dat.split_log_action_logs(_log_lst)
            # 获取各种action的数量
            row_lst.append(_name)
            for _act in action_set:
                row_lst.append(len(action_log_dict.get(_act, [])))
                head_name_lst.append(game_define.EVENT_LOG_ACTION_DICT[_act])
            table_lst.append(row_lst)
    return head_name_lst, table_lst


def is_item_tid_in_key(log, key, equip_tid_lst):
    """
        怪在日志中
    """
    if key in log:
        _val = log[key]
        for i in range(0, len(_val), 2):
            _tid = _val[i]
            if _tid in equip_tid_lst:
                return True
    return False
