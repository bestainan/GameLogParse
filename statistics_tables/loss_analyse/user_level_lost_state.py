# -*- coding:utf-8 -*-


"""
整体用户等级流失情况
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923

"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"

游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

整体用户等级流失情况

等级	停留人数	留存人数	流失人数	到达人数	等级流失率
1	65	9	56	370	15.14%
2	21	3	18	305	5.90%
3	32	10	22	284	7.75%
4	22	11	11	252	4.37%
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
    # 获取搜索区间日志
    new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)
    #获取符合条件的日志
    if register_start_date and register_end_date:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: register_start_date <= log['install']<= register_end_date)


    # 获取新增用户部分日志
    all_login_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN)
    all_uid_log_lst = daily_log_dat.get_set_with_key(all_login_lst, 'uid')

    # 获取全部玩家最后登录间隔天数
    uid_level_dict = dict()
    for _uid in all_uid_log_lst:
        uid_level_dict[_uid] = daily_log_dat.get_max_int_with_key(all_login_lst, 'level', function= lambda x: x['uid'] == _uid)

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
            last_login_dis_day = (search_end_date - last_login_log['log_time'].date()).days  # 最后登录间隔日期
        else:
            last_login_dis_day = 300
        # 记录
        uid_last_login_distance[_uid] = last_login_dis_day

    # 遍历全部等级
    table_row_lst = []
    for _table_lv in xrange(1, 121):
        level_uid_lst = _get_level_uid_lst(_table_lv, uid_level_dict)
        lost_uid_lst = daily_log_dat.get_lost_user_set(new_log_lst, search_end_date)
        arrive_uid_lst = _get_arrive_level_uid_lst(_table_lv, uid_level_dict)

        # 停留人数
        user_num = len(level_uid_lst)
        # 流失人数
        lost_num = len(lost_uid_lst)
        # 留存人数
        stand_num = user_num - lost_num
        # 到达等级人数
        arrive_num = len(arrive_uid_lst)
        # 等级流失率
        level_lost_rate = _get_level_lost_rate(lost_num, arrive_num)
        # 等级	停留人数	留存人数	流失人数	到达人数	等级流失率
        content = [_table_lv, user_num, stand_num, lost_num, arrive_num, level_lost_rate]
        table_row_lst.append(content)

    return table_row_lst


def _get_level_lost_rate(lost_num, arrive_num):
    if arrive_num <= 0:
        return 0
    return round(float(lost_num)/float(arrive_num), 2)


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
