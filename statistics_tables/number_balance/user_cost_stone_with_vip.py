# -*- coding:utf-8 -*-

"""
玩家钻石消耗
开始时间	20100920	结束时间	20100923
渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）

观察不同用户人群的钻石流向
消耗类型	充值用户消耗人数	充值用户消耗次数	非充值用户消耗人数	非充值用户消耗次数	消耗钻石数量 消耗金额	消耗人数	消耗金额	消耗人数	消耗金额	消耗人数
商店道具购买
商定刷新
技能点购买
体力购买
金币购买
精英管卡重置
武斗榜次数购买
豪华签到
旅行商人
黑市商人
钻石扫荡
PS：本表玩家数量均取角色数

"""

from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1, player_min_level=1,
              player_max_level=999):
    # 获取搜索区间日志
    search_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: x['server_id'] == server_id)

    # 适配等级
    search_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda x: player_min_level <= x['level'] <= player_max_level)
    # 所有的消耗钻石的日志
    all_cost_stone_log_lst = daily_log_dat.filter_logs(search_log_lst, function=lambda log: 'cost_stone' in log)
    # 根据事件拆分消耗日志
    action_cost_stone_dict = daily_log_dat.split_log_action_logs(all_cost_stone_log_lst)

    table_lst = []
    # 遍历所有事件
    for _action, _logs in action_cost_stone_dict.items():
        row_lst = []
        # 事件名称
        action_name = game_define.EVENT_LOG_ACTION_DICT[_action]
        # 充值用户消耗的部分日志
        vip1_up_user_log = daily_log_dat.filter_logs(_logs, function=lambda log:log['vip_level'] != 0)
        # 非充值用户的部分日志
        vip0_user_log = daily_log_dat.filter_logs(_logs, function=lambda log:log['vip_level'] == 0)

        # 充值用户消耗人数
        recharge_user_num = daily_log_dat.get_set_num_with_key(vip1_up_user_log, 'uid')
        # 充值用户消耗次数
        recharge_user_log_num = len(vip1_up_user_log)
        # 非充值用户的人数
        vip0_user_num = daily_log_dat.get_set_num_with_key(vip0_user_log, 'uid')
        # 非充值用户消耗次数
        vip0_user_log_num = len(vip0_user_log)
        # vip0 消耗钻石
        vip0_cost_stone_num = daily_log_dat.get_sum_int_with_key(vip0_user_log, 'cost_stone')
        # 消耗钻石数量
        total_cost_stone_num = daily_log_dat.get_sum_int_with_key(_logs, 'cost_stone')

        #事件名称 充值用户消耗人数	充值用户消耗次数	非充值用户消耗人数	非充值用户消耗次数	消耗钻石数量  VIP0消耗金额	VIP0消耗人数
        row_lst = [action_name, recharge_user_num, recharge_user_log_num, vip0_user_num, vip0_user_log_num, total_cost_stone_num, vip0_cost_stone_num, vip0_user_num]
        # 遍历VIP
        for i in xrange(1, 13):
            vip_x_log = daily_log_dat.filter_logs(vip1_up_user_log, function=lambda log:log['vip_level'] == i)
            vip_x_cost_stone_num = daily_log_dat.get_sum_int_with_key(vip_x_log, 'cost_stone')
            vip_x_cost_stone_user_num = daily_log_dat.get_set_num_with_key(vip_x_log, 'uid')
            row_lst.append(vip_x_cost_stone_num)
            row_lst.append(vip_x_cost_stone_user_num)

        table_lst.append(row_lst)

    return table_lst
