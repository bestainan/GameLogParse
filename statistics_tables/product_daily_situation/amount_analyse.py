# -*- coding:utf-8 -*-

"""
单设备对应账号数	占比	单ip对应设备数	占比
1个	95.74%	1个	95.74%
2个	3.55%	2个	3.55%
3个	0.47%	3个	0.47%
5个	0.24%	5个	0.24%
…		…

    这个表是一次返回整个表的
"""
from util import daily_log_dat
from util import game_define


def get_table(start_time, end_time, channel_id=-1, server_id=-1):
    """
        start_time 起始时间
        end_time 结束时间
    """
    new_log_lst = daily_log_dat.get_new_log_lst(start_time, end_time)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)

    # 获取登录事件
    action_login_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_ROLE_LOGIN)

    # 获取所有设备列表
    device_lst = daily_log_dat.get_set_with_key(new_log_lst, 'dev_id')
    ip_lst = daily_log_dat.get_set_with_key(new_log_lst, 'login_ip')

    # 获取单设备账号数比率
    device_account_result = _get_device_account_result(device_lst, action_login_lst)
    device_account_num_dict = _get_device_account_num(device_account_result)
    device_account_rate_dict = _get_device_account_rate(device_account_num_dict)

    # 获取单IP对应设备数
    ip_device_result = _get_ip_device_result(ip_lst, action_login_lst)
    ip_device_num_dict = _get_ip_device_num(ip_device_result)
    ip_device_rate_dict = _get_ip_device_rate(ip_device_num_dict)

    max_row = max(len(device_account_num_dict), len(ip_device_num_dict))
    row_lst = []
    for x in xrange(1, max_row + 1):
        row = []
        # 单设备对应账号数
        row.append(device_account_num_dict.get(x, 0))
        # 占比
        row.append(device_account_rate_dict.get(x, 0))
        # 单ip对应设备数
        row.append(ip_device_num_dict.get(x, 0))
        # 占比
        row.append(ip_device_rate_dict.get(x, 0))
        row_lst.append(row)
    return row_lst

def _get_device_account_result(device_lst, login_lst):
    """
        获取每个设备对应的账号数量
        Return:
        {
            device_id: account_set
            device_id: account_set
            device_id: account_set
        }
    """
    device_account_result = dict()
    for _device_id in device_lst:
        account_set = set()
        for log in login_lst:
            if log['dev_id'] == _device_id:
                account_set.add(log['account_id'])
        device_account_result[_device_id] = account_set
    return device_account_result

def _get_device_account_num(device_account_result):
    """
        返回
        {
        单账号：设备数
        双账号：设备数
        ...
        }
    """
    device_account_num_dict = dict()
    for key, val in device_account_result.items():
        _account_num = len(val)
        device_account_num_dict[_account_num] = device_account_num_dict.get(_account_num, 0) + 1
    return device_account_num_dict


def _get_device_account_rate(device_account_num_dict):
    """
        用单设备账号数：设备数 数据计算比率
    """
    device_account_rate_dict = dict()
    #计算总数
    total_device_num = sum(device_account_num_dict.values())
    for _account_num, val in device_account_num_dict.items():
        device_account_rate_dict[_account_num] = round(float(val) / float(total_device_num), 2)
    return device_account_rate_dict

def _get_ip_device_result(ip_lst, login_lst):
    """
        获取每个IP对应的设备数量
        Return:
        {
            ip: device_set
            ip: device_set
            ip: device_set
        }
    """
    ip_device_result = dict()
    for _ip in ip_lst:
        device_set = set()
        for log in login_lst:
            if log['login_ip'] == _ip:
                device_set.add(log['dev_id'])
        ip_device_result[_ip] = device_set
    return ip_device_result


def _get_ip_device_num(ip_device_result):
    """
        返回
        {
        单账号：设备数
        双账号：设备数
        ...
        }
    """
    ip_device_num_dict = dict()
    for key, val in ip_device_result.items():
        _device_num = len(val)
        ip_device_num_dict[_device_num] = ip_device_num_dict.get(_device_num, 0) + 1
    return ip_device_num_dict

def _get_ip_device_rate(ip_device_num_dict):
    """
        用单ip设备数据 计算比率
    """
    ip_device_rate_dict = dict()
    #计算总数
    total_ip_num = sum(ip_device_num_dict.values())
    for _device_num, val in ip_device_num_dict.items():
        ip_device_rate_dict[_device_num] = round(float(val) / float(total_ip_num), 2)
    return ip_device_rate_dict