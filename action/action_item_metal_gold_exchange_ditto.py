# -*- coding:utf-8 -*-
"""
    金色精华兑换百变怪
"""

from action import action_base
from util import game_define


def log(user, cost_metal_gold_str, add_ditto_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_EXCHANGE_MONSTER

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(cost_metal_gold_str))
    log_lst.append(str(add_ditto_str))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['cost_item_list'] = action_base.get_val(log_part_lst, 1, [], True)
    result['add_item_list'] = action_base.get_val(log_part_lst, 2, [], True)
    return result

