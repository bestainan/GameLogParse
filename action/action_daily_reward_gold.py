# -*- coding:utf-8 -*-
"""
    每日领取金币
"""

from action import action_base
from util import game_define


def log(user, add_gold):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_DAILY_REWARD_GOLD
    cur_gold = user.player.get_gold()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(add_gold))
    log_lst.append(str(cur_gold))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['add_gold'] = int(log_part_lst[1])
    result['cur_gold'] = int(log_part_lst[2])
    result['old_gold'] = result['cur_gold'] - result['add_gold']
    return result