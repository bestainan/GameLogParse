# -*- coding:utf-8 -*-

"""
英雄产出、消耗统计（日新增英雄情况）

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


def get_create_table(search_start_date, search_end_date, monster_tid_lst, register_start_date=None, register_end_date=None, channel_id=-1,
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

    # print("new_log_lst: "+str(new_log_lst)+"player_min_level: "+str(player_min_level)+"player_max_level: "+str(player_max_level))
    # 适配等级
    if player_min_level and player_max_level:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: player_min_level <= x['level'] <= player_max_level)
    # print("new_log_lst: "+str(new_log_lst))

    create_monster_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: is_monster_tid_in_key(log, 'add_monster_list', monster_tid_lst))

    # 用宠物 和 星级拆分日志
    monster_tid_star_dict = dict()
    action_set = set()
    for _log in create_monster_log_lst:
        add_monster_list = _log['add_monster_list']
        action_set.add(_log['action'])
        for i in range(0, len(add_monster_list), 3):
            _tid = add_monster_list[i]
            _star = add_monster_list[i + 1]
            _lv = add_monster_list[i + 2]
            _key = str(_tid) + "," + str(_star)
            if _key in monster_tid_star_dict:
                monster_tid_star_dict[_key].append(_log)
            else:
                monster_tid_star_dict[_key] = [_log]

    # 遍历所有的怪
    table_lst = []
    head_name_lst = []
    for _tid in monster_tid_lst:

        _name = _tid
        for _star in xrange(1, 6):
            row_lst = []
            _key = str(_tid) + "," + str(_star)
            _log_lst = monster_tid_star_dict.get(_key, [])
            if _log_lst:
                # 遍历当前的怪星级的日志
                action_log_dict = daily_log_dat.split_log_action_logs(_log_lst)
                # 获取各种action的数量
                row_lst.append(_name)
                row_lst.append(_star)
                for _act in action_set:
                    row_lst.append(len(action_log_dict.get(_act, [])))
                    head_name_lst.append(game_define.EVENT_LOG_ACTION_DICT[_act])
                table_lst.append(row_lst)

    return table_lst, head_name_lst


def get_consume_table(search_start_date, search_end_date, monster_tid_lst, register_start_date=None, register_end_date=None, channel_id=-1,
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

    create_monster_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: is_monster_tid_in_key(log, 'remove_monster_list', monster_tid_lst))

    # 用宠物 和 星级拆分日志
    monster_tid_star_dict = dict()
    action_set = set()
    for _log in create_monster_log_lst:
        add_monster_list = _log['remove_monster_list']
        action_set.add(_log['action'])
        for i in range(0, len(add_monster_list), 3):
            _tid = add_monster_list[i]
            _star = add_monster_list[i + 1]
            _lv = add_monster_list[i + 2]
            _key = str(_tid) + "," + str(_star)
            if _key in monster_tid_star_dict:
                monster_tid_star_dict[_key].append(_log)
            else:
                monster_tid_star_dict[_key] = [_log]

    # 遍历所有的怪
    table_lst = []
    head_name_lst = []
    for _tid in monster_tid_lst:
        _name = _tid
        for _star in xrange(1, 6):
            row_lst = []
            _key = str(_tid) + "," + str(_star)
            _log_lst = monster_tid_star_dict.get(_key, [])
            if _log_lst:
                # 遍历当前的怪星级的日志
                action_log_dict = daily_log_dat.split_log_action_logs(_log_lst)
                # 获取各种action的数量
                row_lst.append(_name)
                row_lst.append(_star)
                for _act in action_set:
                    row_lst.append(len(action_log_dict.get(_act, [])))
                    head_name_lst.append(game_define.EVENT_LOG_ACTION_DICT[_act])
                table_lst.append(row_lst)
    return head_name_lst, table_lst


def is_monster_tid_in_key(log, key, monster_tid_lst):
    """
        怪在日志中
    """
    if key in log:
        _val = log[key]
        for i in range(0, len(_val), 3):
            _tid = _val[i]
            if _tid in monster_tid_lst:
                return True
    return False
