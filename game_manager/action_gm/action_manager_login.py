# -*- coding:utf-8 -*-
"""
    游戏管理员登陆
"""
import datetime

from game_manager.action_gm import action_base_gm
from util import game_define


def log(gm):
    """
        输出日志
    """
    action = game_define.GM_ACTION_MANAGER_LOGIN
    last_login_ip = str(gm.last_login_ip)
    last_login_time = str(gm.last_login_time)

    log_lst = action_base_gm.log_base(gm)

    log_lst.append(str(action))
    log_lst.append(str(last_login_ip))
    log_lst.append(str(last_login_time))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['last_login_ip'] = log_part_lst[1]
    result['last_login_time'] = log_part_lst[2]

    return result