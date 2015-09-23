# -*- coding:utf-8 -*-
"""
    联盟 玩家联盟签到
"""

from action import action_base
from util import game_define


def log(user, union_uid, union_sign_type, cost_gold, cost_stone, add_progress, cur_progress, add_union_exp, cur_union_exp, add_point, cur_point, union_level):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_UNION_SIGN
    cur_gold = user.player.get_gold()
    cur_stone = user.player.get_stone()
    total_cost_gold = user.player.total_cost_gold
    total_cost_stone = user.player.total_cost_stone

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(union_uid))
    log_lst.append(str(union_sign_type))
    log_lst.append(str(cost_gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(cost_stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(add_progress))
    log_lst.append(str(cur_progress))
    log_lst.append(str(add_union_exp))
    log_lst.append(str(cur_union_exp))
    log_lst.append(str(add_point))
    log_lst.append(str(cur_point))
    log_lst.append(str(union_level))
    log_lst.append(str(total_cost_gold))
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
    result['union_sign_type'] = int(log_part_lst[2])
    result['cost_gold'] = int(log_part_lst[3])
    result['cur_gold'] = int(log_part_lst[4])
    result['cost_stone'] = int(log_part_lst[5])
    result['cur_stone'] = int(log_part_lst[6])
    result['union_add_progress'] = int(log_part_lst[7])
    result['union_cur_progress'] = int(log_part_lst[8])
    result['union_add_exp'] = int(log_part_lst[9])
    result['union_cur_exp'] = int(log_part_lst[10])
    result['add_union_point'] = int(log_part_lst[11])
    result['cur_union_point'] = int(log_part_lst[12])
    result['union_level'] = int(log_part_lst[13])
    result['total_cost_gold'] = int(action_base.get_val(log_part_lst, 14, 0, False))
    result['total_cost_stone'] = int(action_base.get_val(log_part_lst, 15, 0, False))

    return result