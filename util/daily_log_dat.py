# -*- coding:utf-8 -*-

"""
    每日日志对象
"""
import datetime

# 保存日志获取的数据
from util import game_define

all_log_lst = []


def get_new_log_lst_with_key(log_lst, key):
    """
        获取包含特定KEY的日志
    """
    return [log for log in log_lst if key in log]


def get_log_lst_with_level(log_lst, level):
    """
        用等级拆分日志
    """
    return [log for log in log_lst if log['level'] == level]


def get_user_uid_lst(log_lst, from_date=None, to_date=None):
    """
        获取用户列表
        from_date datetime
        to_date datetime
    """
    if from_date and to_date:
        user_uid_set = {log['uid'] for log in log_lst if from_date <= log['log_time'].date() <= to_date}
    else:
        user_uid_set = {log['uid'] for log in log_lst}
    return list(user_uid_set)


def get_item_tid_lst(log_lst, from_date=None, to_date=None):
    """
        获取item——tid表
        from_date datetime
        to_date datetime
    """
    if from_date and to_date:
        item_tid_set = {log['item_tid'] for log in log_lst if log['item_tid'] > 0}
    else:
        item_tid_set = {log['item_tid'] for log in log_lst}
    return list(item_tid_set)


def get_log_with_uid(log_lst, uid):
    return [log for log in log_lst if log['uid'] == uid]


def get_user_uid_lst_with_create_player(log_lst):
    """
        获取用户区间内新用户
    """
    user_uid_set = {log['uid'] for log in log_lst if log['action'] == game_define.EVENT_ACTION_CREATE_ROLE}
    return list(user_uid_set)


def get_user_uid_lst_with_datetime(log_lst, from_datetime, to_datetime):
    """
        获取指定时间段内游戏的用户
    """
    user_uid_set = {log['uid'] for log in log_lst if from_datetime <= log['log_time'] <= to_datetime}
    return list(user_uid_set)


def get_log_with_install_time(log_lst, install_from_date, install_to_date):
    """
        获取日志内 指定安装时间的特定玩家的日志
    """
    install_user_uid_lst = [log['uid'] for log in log_lst if install_from_date <= log.get('install', 0) <= install_to_date]

    return [log for log in log_lst if log['uid'] in install_user_uid_lst]


def get_account_num(new_log_lst):
    """
        获取账号数
    """
    user_uid_set = {log['account_id'] for log in new_log_lst if 'account_id' in log}
    return list(user_uid_set)


def get_device_lst(log_lst):
    """
        获取全部设备
    """
    device_set = {log['dev_id'] for log in log_lst if 'dev_id' in log}
    return list(device_set)


def get_ip_lst(log_lst):
    """
        获取全部IP
    """
    ip_set = {log['login_ip'] for log in log_lst if 'login_ip' in log}
    return list(ip_set)


def get_user_online_time(log_lst, user_uid):
    """
        获取玩家在线时长
    """
    user_log_lst = [log for log in log_lst if log['uid'] == user_uid]
    first_log = None
    end_log = None
    for log in user_log_lst:
        if not first_log or first_log['log_time'] < log['log_time']:
            first_log = log
        if not end_log or end_log['log_time'] > log['log_time']:
            end_log = log

    return (first_log['log_time'] - end_log['log_time']).total_seconds()






def get_login_uid_set_with_install(line_time, one_day_log_lst):
    """
        获取指定安装日期的玩家 登录列表
    """

    return {log['uid'] for log in one_day_log_lst if log['action'] == game_define.EVENT_ACTION_ROLE_LOGIN and log['install'] == line_time}

# ----------------------------------------------------充值部分---------------------------------------------------

def get_recharge_with_install(log_lst, install_from_date, install_to_date):
    return [log for log in log_lst if (log['action'] == game_define.EVENT_ACTION_RECHARGE_PLAYER) and install_from_date <= log['install'] <= install_to_date]


def get_recharge(log_lst, from_day=0, to_day=0):
    """
        获取充值日志列表
        from_day 创建日期开始第几天充值
        to_day 创建日期开始第几天充值
    """
    recharge_lst = [log for log in log_lst if (log['action'] == game_define.EVENT_ACTION_RECHARGE_PLAYER)]
    if to_day:
        recharge_lst = [log for log in recharge_lst if (log['log_time'].date() - log['install']).days <= to_day]
    if from_day:
        recharge_lst = [log for log in recharge_lst if from_day < (log['log_time'].date() - log['install']).days]
    return recharge_lst


def get_recharge_log_lst_with_uid_lst(log_lst, uid_lst):
    """
        获取充值日志， 用uid列表
    """
    return [log for log in log_lst if (log['action'] == game_define.EVENT_ACTION_RECHARGE_PLAYER) and log['uid'] in uid_lst]


def get_recharge_lst_with_shop_index(recharge_log_lst, shop_index):
    """
        根据商店ID获取对应的全部日志
    """
    return [log for log in recharge_log_lst if log['shop_index'] == shop_index]


def get_recharge_lst_with_user_level(recharge_log_lst, level):
    """
        根据玩家等级获取充值日志
    """
    return [log for log in recharge_log_lst if log.get('level', 0) == level]


def get_recharge_user(new_log_lst):
    """
        充值用户数
    """
    user_recharge_set = {log['uid'] for log in new_log_lst if 'add_rmb' in log}
    return list(user_recharge_set)


def get_recharge_total_money(recharge_log_lst):
    """
        获取充值总金额
    """
    money_lst = [int(log['add_rmb']) for log in recharge_log_lst]
    return sum(money_lst)


def get_first_recharge_log_lst(recharge_log_lst, days=0):
    """
        获取新增充值人数
    """
    first_recharge_log_lst = [log for log in recharge_log_lst if log.get('old_rmb', 0) == 0]
    if days:    # 加上安装后第几天充值的条件
        first_recharge_log_lst = [log for log in first_recharge_log_lst if (log['log_time'].date() - log['install']).days == days]
    return first_recharge_log_lst

# ----------------------------------------------------钻石商城物品购买---------------------------------------------------

def get_stone_shop_log_lst(log_lst):
    """
        获取钻石商城物品购买日志
    """
    first_cost_stone_log_lst = [log for log in log_lst if log['action'] == game_define.EVENT_ACTION_STONE_SHOP_BUY]
    return first_cost_stone_log_lst

def get_cost_stone_log_with_item_tid(cost_stone_log_lst, item_tid):
    """
        获取所有item_tid指定消耗钻石日志
    """
    cost_stone_log_lst = [log for log in cost_stone_log_lst if log['item_tid'] == item_tid]
    return cost_stone_log_lst

def get_stone_shop_log_with_install(log_lst, install_from_date, install_to_date):
    return [log for log in log_lst if (log['action'] == game_define.EVENT_ACTION_STONE_SHOP_BUY) and install_from_date <= log['install'] <= install_to_date]

def get_stone_shop_log(log_lst, from_day=0, to_day=0):
    """
        获取钻石商城物品购买日志列表
        from_day 创建日期开始第几天消耗钻石
        to_day 创建日期开始第几天消耗钻石
    """
    cost_stone_lst = [log for log in log_lst if (log['action'] == game_define.EVENT_ACTION_STONE_SHOP_BUY)]
    if to_day:
        cost_stone_lst = [log for log in cost_stone_lst if (log['log_time'].date() - log['install']).days <= to_day]
    if from_day:
        cost_stone_lst = [log for log in cost_stone_lst if from_day < (log['log_time'].date() - log['install']).days]
    return cost_stone_lst



# ----------------------------------------------------钻石消耗查询---------------------------------------------------



def get_cost_stone_log_with_action(cost_stone_log_lst, reason_action):
    """
        获取所有事件指定消耗钻石日志
    """
    cost_stone_log_lst = [log for log in cost_stone_log_lst if log['reason'] == reason_action]
    return cost_stone_log_lst

def get_total_cost_stone(cost_stone_log_lst):
    """
        获取钻石总消耗
    """
    cost_num_lst = [int(log.get('cost', 0)) for log in cost_stone_log_lst]
    return sum(cost_num_lst)

# ----------------------------------------------------登录事件-------------------------------------------------------

def get_login_log(log_lst):
    """
        获取所有的登录日志
    """
    return [log for log in log_lst if log['action'] == game_define.EVENT_ACTION_ROLE_LOGIN]


def get_last_login_log(login_lst):
    """
        获取每个玩家的最后登录日志
    """
    uid_lst = get_user_uid_lst(login_lst)

    last_login_lst = []
    for _uid in uid_lst:
        last_login_log = None
        log_lst = get_log_with_uid(login_lst, _uid)
        for log in log_lst:
            if not last_login_log or last_login_log['log_time'] < log['log_time']:
                last_login_log = log
        last_login_lst.append(last_login_log)

    return last_login_lst


def get_uid_vip_dict_with_last_login_lst(last_login_lst):
    """
        获取登录VIP字典
    """
    uid_vip_dict = dict()
    for log in last_login_lst:
        uid_vip_dict[log['uid']] = log['vip_level']
    return uid_vip_dict


def get_uid_level_dict_with_log_lst(log_lst):
    """
        获取登录VIP字典
    """
    uid_lv_dict = dict()
    for log in log_lst:
        uid_lv_dict[log['uid']] = log['level']
    return uid_lv_dict



def get_uid_month_days_dict_with_last_login_lst(last_login_lst):
    """
        获取登录VIP字典
    """
    uid_month_days_dict = dict()
    for log in last_login_lst:
        uid_month_days_dict[log['uid']] = log.get('month_card_days', 0)
    return uid_month_days_dict


def get_uid_login_back_lst(login_lst):
    """
        获取回流用户
    """
    return [log['uid'] for log in login_lst if log['login_dis_days'] > 3]


def get_uid_lost_lst(last_login_lst, target_date):
    """
        获取日志列表中所有流失的用户（超过3天没登录）
        last_login_lst 是4天的日志 最后一天应该是target_date
    """
    return [log['uid'] for log in last_login_lst if (log['log_time'].date() - target_date).days > 3]


def get_user_lost_log_lst(last_login_lst, target_date):
    """
        获取流失用户的登录日志
        last_login_lst 是4天的日志 最后一天应该是target_date
    """
    return [log for log in last_login_lst if (log['log_time'].date() - target_date).days > 3]


def get_user_player_days(login_log):
    """
        获取玩家游戏天数
    """
    return (login_log['log_time'] - login_log['log_time']).days



# ----------------------------------------------------金币消耗查询---------------------------------------------------



def get_cost_gold_log_with_action(cost_gold_log_lst, reason_action):
    """
        获取所有事件指定 消耗钻石日志
    """
    cost_gold_log_lst = [log for log in cost_gold_log_lst if log['reason'] == reason_action]
    return cost_gold_log_lst


def get_total_cost_gold(cost_gold_log_lst):
    """
        获取钻石总消耗
    """
    cost_num_lst = [int(log.get('cost', 0)) for log in cost_gold_log_lst]
    return sum(cost_num_lst)


# ----------------------------------------------------单体用户查询---------------------------------------------------

def get_user_cur_level(log_lst, uid):
    """
        查询玩家的等级记录 获取当前等级
    """
    # 当前用户的升级事件
    level_up_log_lst = [log for log in log_lst if log['action'] == game_define.EVENT_ACTION_ROLE_LEVEL_UP and log['uid'] == uid]
    # 获取最高等级
    cur_level = 0
    for log in level_up_log_lst:
        if cur_level < log['later_level']:
            cur_level = log['later_level']
    return cur_level

def get_user_last_login_distance_day(log_lst, uid):
    """
        获取玩家最后登录日期 跟目标日期的间隔
    """
    # 当前用户的登录事件
    login_log_lst = [log for log in log_lst if log['action'] == game_define.EVENT_ACTION_ROLE_LOGIN and log['uid'] == uid]
    if not login_log_lst:
        return 0

    # 获取最后登录日期间隔天数
    login_dis_days = 0
    for log in login_log_lst:
        login_dis_days = log['login_dis_days']
    return login_dis_days

# ----------------------------------------------------新手引导---------------------------------------------------

def get_guide_log(log_lst):
    """
        获取所有引导日志
    """

    guide_log_lst = [log for log in log_lst if log['action'] == game_define.EVENT_ACTION_FINISH_GUIDE]

    return guide_log_lst


def get_guide_log_with_guide_id(guide_log_lst, guide_id):
    """
        获取指定的引导ID 日志
    """
    guide_log_lst = [log for log in guide_log_lst if log['guide_id'] == guide_id]
    return guide_log_lst


# ----------------------------------------------------通用部分---------------------------------------------------

def get_sum_int_with_key(log_lst, key, action=None, function=None):
    """
        获取指定key的累加
    """

    _lst = log_lst
    if action:
        _lst = [log for log in _lst if log['action'] == action]
    if function:
        _lst = [log for log in _lst if function(log)]

    lst = [log.get(key, 0) for log in _lst if key in log]

    return sum(lst)


def get_max_int_with_key(log_lst, key, action=None, function=None):
    """
        获取最大值
    """

    _lst = log_lst
    if action:
        _lst = [log for log in _lst if log['action'] == action]
    if function:
        _lst = [log for log in _lst if function(log)]

    lst = [log[key] for log in _lst if key in log]

    return max(lst)


def get_list_num_with_key(log_lst, key, action=None, function=None):
    """
        获取指定key的数量
    """

    _lst = log_lst
    if action:
        _lst = [log for log in _lst if log['action'] == action]
    if function:
        _lst = [log for log in _lst if function(log)]

    lst = [log[key] for log in _lst if key in log]

    return len(lst)


def get_list_with_key(log_lst, key, action=None, function=None):
    """
        获取指定key的数量
    """

    _lst = log_lst
    if action:
        _lst = [log for log in _lst if log['action'] == action]
    if function:
        _lst = [log for log in _lst if function(log)]

    lst = [log[key] for log in _lst if key in log]
    return lst


def get_set_num_with_key(log_lst, key, action=None, function=None):
    """
        获取指定key的数量
    """
    _lst = log_lst
    if action:
        _lst = [log for log in _lst if log['action'] == action]
    if function:
        _lst = [log for log in _lst if function(log)]

    s = {log[key] for log in _lst if key in log}
    return len(s)


def get_set_with_key(log_lst, key, action=None, function=None):
    """
        获取指定key的数量
    """
    _lst = log_lst
    if action:
        _lst = [log for log in _lst if log['action'] == action]
    if function:
        _lst = [log for log in _lst if function(log)]
    s = {log[key] for log in _lst if key in log}
    return s


def get_new_log_lst(from_date, to_date):
    """
        获取指定日期的日志
    """
    return [log for log in all_log_lst if from_date <= log['log_time'].date() <= to_date]


def filter_logs(new_log_lst, action=None, function=None):
    """
        筛选日志
    """
    _lst = new_log_lst
    if action:
        _lst = [log for log in _lst if log['action'] == action]
    if function:
        _lst = [log for log in _lst if function(log)]

    return _lst


def get_log_lst_with_channel(new_log_lst, channel_id=-1):
    """

    """
    return [log for log in new_log_lst if log['platform_id'] == channel_id]


def get_log_lst_with_server(new_log_lst, server_id=-1):
    """
    result['server_id'] = item_lst[1]
    result['platform_id'] = item_lst[2]
    """
    return [log for log in new_log_lst if log['server_id'] == server_id]


def get_new_log_lst_with_log(log_lst, from_date, to_date):
    """
        在日志列表内 按照指定日期获取日志列表
    """
    return [log for log in log_lst if from_date <= log['log_time'].date() <= to_date]


def get_online_user_len_lst(show_date, today_log_lst, minute=30):
    """
        获取在线用户时间
        半小时一次
    """
    result_lst = []
    count = 24 * 60 / minute
    show_datetime = datetime.datetime.strptime(str(show_date), '%Y-%m-%d')
    for i in xrange(count):
        time_dis = datetime.timedelta(minutes=minute*i)
        start_datetime = show_datetime + time_dis
        end_datetime = start_datetime + datetime.timedelta(minutes=minute)
        user_set = {log['uid'] for log in today_log_lst if start_datetime <= log['log_time'] <= end_datetime}
        result_lst.append(len(user_set))
    return result_lst



def get_online_user_uid_lst(show_date, today_log_lst, minute=30):
    """
        获取玩家时间段分布（5分钟）
    """

    result_lst = []
    count = 24 * 60 / minute
    show_datetime = datetime.datetime.strptime(str(show_date), '%Y-%m-%d')
    for i in xrange(count):
        time_dis = datetime.timedelta(minutes=minute*i)
        start_datetime = show_datetime + time_dis
        end_datetime = start_datetime + datetime.timedelta(minutes=minute)
        user_set = {log['uid'] for log in today_log_lst if start_datetime <= log['log_time'] <= end_datetime}
        result_lst.append(user_set)
    return result_lst


def get_dict_uid_last_login_distance_day(log_lst, uid_lst, end_date):
    """
        获取用户最后登录距离日期
    """
    uid_last_login_distance = dict()
    for _uid in uid_lst:
        # 获取玩家最后登录日志
        _user_login_logs = filter_logs(log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['uid'] == _uid)
        if _user_login_logs:
            last_login_log = _user_login_logs[0]
            for _log in _user_login_logs:
                if _log['log_time'] > last_login_log['log_time']:
                    last_login_log = _log
            # 计算距离搜索日的日期
            last_login_dis_day = (end_date - last_login_log['log_time'].date()).days  # 最后登录间隔日期
        else:
            last_login_dis_day = 300
        # 记录
        uid_last_login_distance[_uid] = last_login_dis_day
    return uid_last_login_distance


def get_lost_user_set(retained_log_lst, lost_check_date):
    """
        Arg:
            retained_log_lst 包含检查日期3天前 到检查日当天的日志
        获取流失用户
        3天前登录了 但是直到检查日都没再次登录
    """
    _last_login_date = lost_check_date - datetime.timedelta(days=3)
    # print("计算最终登录日期 " + str(_last_login_date))
    # 获取登录玩家uid
    _last_login_user_lst = get_set_with_key(retained_log_lst, 'uid', function=lambda log:log['log_time'].date() == _last_login_date)
    # print("最终登录玩家 " + str(_last_login_user_lst))
    #截取对应日期的日志 (2天前的到检查日 如果完全没有那个用户的消息 就是流失)
    lost_retained_log_lst = filter_logs(retained_log_lst,
                                   function=lambda log:_last_login_date + datetime.timedelta(days=1) <= log['log_time'].date() <= lost_check_date)
    # print("计算日期 " + str(_last_login_date + datetime.timedelta(days=1)) + "   " + str(lost_check_date))
    _retain_log_user_lst = get_set_with_key(lost_retained_log_lst, 'uid')

    # print("近3天登录玩家 " + str(_retain_log_user_lst))

    lost_uid_set = set()
    for _uid in _last_login_user_lst:
        if _uid not in _retain_log_user_lst:
            lost_uid_set.add(_uid)
    # print("流失用户 " + str(lost_uid_set))
    return lost_uid_set


def get_lost_back_user_set(retained_log_lst, back_check_date):
    """
        获取回流用户
        流失后又再次登录的
    """
    # 流失用户
    lost_check_date = back_check_date - datetime.timedelta(days=1)
    lost_uid_lst = get_lost_user_set(retained_log_lst, lost_check_date)

    back_log_lst = filter_logs(retained_log_lst,
                                   function=lambda log:log['log_time'].date() == back_check_date)

    lost_back_set = set()
    for _uid in lost_uid_lst:
        _log_lst = filter_logs(back_log_lst, function=lambda log:log['uid']==_uid)
        if _log_lst:
            lost_back_set.add(_uid)

    return lost_back_set


def get_retained_user_set(retained_log_lst, check_date):
    """
        获取留存用户
        在指定日期还在游戏的用户
    """
    # 获取登录玩家uid
    _check_login_user_set = get_set_with_key(retained_log_lst, 'uid', action=game_define.EVENT_ACTION_ROLE_LOGIN, function=lambda log:log['log_time'].date() == check_date)

    return _check_login_user_set


# ------------------------------------拆分日志部分-------------------------------------------

def split_log_users_last_stone(log_lst):
    """
        获取玩家最后的钻石数值
    """
    user_stone_dict = dict()
    user_time_dict = dict()
    for _log in log_lst:
        _uid = _log['uid']
        if 'cur_stone' in _log:
            _cur = _log['cur_stone']
            _time = _log['log_time']
            if _uid not in user_time_dict or _time > user_time_dict[_uid]:
                user_time_dict[_uid] = _time
                user_stone_dict[_uid] = _cur
    return user_stone_dict


def split_log_users_last_gold(log_lst):
    """
        获取玩家最后的金币数值
        {
            _uid: gold 玩家最后登录时候的金币
        }
    """
    user_gold_dict = dict()
    user_time_dict = dict()
    for _log in log_lst:
        _uid = _log['uid']
        if 'cur_gold' in _log:
            _cur = _log['cur_gold']
            _time = _log['log_time']
            if _uid not in user_time_dict or _time > user_time_dict[_uid]:
                user_time_dict[_uid] = _time
                user_gold_dict[_uid] = _cur
    return user_gold_dict

def split_log_users_play_days(log_lst):
    """
        获取玩家游戏天数
        {
            _uid: player_days 游戏最高天数
        }
    """
    user_player_day_dict = dict()
    for _log in log_lst:
        _uid = _log['uid']
        player_days = (_log['log_time'].date() - _log['install']).days + 1
        if player_days >= user_player_day_dict.get(_uid, 0):
            user_player_day_dict[_uid] = player_days
    return user_player_day_dict


def split_log_users_level(log_lst):
    """
        拆分日志列表
        {
            _uid: _level 列表中玩家最高等级
        }
    """
    user_level_dict = dict()
    for _log in log_lst:
        _uid = _log['uid']
        _level = _log['level']
        if _level > user_level_dict.get(_uid, 0):
            user_level_dict[_uid] = _level

    return user_level_dict

def split_log_action_logs(log_lst):
    """
        用事件拆分日志
        {
            _action: [log ...] 所有日志当前事件日志列表
        }
    """
    action_logs_dict = dict()
    for _log in log_lst:
        _action = _log['action']
        if _action in action_logs_dict:
            action_logs_dict[_action].append(_log)
        else:
            action_logs_dict[_action] = [_log]

    return action_logs_dict


def split_log_with_key_value(log_lst, key):
    """
        用key切分日志
        {
            _val （key的值）: [log ...] 所有日志当前事件日志列表
        }
    """
    key_logs_dict = dict()
    for _log in log_lst:
        if key in _log:
            _val = _log[key]
            if _val in key_logs_dict:
                key_logs_dict[_val].append(_log)
            else:
                key_logs_dict[_val] = [_log]
    return key_logs_dict
