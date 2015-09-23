# -*- coding:utf-8 -*-

"""
    时间基类
"""
import time
import datetime
# from apps.platform.platform import conf


# def log_base(user):
#     """
#         日志基础
#     """
#     log_time = str(time.strftime("%Y-%m-%d %H:%M:%S"))
#     server_id = str(conf['server_id'])
#     platform_id = str(user.platform_id)
#     uid = str(user.uid)
#     level = str(user.player.level)
#     vip_level = str(user.player.vip_level)
#     install = str(user.add_time.date())
#
#     log_lst = []
#     log_lst.append(log_time)
#     log_lst.append(server_id)
#     log_lst.append(platform_id)
#     log_lst.append(uid)
#     log_lst.append(level)
#     log_lst.append(vip_level)
#     log_lst.append(install)
#
#     return log_lst


def parse(log_dat):
    """
        基础部分解析
    """
    result = dict()

    item_lst = log_dat.split('$$')

    try:
        result['log_time'] = datetime.datetime.strptime(item_lst[0], '%Y-%m-%d %H:%M:%S')
        result['server_id'] = int(item_lst[1])
        result['platform_id'] = int(item_lst[2])
        result['uid'] = int(item_lst[3])
        result['level'] = int(item_lst[4])
        result['vip_level'] = int(item_lst[5])
        result['install'] = datetime.datetime.strptime(item_lst[6], '%Y-%m-%d').date()
    except:
        print("基础部分出错日志行:"+str(log_dat))

    return result, item_lst[7:]


def list_parse(log_part_lst):
    if log_part_lst:
        return map(int, log_part_lst.split(','))
    else:
        return []


def get_val(log_part_lst, index, default='', split=False):
    if index < len(log_part_lst) and log_part_lst[index] != '':
        val = log_part_lst[index]
    else:
        val = default

    if split and val:
        val = val.split(',')
    return val