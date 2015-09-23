# -*- coding:utf-8 -*-
"""
    金币副本战斗胜利
"""

from action import action_base
from util import game_define


def log(user, stage_index, add_exp, add_gold, monster_str, equip_str, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_STAGE_GOLD_WIN
    cur_exp = user.player.exp
    cur_gold = user.player.get_gold()
    total_challenge_count = user.player.stage_gold_total_count

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(stage_index))
    log_lst.append(str(add_exp))
    log_lst.append(str(cur_exp))
    log_lst.append(str(add_gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(monster_str))
    log_lst.append(str(equip_str))
    log_lst.append(str(item_str))
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
    result['add_exp'] = int(log_part_lst[2])
    result['cur_exp'] = int(log_part_lst[3])
    result['add_gold'] = int(log_part_lst[4])
    result['cur_gold'] = int(log_part_lst[5])
    result['add_monster_list'] = action_base.get_val(log_part_lst, 6, [], True)
    result['add_equip_list'] = action_base.get_val(log_part_lst, 7, [], True)
    result['add_item_list'] = action_base.get_val(log_part_lst, 8, [], True)
    result['total_challenge_count'] = int(log_part_lst[9])
    result['old_exp'] = result['cur_exp'] - result['add_exp']
    result['old_gold'] = result['cur_gold'] - result['add_gold']
    return result