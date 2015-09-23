# -*- coding:utf-8 -*-
"""
    好友 与好友通讯
"""

from action import action_base
from util import game_define


def log(user, buddy_uid, add_stone, add_today_num, today_num, cost_contact_num, contact_num, add_progress, progress):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_BUDDY_CONTACT
    cur_stone = user.player.get_stone()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(buddy_uid))
    log_lst.append(str(add_stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(add_today_num))
    log_lst.append(str(today_num))
    log_lst.append(str(cost_contact_num))
    log_lst.append(str(contact_num))
    log_lst.append(str(add_progress))
    log_lst.append(str(progress))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['buddy_uid'] = int(log_part_lst[1])
    result['add_stone'] = int(log_part_lst[2])
    result['cur_stone'] = int(log_part_lst[3])
    result['add_today_num'] = int(log_part_lst[4])
    result['today_contact_num'] = int(log_part_lst[5])
    result['cost_contact_num'] = int(log_part_lst[6])
    result['left_contact_num'] = int(log_part_lst[7])
    result['add_progress'] = int(log_part_lst[8])
    result['buddy_contact_progress'] = int(log_part_lst[9])
    result['old_stone'] = result['cur_stone'] - result['add_stone']

    return result