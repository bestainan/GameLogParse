# -*- coding:utf-8 -*-
"""
    夺宝战斗失败
"""

from action import action_base
from util import game_define


def log(user):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_TREASURE_BATTLE_FAIL

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    return result