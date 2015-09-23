# -*- coding:utf-8 -*-

"""
付费点分析
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）


"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"



付费点分析

档位	充值金额	人数	次数	金额占比	人数占比	次数占比
30元月卡
6元
50元
100元
200元
300元
648元
1998元
总数
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
    # 获取搜索区间日志
#     new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)
#
#     if channel_id >= 0:
#         new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
#     if server_id >= 0:
#         new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)
#
#
#     #获取符合条件的日志
#     if register_start_date and register_end_date:
#         # install_from_date <= log['install'] <= install_to_date
#         recharge_log_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER, function=lambda log: register_start_date <= log['install'] <= register_end_date)
#     else:
#         recharge_log_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER)
#
#     # 获取商店数据表
#     all_recharge_config = game_config.get_all_recharge_config()
#
#     # 获取所有特定充值的日志列表
#     #根据充值ID 获取充值列表
#     recharge_money_lst = []
#     recharge_user_num_lst = []
#     recharge_num_lst = []
#     for _config in all_recharge_config:
#         recharge_id = _config['id']
#         # recharge_log = daily_log_dat.get_recharge_lst_with_shop_index(recharge_log_lst, recharge_id)
#         recharge_log = daily_log_dat.filter_logs(recharge_log_lst, function=lambda log:log['shop_index'] == recharge_id)
#
#         id_total_money = _config['money'] * len(recharge_log)
#         # id_user_num = len(daily_log_dat.get_user_uid_lst(recharge_log))
#         id_user_num = daily_log_dat.get_set_num_with_key(recharge_log, 'uid')
#         recharge_num_lst.append(len(recharge_log))
#         recharge_money_lst.append(id_total_money)
#         recharge_user_num_lst.append(id_user_num)
#
#     row_lst = []
#     for index, _config in enumerate(all_recharge_config):
#         row = []
#         total_money = recharge_money_lst[index]
#         total_user_num = recharge_user_num_lst[index]
#         total_recharge_num = recharge_num_lst[index]
#         money = _config['money']
#         # 档位
#         row.append(money)
#         # 充值金额总数
#         row.append(total_money)
#         # 人数
#         row.append(total_user_num)
#         # 次数
#         row.append(total_recharge_num)
#         # 金额比
#         row.append(get_total_money_rate(total_money,recharge_money_lst))
#         # 人数比
#         row.append(get_total_user_num_rate(total_user_num,recharge_user_num_lst))
#         # 次数比
#         row.append(get_total_recharge_num_rate(total_recharge_num,recharge_num_lst))
#         row_lst.append(row)
#
#     return row_lst
#
# def get_total_money_rate(total_money,recharge_money_lst):
#     if sum(recharge_money_lst) <= 0:
#         return 0
#     return round(float(total_money) / float(sum(recharge_money_lst)), 2)
#
# def get_total_user_num_rate(total_user_num,recharge_user_num_lst):
#     if sum(recharge_user_num_lst) <= 0:
#         return 0
#     return round(float(total_user_num) / float(sum(recharge_user_num_lst)), 2)
#
# def get_total_recharge_num_rate(total_recharge_num,recharge_num_lst):
#     if sum(recharge_num_lst) <= 0:
#         return 0
#     return round(float(total_recharge_num) / float(sum(recharge_num_lst)), 2)










