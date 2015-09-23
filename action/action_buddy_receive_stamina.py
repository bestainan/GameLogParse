# -*- coding:utf-8 -*-
"""
    领取好友赠送体力
"""

from action import action_base
from util import game_define


def log(user, buddy_uid, stamina):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_BUDDY_RECEIVE_STAMINA
    cur_stamina = user.player.get_stamina()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(buddy_uid))
    log_lst.append(str(stamina))
    log_lst.append(str(cur_stamina))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['buddy_uid'] = int(log_part_lst[1])
    result['add_stamina'] = int(log_part_lst[2])
    result['cur_stamina'] = int(log_part_lst[3])
    result['old_stamina'] = result['cur_stamina'] - result['add_stamina']

    return result