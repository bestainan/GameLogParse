# -*- coding:utf-8 -*-
from mysql import mysql_connection
from util import game_define
import datetime


def query(sql):
    connection = mysql_connection.get_log_mysql_connection_haima()
    return connection.query(sql)



def get_retained_num(spe_column,table_name, install_date,row_date,action=game_define.EVENT_ACTION_ROLE_LOGIN, channel_id=-1, server_id=-1):
    """
        指定日期留存人数
    """
    connection = mysql_connection.get_log_mysql_connection_haima()

    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "
    # 数据库表是否存在
    sql_exist = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % table_name
    exist_table = connection.query(sql_exist)
    if exist_table == []:
        return 0
    # 获取次数
    sql = "SELECT count(distinct %s) FROM %s where %s action = %s and install = '%s' and log_time >= '%s' and log_time < '%s'" % (spe_column,table_name, channel_server_str ,action, install_date,row_date, row_date + datetime.timedelta(days=1))

    # print sql
    count = connection.query(sql)
    # print count
    return count[0].values()[0]

def get_today_num(spe_column,table_name, row_date,action=game_define.EVENT_ACTION_ROLE_LOGIN, channel_id=-1, server_id=-1):
    """
        指定日期登录设备数
    """
     # 获取物品购买次数
    # sql = "SELECT COUNT(dev_id) FROM server_world_boss WHERE time >= '%s' and time < '%s'" % (star_time, end_time)
    connection = mysql_connection.get_log_mysql_connection_haima()
        # 数据库表是否存在
    sql_exist = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % table_name
    exist_table = connection.query(sql_exist)
    if exist_table == []:
        return 0
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "
    # 获取次数
    sql = "SELECT count(distinct %s) FROM %s where %s  action = %s and log_time >= '%s' and log_time < '%s'" % (spe_column,table_name, channel_server_str ,action, row_date, row_date + datetime.timedelta(days=1))
    # print sql
    count = connection.query(sql)
    # print count
    return count[0].values()[0]
# row_date =datetime.datetime.now() - datetime.timedelta(days=2)
# print get_today_num('uid',row_date,1)

def get_today_new_num(spe_column,table_name, row_date, channel_id=-1, server_id=-1):
    """
        指定日期今天的新增用户数

    """
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "
    connection = mysql_connection.get_log_mysql_connection_haima()
        # 数据库表是否存在
    sql_exist = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % table_name
    exist_table = connection.query(sql_exist)
    if exist_table == []:
        return 0
    # 获取次数
    sql = "SELECT count(distinct %s) FROM %s where %s action = %s and install = '%s' and log_time >= '%s' and log_time < '%s'" % (spe_column,table_name,channel_server_str, game_define.EVENT_ACTION_ROLE_LOGIN , row_date, row_date, row_date + datetime.timedelta(days=1))
    count = connection.query(sql)
    return count[0].values()[0]

def get_all_count(spe_column,table_name, row_date, channel_id=-1, server_id=-1):
    """
        指定截止到日期获取开始的所有设备数

    """
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "
    connection = mysql_connection.get_log_mysql_connection_haima()
        # 数据库表是否存在
    sql_exist = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % table_name
    exist_table = connection.query(sql_exist)
    if exist_table == []:
        return 0
    # 获取次数
    sql = "SELECT count(distinct %s) FROM %s  where %s  action = %s and log_time < '%s'" % (spe_column,table_name,channel_server_str ,game_define.EVENT_ACTION_ROLE_LOGIN , row_date)
    count = connection.query(sql)
    return count[0].values()[0]

def get_recharge_uid_num(spe_column,table_name, row_date, channel_id=-1, server_id=-1):
    """
        指定日期充值人数
    """
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "
    connection = mysql_connection.get_log_mysql_connection_haima()
    # 获取次数
    sql = "SELECT count(distinct %s) FROM %s where %s  action = %s and log_time >= '%s' and log_time < '%s'" % (spe_column ,table_name, channel_server_str,game_define.EVENT_ACTION_RECHARGE_PLAYER, row_date, row_date + datetime.timedelta(days=1))
    # print sql
    count = connection.query(sql)
    # print count
    return count[0].values()[0]

def get_new_recharge_user_num(spe_column,table_name, row_date, channel_id=-1, server_id=-1):
    """
        指定日期新增充值人数
        today_new_recharge_user_num = daily_log_dat.get_set_num_with_key(today_log_lst, 'uid', game_define.EVENT_ACTION_RECHARGE_PLAYER, lambda log:log['cur_rmb']== log['add_rmb'])
    """
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "
    connection = mysql_connection.get_log_mysql_connection_haima()
    # 数据库表是否存在
    sql_exist = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % table_name
    exist_table = connection.query(sql_exist)
    if exist_table == []:
        return 0
    # 获取次数
    sql = "SELECT count(distinct %s) FROM %s where %s  action = %s and cur_rmb = add_rmb and log_time >= '%s' and log_time < '%s'" % (spe_column,table_name, channel_server_str,game_define.EVENT_ACTION_RECHARGE_PLAYER, row_date, row_date + datetime.timedelta(days=1))
    # print sql
    count = connection.query(sql)
    # print count
    return count[0].values()[0]

def get_sum(spe_column,row_date,table_name= 'EVENT_ACTION_RECHARGE_PLAYER', action=game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id=-1, server_id=-1):
    """
        指定日期充值金额
        today_recharge_rmb = daily_log_dat.get_sum_int_with_key(today_log_lst, 'add_rmb', game_define.EVENT_ACTION_RECHARGE_PLAYER)
    """
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "
    connection = mysql_connection.get_log_mysql_connection_haima()
    # 数据库表是否存在
    sql_exist = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % table_name
    exist_table = connection.query(sql_exist)
    if exist_table == []:
        return 0
    # 获取次数
    sql = "SELECT sum(%s) FROM %s where %s  action = %s and log_time >= '%s' and log_time < '%s'" % (spe_column,table_name,channel_server_str,action, row_date, row_date + datetime.timedelta(days=1))
    print sql
    count = connection.query(sql)
    if not count[0].values()[0]:
        return 0
    print type(count)
    return count[0].values()[0]

def get_new_sum(spe_column,row_date,cur_val, add_val,table_name= 'EVENT_ACTION_RECHARGE_PLAYER', action=game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id=-1, server_id=-1):
    """
        指定日期充值金额
        today_recharge_rmb = daily_log_dat.get_sum_int_with_key(today_log_lst, 'add_rmb', game_define.EVENT_ACTION_RECHARGE_PLAYER)
    """
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "
    connection = mysql_connection.get_log_mysql_connection_haima()
        # 数据库表是否存在
    sql_exist = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % table_name
    exist_table = connection.query(sql_exist)
    if exist_table == []:
        return 0
    # 获取次数
    sql = "SELECT sum(%s) FROM %s where %s action = %s and %s = %s and log_time >= '%s' and log_time < '%s'" % (spe_column,table_name,channel_server_str,action,cur_val, add_val, row_date, row_date + datetime.timedelta(days=1))
    # print sql
    count = connection.query(sql)
    if not count[0].values()[0]:
        return 0
    # print count
    return count[0].values()[0]

def get_spec_sum(spe_column=None,from_date=None,to_date=None,specfy_column_name='shop_index', shop_index = -1,table_name= 'EVENT_ACTION_RECHARGE_PLAYER', action=game_define.EVENT_ACTION_RECHARGE_PLAYER, channel_id=-1, server_id=-1,register_start_date=None, register_end_date=None,ext=None):
    """
        指定日期指定充值档充值金额金额总数
        function=lambda log: register_start_date <= log['install'] <= register_end_date)
    """
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "
    if register_start_date:
        channel_server_str += "  '%s' <= install and " % register_start_date
    if register_end_date:
        channel_server_str += " install  <= '%s' and " % register_end_date
    if spe_column == 'add_rmb':
        spe_column = 'sum(add_rmb) '
    if spe_column == 'uid':
        spe_column = 'count(distinct uid) '
    if not spe_column:
        spe_column = 'count(uid) '

    shop_index_str = ""
    if shop_index > 0:
        shop_index_str += " and  " + str(specfy_column_name) + str(shop_index)
    # 扩展字段
    ext_str = ""
    if ext:
        ext_str += " and  %s " %ext

    connection = mysql_connection.get_log_mysql_connection_haima()
        # 数据库表是否存在
    sql_exist = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % table_name
    exist_table = connection.query(sql_exist)
    if exist_table == []:
        return 0
    # 获取次数
    sql = "SELECT %s FROM %s where %s action = %s  and log_time >= '%s' and log_time < '%s' %s %s" % (spe_column,table_name,channel_server_str,action, from_date, to_date,shop_index_str,ext_str)
    print sql
    count = connection.query(sql)
    if not count[0].values()[0]:
        return 0
    # print count
    return count[0].values()[0]

def get_role_charge_lst(search_date=None, channel_id=-1, server_id=-1,register_start_date=None, register_end_date=None):
    """
        指定日期流失人数
        function=lambda log: register_start_date <= log['install'] <= register_end_date)
    """
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "
    if register_start_date:
        channel_server_str += "  '%s' <= install and " % register_start_date
    if register_end_date:
        channel_server_str += " install  <= '%s' and " % register_end_date

    connection = mysql_connection.get_log_mysql_connection_haima()
    # 获取次数
    sql = "SELECT * FROM EVENT_ACTION_RECHARGE_PLAYER where %s  log_time >= '%s' and log_time < '%s'" % (channel_server_str,search_date,search_date + datetime.timedelta(days=1))
    print sql
    count = connection.query(sql)
    # print count
    return count


def get_role_action_lst(table_name='EVENT_ACTION_ROLE_LOGIN',from_date=None, to_date=None, channel_id=-1, server_id=-1,register_start_date=None, register_end_date=None):
    """
        指定日期玩家登陆
        function=lambda log: register_start_date <= log['install'] <= register_end_date)
    """
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += " platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += "  server_id = " + str(server_id)+" and "
    if register_start_date:
        channel_server_str += "  '%s' <= install and " % register_start_date
    if register_end_date:
        channel_server_str += " install  <= '%s' and " % register_end_date
    connection = mysql_connection.get_log_mysql_connection_haima()
        # 数据库表是否存在
    sql_exist = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % table_name
    exist_table = connection.query(sql_exist)
    if exist_table == []:
        return 0
    sql = "SELECT *  FROM %s  where %s  log_time >= '%s' and log_time < '%s'" % (table_name,channel_server_str, from_date,to_date + datetime.timedelta(days=1))
    # print sql
    count = connection.query(sql)
    # print (count)
    return count



# get1_sum()
# -----------------------------------------------------------------
def get_set_with_key(log_lst, key, action=None, function=None):
    """
        获取指定key的数量
    """
    _lst = []
    if action:
        _lst = [log for log in log_lst if log['action'] == action]
    if function:
        _lst = [log for log in log_lst if function(log)]
    # print _lst[0]['uid']
    lost_uid_set = set()
    for item in _lst:
        # print item['uid']
        lost_uid_set.add(item['uid'])
    # print lost_uid_set
    # s = {log[key] for log in _lst if key in log}
    return lost_uid_set


def get_max_int_with_key(log_lst, key, action=None, function=None):
    """
        获取最大值
    """

    _lst = []
    if action:
        _lst = [log for log in log_lst if log['action'] == action]
    if function:
        _lst = [log for log in log_lst if function(log)]
    print("_lst " + str(_lst))

    lost_uid_lst = []
    for item in _lst:
        lost_uid_lst.append(item['level'])
    print("lost_uid_lst " + str(lost_uid_lst))
    # lst = [log[key] for log in _lst if key in log]
    return max(lost_uid_lst)

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
    # print("_last_login_date: "+str(_last_login_date))
    _last_login_user_lst = get_set_with_key(retained_log_lst, 'uid', function=lambda log:log['log_time'].date() == _last_login_date)
    # print("_last_login_user_lst: "+str(_last_login_user_lst))
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


def get_recharge_lst_with_user_level(recharge_log_lst, level):
    """
        根据玩家等级获取充值日志
    """
    return [log for log in recharge_log_lst if log.get('level', 0) == level]


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

def get_recharge_total_money(recharge_log_lst):
    """
        获取充值总金额
    """
    money_lst = [int(log['add_rmb']) for log in recharge_log_lst]
    return sum(money_lst)