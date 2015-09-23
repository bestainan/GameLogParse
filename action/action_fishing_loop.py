# -*- coding:utf-8 -*-
"""
    全部钓鱼
"""

from action import action_base
from util import game_define


def log(user, exp, gold, stone, item_str, cost_fishing_count):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_FISHING_LOOP
    cur_exp = user.player.exp
    cur_gold = user.player.gold
    cur_stone = user.player.stone

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(exp))
    log_lst.append(str(cur_exp))
    log_lst.append(str(gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(item_str))
    log_lst.append(str(cost_fishing_count))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['add_exp'] = int(log_part_lst[1])
    result['cur_exp'] = int(log_part_lst[2])
    result['add_gold'] = int(log_part_lst[3])
    result['cur_gold'] = int(log_part_lst[4])
    result['add_stone'] = int(log_part_lst[5])
    result['cur_stone'] = int(log_part_lst[6])
    result['add_item_list'] = action_base.get_val(log_part_lst, 7, [], True)
    result['cost_fishing_count'] = int(action_base.get_val(log_part_lst, 8, 0, False))
    result['old_exp'] = result['cur_exp'] - result['add_exp']
    result['old_gold'] = result['cur_gold'] - result['add_gold']
    result['old_stone'] = result['cur_stone'] - result['add_stone']
    return result