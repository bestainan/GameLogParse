# -*- coding:utf-8 -*-
"""
    宝物提升阶级
"""

from action import action_base
from util import game_define


def log(user, treasure_old_tid, treasure_old_phase, treasure_new_phase, need_treasure_material_num, need_material_str, cost_gold):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_TREASURE_PHASE_UP
    cur_gold = user.player.get_gold()
    total_cost_gold = user.player.total_cost_gold

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(treasure_old_tid))
    log_lst.append(str(treasure_old_phase))
    log_lst.append(str(treasure_new_phase))
    log_lst.append(str(need_treasure_material_num))
    log_lst.append(str(need_material_str))
    log_lst.append(str(cost_gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(total_cost_gold))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    # print(log_part_lst)
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['treasure_id'] = int(log_part_lst[1])
    result['treasure_old_phase'] = int(log_part_lst[2])
    result['treasure_new_phase'] = int(log_part_lst[3])
    result['treasure_need_material_num'] = int(log_part_lst[4])
    result['treasure_phase_up_material'] = action_base.get_val(log_part_lst, 5, [], True)
    result['cost_gold'] = int(log_part_lst[6])
    result['cur_gold'] = int(log_part_lst[7])
    result['total_cost_gold'] = int(log_part_lst[8])
    result['old_gold'] = result['cur_gold'] + result['cost_gold']
    return result