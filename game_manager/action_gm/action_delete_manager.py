# -*- coding:utf-8 -*-
"""
    删除一个管理员
"""
import datetime

from game_manager.action_gm import action_base_gm
from util import game_define


def log(gm, del_id):
    """
        输出日志
    """
    action = game_define.GM_ACTION_DELETE_MANAGER

    log_lst = action_base_gm.log_base(gm)

    log_lst.append(str(action))
    log_lst.append(str(del_id))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['del_gm'] = int(log_part_lst[1])

    return result