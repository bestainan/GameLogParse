# -*- coding:utf-8 -*-
"""
    商城
"""

from action import action_base
from util import game_define


def log(user, cost_stone, cost_item_list, add_item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_FRAGMENT_SHOP_BUY
    cur_stone = user.player.get_stone()
    total_cost_stone = user.player.total_cost_stone

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(cost_stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(cost_item_list))
    log_lst.append(str(add_item_str))
    log_lst.append(str(total_cost_stone))
    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['cost_stone'] = int(log_part_lst[1])
    result['cur_stone'] = int(log_part_lst[2])
    result['cost_item_list'] = action_base.get_val(log_part_lst, 3, [], True)
    result['add_item_list'] = action_base.get_val(log_part_lst, 4, [], True)
    result['total_cost_stone'] = int(log_part_lst[5])
    result['old_stone'] = result['cur_stone'] + result['cost_stone']
    return result