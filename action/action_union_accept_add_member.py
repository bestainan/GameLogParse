# -*- coding:utf-8 -*-
"""
    联盟 同意添加联盟成员
    联盟uid　　联盟当前人数　添加的玩家uid
"""

from action import action_base
from util import game_define


def log(user, union_uid, cur_num, user_uid, union_level):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_UNION_ACCEPT_ADD_MEMBER

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(union_uid))
    log_lst.append(str(cur_num))
    log_lst.append(str(user_uid))
    log_lst.append(str(union_level))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['union_uid'] = int(log_part_lst[1])
    result['union_cur_number'] = int(log_part_lst[2])
    result['union_new_member'] = int(log_part_lst[3])
    result['union_level'] = int(log_part_lst[4])
    return result