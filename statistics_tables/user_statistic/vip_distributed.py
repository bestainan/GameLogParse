# -*- coding:utf-8 -*-


"""
vip分布（具体情况根据游戏而定）
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923

"查询说明：
1.若输入注册时间，则查询表示查询注册玩家在查询时间段活跃用户的信息
2.若不输入注册时间，则查询表示查询在查询时间段的活跃用户信息"
查询时间	开始时间	20100920	结束时间	20100923
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

注：以下情况会根据游戏具体情况进行修订
条件	首冲	月卡 vip0	vip1	vip2	vip3	vip4	vip5	vip6	vip7	vip8	vip9	vip10	。。。
总体	124	124	125	124	125	126	127	128	129	130	131	132	133	134
新增	124	124	125	124	125	126	127	128	129	130	131	132	133	134
比率
比率=新增vip数/新增用户数
PS：本表用户均取角色数
"""
from util import daily_log_dat
from util import game_define


def get_table(search_start_date, search_end_date, channel_id=-1, server_id=-1):
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

    new_user_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: search_start_date <= log['install'] <= search_end_date)
    # 新用户数量
    new_user_num = daily_log_dat.get_set_num_with_key(new_user_log_lst, 'uid')
    # 获取首冲日志列表
    first_recharge_log_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER, function=lambda log: log['old_rmb'] == 0)
    first_recharge_uid_lst = daily_log_dat.get_set_with_key(first_recharge_log_lst, 'uid')
    # 新用户首冲
    new_user_first_recharge_log_lst = daily_log_dat.filter_logs(new_user_log_lst, action=game_define.EVENT_ACTION_RECHARGE_PLAYER, function=lambda log: log['old_rmb'] == 0)
    new_user_first_recharge_uid_lst = daily_log_dat.get_set_with_key(new_user_first_recharge_log_lst, 'uid')
    # 获取所有登录日志
    all_login_log_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN)
    all_login_uid_lst = daily_log_dat.get_set_with_key(all_login_log_lst, 'uid')

    # 新用户登录日志
    all_new_user_login_log_lst = daily_log_dat.filter_logs(new_user_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN)
    all_new_user_login_uid_lst = daily_log_dat.get_set_with_key(all_new_user_login_log_lst, 'uid')

    # 获取用户的所有VIP字典
    uid_vip_dict = dict()
    uid_month_days_dict = dict()
    new_user_uid_vip_dict = dict()
    new_user_uid_month_days_dict = dict()

    for _uid in all_login_uid_lst:
        _vip_lv = daily_log_dat.get_max_int_with_key(all_login_log_lst, 'vip_level', function=lambda log: log['uid'] == _uid)
        _month_card_days = daily_log_dat.get_max_int_with_key(all_login_log_lst, 'month_card_days', function=lambda log: log['uid'] == _uid)
        uid_vip_dict[_uid] = _vip_lv
        uid_month_days_dict[_uid] = _month_card_days
        if _uid in all_new_user_login_uid_lst:
            new_user_uid_vip_dict[_uid] = _vip_lv
            new_user_uid_month_days_dict[_uid] = _month_card_days

    table_lst = []

    # 首冲人数
    first_recharge_uid_num = len(first_recharge_uid_lst)
    month_card_num = get_month_user_num(uid_month_days_dict)
    vip_lst = []
    for vip in xrange(13):
        vip_num = get_vip_user_num(uid_vip_dict, vip)
        vip_lst.append(vip_num)

    row = ['总体', first_recharge_uid_num, month_card_num]
    row.extend(vip_lst)

    table_lst.append(row)

    # 新增部分数据
    new_user_first_recharge_uid_num = len(new_user_first_recharge_uid_lst)
    new_user_month_card_num = get_month_user_num(new_user_uid_month_days_dict)
    new_vip_lst = []
    for vip in xrange(13):
        vip_num = get_vip_user_num(new_user_uid_vip_dict, vip)
        new_vip_lst.append(vip_num)


    new_row = ['新增',new_user_first_recharge_uid_num, new_user_month_card_num]
    new_row.extend(new_vip_lst)
    table_lst.append(new_row)

    # 区间新增用户数
    new_user_num_row = ['新增角色数']
    new_user_num_row.extend([new_user_num] * 15)

    table_lst.append(new_user_num_row)

    rate_row = ['比率', get_rate(new_user_first_recharge_uid_num, new_user_num), get_rate(new_user_month_card_num, new_user_num) ]
    for _vip_num in new_row[3:]:
        rate_row.append(get_rate(_vip_num, new_user_num))
    table_lst.append(rate_row)

    return table_lst


def get_rate(num1, num2):
    """
        获取比例
    """
    if num2 <= 0:
        return 0
    return round(float(num1) / float(num2), 2)


def get_month_user_num(uid_month_days_dict):
    """
        获取月卡用户
    """
    num = 0
    for _days in uid_month_days_dict.values():
        if _days > 0:
            num += 1
    return num

def get_vip_user_num(uid_vip_dict, vip):
    """
        获取VIP用户数量
    """
    num = 0
    for _vip in uid_vip_dict.values():
        if _vip == vip:
            num += 1
    return num

