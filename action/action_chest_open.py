# -*- coding:utf-8 -*-
"""
    开启宝箱
"""

from action import action_base
from util import game_define


def log(user, cost_item_str, add_item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_CHEST_OPEN

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(cost_item_str))
    log_lst.append(str(add_item_str))

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