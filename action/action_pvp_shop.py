# -*- coding:utf-8 -*-
"""
    商城
"""

from action import action_base
from util import game_define


def log(user, cost_arena_emblem, cur_arena_emblem, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_PVP_SHOP_BUY

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(cost_arena_emblem))
    log_lst.append(str(cur_arena_emblem))
    log_lst.append(str(item_str))
    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['cost_arena_emblem'] = int(log_part_lst[1])
    result['cur_arena_emblem'] = int(log_part_lst[2])
    result['add_item_list'] = action_base.get_val(log_part_lst, 3, [], True)
    result['old_arena_emblem'] = result['cur_arena_emblem'] + result['cost_arena_emblem']
    return result