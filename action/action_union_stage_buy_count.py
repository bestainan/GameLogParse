# -*- coding:utf-8 -*-
"""
    联盟 玩家购买联盟战斗次数
"""

from action import action_base
from util import game_define


def log(user, union_uid, cost_stone):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_UNION_STAGE_BUY_COUNT
    cur_stone = user.player.get_stone()
    total_cost_stone = user.player.total_cost_stone

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(union_uid))
    log_lst.append(str(cost_stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(total_cost_stone))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['union_uid'] = int(log_part_lst[1])
    result['cost_stone'] = int(log_part_lst[2])
    result['cur_stone'] = int(log_part_lst[3])
    result['total_cost_stone'] = int(action_base.get_val(log_part_lst, 4, 0, False))
    result['old_stone'] = result['cur_stone'] + result['cost_stone']

    return result