# -*- coding:utf-8 -*-
"""
    物品售出
"""

from action import action_base
from util import game_define


def log(user, add_gold, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_SELL_ITEM
    cur_gold = user.player.get_gold()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(add_gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(item_str))

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
    result['cost_item_list'] = action_base.get_val(log_part_lst, 3, [], True)
    result['old_gold'] = result['cur_gold'] - result['add_gold']
    return result