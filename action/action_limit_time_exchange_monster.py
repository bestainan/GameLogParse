# -*- coding:utf-8 -*-
"""
    限时兑换
"""

from action import action_base
from util import game_define


def log(user, cost_consumption_point, cur_consumption_point, monster_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_SHOP_EXCHANGE

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(cost_consumption_point))
    log_lst.append(str(cur_consumption_point))
    log_lst.append(str(monster_str))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['cost_consumption_point'] = float(log_part_lst[1])
    result['cur_consumption_point'] = float(log_part_lst[2])
    result['add_monster_list'] = action_base.get_val(log_part_lst, 3, [], True)
    result['old_consumption_point'] = result['cur_consumption_point'] + result['cost_consumption_point']
    return result