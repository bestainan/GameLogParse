# -*- coding:utf -*-

"""
各等级充值情况 和 付费用户等级流失情况 这两个表相同

注册时间	开始时间	20100919	结束时间	20100920(修改为一个日期)
查询时间	查询	20100920
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"

停留人数=留存人数+流失人数
流失人数定义：到达该等级后截止至数据捞取当天，未登录天数大于等于3天的玩家
等级付费率=充值人数/到达人数
等级流失率=流失人数/到达人数

等级	停留人数	留存人数	流失人数	到达人数	充值金额	充值次数	充值人数	等级付费率	等级流失率
1
2
3
4
…
PS：本表人数均取角色数

"""

import datetime

from util import daily_log_dat
from util import game_define


def get_table(search_date, register_start_date=None, register_end_date=None, channel_id=-1, server_id=-1):
    """
        获取各等级充值状况表格
    """
    # 获取搜索区间日志
    # 本地写入的开始日期
    log_start_date = datetime.datetime.strptime(game_define.LOCAL_LOG_START_DATE, '%Y-%m-%d').date()
    new_log_lst = daily_log_dat.get_new_log_lst(log_start_date, search_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)


    #获取符合条件的日志
    if register_start_date and register_end_date:
        recharge_log_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER, function=lambda log: register_start_date <= log['install'] <= register_end_date)
    else:
        recharge_log_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER)

    # 获取所有充值玩家UID
    all_uid_log_lst = daily_log_dat.get_set_with_key(recharge_log_lst, 'uid')

    # 获取全部玩家当前等级
    uid_level_dict = dict()
    for _uid in all_uid_log_lst:
        uid_level_dict[_uid] = daily_log_dat.get_max_int_with_key(new_log_lst, 'level', function=lambda log:log['uid'] == _uid)

    # print("uid_level_dict " + str(uid_level_dict))

    # 获取全部玩家最后登录间隔天数
    uid_last_login_distance = dict()
    for _uid in all_uid_log_lst:
        # 获取玩家最后登录日志
        _user_login_logs = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['uid'] == _uid)
        if _user_login_logs:
            last_login_log = _user_login_logs[0]
            for _log in _user_login_logs:
                if _log['log_time'] > last_login_log['log_time']:
                    last_login_log = _log
            # 计算距离搜索日的日期
            last_login_dis_day = (search_date - last_login_log['log_time'].date()).days  # 最后登录间隔日期
        else:
            last_login_dis_day = 300
        # 记录
        uid_last_login_distance[_uid] = last_login_dis_day

    # 获取所有等级停留人数
    table_row_lst = []
    for _table_lv in xrange(1, 121):
        level_uid_lst = _get_level_uid_lst(_table_lv, uid_level_dict)
        lost_uid_lst = daily_log_dat.get_lost_user_set(level_uid_lst, search_date)
        arrive_uid_lst = _get_arrive_level_uid_lst(_table_lv, uid_level_dict)
        level_recharge_lst = daily_log_dat.get_recharge_lst_with_user_level(recharge_log_lst, _table_lv)
        recharge_uid_lst = daily_log_dat.get_user_uid_lst(level_recharge_lst)
        # 停留人数
        user_num = len(level_uid_lst)
        # 流失人数
        lost_num = len(lost_uid_lst)
        # 留存人数
        stand_num = user_num - lost_num
        # 到达等级人数
        arrive_num = len(arrive_uid_lst)
        # 充值金额
        recharge_money = daily_log_dat.get_recharge_total_money(level_recharge_lst)
        # 充值次数
        recharge_num = len(level_recharge_lst)
        # 充值人数
        recharge_user_num = len(recharge_uid_lst)
        # 等级付费率
        level_pay_rate = _get_level_pay_rate(recharge_user_num, arrive_num)
        # 等级流失率 流失人数/到达人数
        level_lost_rate = _get_level_lost_rate(lost_num, arrive_num)

        content = [_table_lv, user_num, lost_num, stand_num, arrive_num, recharge_money, recharge_num, recharge_user_num, level_pay_rate, level_lost_rate]
        table_row_lst.append(content)

    return table_row_lst


def _get_level_pay_rate(recharge_user_num, arrive_num):
    if arrive_num <= 0:
        return 0
    return round(float(recharge_user_num) / float(arrive_num), 2)


def _get_level_lost_rate(lost_num, arrive_num):
    if arrive_num <= 0:
        return 0
    return round(float(lost_num) / float(arrive_num), 2)


def _get_level_uid_lst(level, uid_level_dict):
    """
        获取指定等级玩家UID 列表
    """
    return [_uid for _uid, _lv in uid_level_dict.items() if _lv == level]





def _get_arrive_level_uid_lst(level, uid_level_dict):
    """
        获取到达等级的玩家
    """
    return [_uid for _uid, _lv in uid_level_dict.items() if _lv >= level]