# -*- coding:utf-8 -*-
"""
    联盟 解散联盟
"""

from action import action_base
from util import game_define


def log(user, union_uid, union_name):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_UNION_DISMISS

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(union_uid))
    log_lst.append(str(union_name))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['union_uid'] = int(log_part_lst[1])
    result['union_name'] = log_part_lst[2].decode('utf-8')

    return result