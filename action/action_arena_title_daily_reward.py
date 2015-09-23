# -*- coding:utf-8 -*-
"""
    领取每日爵位奖励
"""

from action import action_base
from util import game_define


def log(user, add_gold, add_arena_emblem, cur_arena_emblem):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_ARENA_DAILY_REWARD
    cur_gold = user.player.get_gold()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(add_gold))
    log_lst.append(str(cur_gold))
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
    result['add_gold'] = int(log_part_lst[1])
    result['cur_gold'] = int(log_part_lst[2])
    result['add_arena_emblem'] = int(log_part_lst[3])
    result['cur_arena_emblem'] = int(log_part_lst[4])
    result['old_arena_emblem'] = result['cur_arena_emblem'] - result['add_arena_emblem']
    return result