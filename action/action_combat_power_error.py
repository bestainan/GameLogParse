# -*- coding:utf-8 -*-
"""
    竞技场参与
"""

from action import action_base
from util import game_define


def log(user, server_combat_power, cur_client_combat_power,reason_id):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_COMBAT_POWER_ERROR

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(server_combat_power))
    log_lst.append(str(cur_client_combat_power))
    log_lst.append(str(reason_id))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['server_combat_power'] = log_part_lst[1]
    result['client_combat_power'] = int(log_part_lst[2])

    return result