# -*- coding:utf-8 -*-
"""
    人物升级
"""

from action import action_base
from util import game_define


def log(user, former_level, former_exp, later_level, later_exp):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_ROLE_LEVEL_UP

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(former_level))
    log_lst.append(str(former_exp))
    log_lst.append(str(later_level))
    log_lst.append(str(later_exp))
    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['former_level'] = int(log_part_lst[1])
    result['former_exp'] = int(log_part_lst[2])
    result['later_level'] = int(log_part_lst[3])
    result['later_exp'] = int(log_part_lst[4])
    return result