# -*- coding:utf-8 -*-
"""
    好友 与好友通讯进度奖励
"""

from action import action_base
from util import game_define


def log(user, add_free_draw, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_REWARD_BUDDY_CONTACT
    cur_free_draw = user.player.get_free_draw_material()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(add_free_draw))
    log_lst.append(str(cur_free_draw))
    log_lst.append(str(item_str))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['add_free_draw'] = int(log_part_lst[1])
    result['cur_free_draw'] = int(log_part_lst[2])
    result['add_item_list'] = action_base.list_parse(log_part_lst[3])
    result['old_free_draw'] = result['cur_free_draw'] - result['add_free_draw']

    return result