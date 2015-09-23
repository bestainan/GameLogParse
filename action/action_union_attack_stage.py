# -*- coding:utf-8 -*-
"""
    联盟 玩家攻击联盟关卡
"""

from action import action_base
from util import game_define


def log(user, union_uid, stage_id, add_stone, add_union_point, cur_union_point, add_exp, cur_exp, level, stage_cur_hp, damage, small_hp):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_UNION_ATTACK_STAGE
    cur_stone = user.player.get_stone()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(union_uid))
    log_lst.append(str(stage_id))
    log_lst.append(str(add_stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(add_union_point))
    log_lst.append(str(cur_union_point))
    log_lst.append(str(add_exp))
    log_lst.append(str(cur_exp))
    log_lst.append(str(level))
    log_lst.append(str(stage_cur_hp))
    log_lst.append(str(damage))
    log_lst.append(str(small_hp))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['union_uid'] = int(log_part_lst[1])
    result['stage_index'] = int(log_part_lst[2])
    result['add_stone'] = int(log_part_lst[3])
    result['cur_stone'] = int(log_part_lst[4])
    result['add_union_point'] = int(log_part_lst[5])
    result['cur_union_point'] = int(log_part_lst[6])
    result['union_add_exp'] = int(log_part_lst[7])
    result['union_cur_exp'] = int(log_part_lst[8])
    result['union_level'] = int(log_part_lst[9])
    result['union_all_hp'] = int(log_part_lst[10])
    result['union_damage'] = int(log_part_lst[11])
    result['union_stage_hp'] = int(log_part_lst[12])

    return result