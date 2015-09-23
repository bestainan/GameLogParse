# -*- coding:utf-8 -*-
"""
    试炼失败
"""

from action import action_base
from util import game_define


def log(user, cost_stamina):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_TRIAL_BATTLE_FAIL

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(cost_stamina))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['cost_stamina'] = int(log_part_lst[1])
    return result