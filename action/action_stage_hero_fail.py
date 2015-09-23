# -*- coding:utf-8 -*-
"""
    困难副本战斗失败
"""

from action import action_base
from util import game_define


def log(user, stageIndex):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_STAGE_HERO_FAIL

    log_lst = action_base.log_base(user)
    total_challenge_count = user.player.stage_hero_total_count

    log_lst.append(str(action))
    log_lst.append(str(stageIndex))
    log_lst.append(str(total_challenge_count))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['stage_index'] = log_part_lst[1]
    result['total_challenge_count'] = log_part_lst[2]
    return result