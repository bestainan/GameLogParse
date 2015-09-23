# -*- coding:utf-8 -*-
"""
    每日累计签到奖励
"""

from action import action_base
from util import game_define


def log(user, monster_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_LOGIN_SERIES_REWARD

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(monster_str))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['add_monster_list'] = action_base.get_val(log_part_lst, 1, [], True)

    return result