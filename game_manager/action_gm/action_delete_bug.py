# -*- coding:utf-8 -*-
"""
    删除玩家提的bug
"""
from game_manager.action_gm import action_base_gm
from util import game_define


def log(manager, del_bug):
    """
        输出日志
    """
    action = game_define.GM_ACTION_DELETE_BUG
    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(del_bug))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['bug'] = log_part_lst[1]

    return result
