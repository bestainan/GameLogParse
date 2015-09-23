# -*- coding:utf-8 -*-
"""
    联盟 玩家获取联盟通关点数奖励
"""

from action import action_base
from util import game_define


def log(user, union_uid, add_union_point, cur_union_point):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_UNION_PASS_STAGE_REWARD_POINT

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(union_uid))
    log_lst.append(str(add_union_point))
    log_lst.append(str(cur_union_point))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['union_uid'] = int(log_part_lst[1])
    result['add_union_point'] = int(log_part_lst[2])
    result['cur_union_point'] = int(log_part_lst[3])

    return result