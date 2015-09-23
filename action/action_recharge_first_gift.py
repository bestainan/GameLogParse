# -*- coding:utf-8 -*-
"""
    获取首次充值礼包
"""

from action import action_base
from util import game_define


def log(user, monster_str, equip_str, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_GET_FIRST_RECHARGE_GIFT

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(monster_str))
    log_lst.append(str(equip_str))
    log_lst.append(str(item_str))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['add_monster_list'] = action_base.get_val(log_part_lst, 1, [], True)
    result['add_equip_list'] = action_base.get_val(log_part_lst, 2, [], True)
    result['add_item_list'] = action_base.get_val(log_part_lst, 3, [], True)
    return result