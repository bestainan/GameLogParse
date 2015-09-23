# -*- coding:utf-8 -*-

"""
    时间基类
"""
import time
import datetime


def log_base(gm):
    """
        日志基础
    """
    log_time = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    uid = str(gm.uid)
    account = str(gm.account)
    name = gm.name.encode('utf8')
    description = gm.description.encode('utf8')
    permission = str(gm.permissions)

    log_lst = []
    log_lst.append(log_time)
    log_lst.append(uid)
    log_lst.append(account)
    log_lst.append(name)
    log_lst.append(description)
    log_lst.append(permission)

    return log_lst


def parse(log_dat):
    """
        基础部分解析
    """
    result = dict()

    item_lst = log_dat.split('$$')

    result['log_time'] = datetime.datetime.strptime(item_lst[0], '%Y-%m-%d %H:%M:%S')
    result['gm_uid'] = item_lst[1]
    result['account'] = item_lst[2]
    result['gm_name'] = item_lst[3].decode(encoding='utf8')
    result['description'] = item_lst[4].decode(encoding='utf8')
    result['permission'] = item_lst[5]

    return result, item_lst[6:]


def get_val(log_part_lst, index, default='', split=False):
    if index < len(log_part_lst) and log_part_lst[index] != '':
        val = log_part_lst[index]
    else:
        val = default

    if split and val:
        val = val.split(',')
    return val