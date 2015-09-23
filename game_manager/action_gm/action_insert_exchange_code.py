# -*- coding:utf-8 -*-
"""
    插入兑换码
"""
from game_manager.action_gm import action_base_gm
from util import game_define


def log(manager, gift_id, num):
    """
        输出日志
    """
    action = game_define.GM_ACTION_INSERT_EXCHANGE_CODE
    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(gift_id))
    log_lst.append(str(num))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['gift_id'] = log_part_lst[1]
    result['num'] = log_part_lst[2]

    return result
