# -*- coding:utf-8 -*-
"""
    竞技场参与
"""

from action import action_base
from util import game_define


def log(user, add_arena_emblem, cur_arena_emblem):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_ARENA_FAIL

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(add_arena_emblem))
    log_lst.append(str(cur_arena_emblem))


    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['add_arena_emblem'] = int(log_part_lst[1])
    result['cur_arena_emblem'] = int(log_part_lst[2])
    result['old_arena_emblem'] = result['cur_arena_emblem'] - result['add_arena_emblem']

    return result