# -*- coding:utf-8 -*-
"""
    好友 给好友发私信
"""

from action import action_base
from util import game_define


def log(user, buddy_uid, content):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_BUDDY_SEND_MAIL

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(buddy_uid))
    log_lst.append(str(content))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['buddy_uid'] = int(log_part_lst[1])
    result['buddy_content'] = log_part_lst[2].decode('utf8')

    return result