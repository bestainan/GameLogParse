# -*- coding:utf-8 -*-
"""
    添加服务器
"""
from game_manager.action_gm import action_base_gm
from util import game_define
import datetime


def log(manager, server_id, url, name, server_state, server_hidden, version, open_server_time):
    """
        输出日志
    """
    action = game_define.GM_ACTION_INSERT_SERVER
    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(server_id))
    log_lst.append(str(url))
    log_lst.append(str(name))
    log_lst.append(str(server_state))
    log_lst.append(str(server_hidden))
    log_lst.append(str(version))
    log_lst.append(str(open_server_time.strftime("%Y-%m-%d")))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['server_id'] = log_part_lst[1]
    result['url'] = log_part_lst[2]
    result['name'] = log_part_lst[3].decode('utf-8')
    result['state'] = log_part_lst[4]
    result['hidden'] = log_part_lst[5]
    result['version'] = log_part_lst[6]
    result['open_time'] = log_part_lst[7]

    return result
