# -*- coding:utf-8 -*-
"""
    联盟商城购买
"""

from action import action_base
from util import game_define


def log(user, cost_union_point, cur_union_point, add_item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_UNION_SHOP_BUY

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(cost_union_point))
    log_lst.append(str(cur_union_point))
    log_lst.append(str(add_item_str))
    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['cost_union_point'] = int(log_part_lst[1])
    result['cur_union_point'] = int(log_part_lst[2])
    result['add_item_list'] = action_base.list_parse(log_part_lst[3])
    result['old_union_point'] = result['cur_union_point'] + result['cost_union_point']
    return result