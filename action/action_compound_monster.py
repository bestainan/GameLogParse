# -*- coding:utf-8 -*-
"""
    怪碎片合成
"""

from action import action_base
from util import game_define


def log(user, cost_item_str, monster_str, cost_universal_fragment):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_COMPOUND_MONSTER
    cur_universal_fragment = user.player.universal_fragment

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(cost_item_str))
    log_lst.append(str(monster_str))
    log_lst.append(str(cost_universal_fragment))
    log_lst.append(str(cur_universal_fragment))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['cost_item_list'] = action_base.get_val(log_part_lst, 1, [], True)
    result['add_monster_list'] = action_base.get_val(log_part_lst, 2, [], True)
    result['cost_universal_fragment'] = int(log_part_lst[3])
    result['cur_universal_fragment'] = int(log_part_lst[4])
    result['old_universal_fragment'] = result['cur_universal_fragment'] + result['cost_universal_fragment']
    return result