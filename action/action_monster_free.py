# -*- coding:utf-8 -*-
"""
    宠物放生
"""

from action import action_base
from util import game_define


def log(user, remove_mon_str, add_item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_MONSTER_FREE

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(remove_mon_str))
    log_lst.append(str(add_item_str))

    log_str = '$$'.join(log_lst)
    # print("free monster:")
    # print(log_str)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['remove_monster_list'] = action_base.get_val(log_part_lst, 1, [], True)
    result['add_item_list'] = action_base.get_val(log_part_lst, 2, [], True)
    return result