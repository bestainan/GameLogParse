# -*- coding:utf-8 -*-
"""
    抽奖
"""

from action import action_base
from util import game_define


def log(user, monster_str, equip_str, item_str, cost_stone, cost_free_draw):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_ONE_DRAW
    cur_stone = user.player.get_stone()
    cur_free_draw = user.player.get_free_draw_material()
    total_cost_stone = user.player.total_cost_stone

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(monster_str))
    log_lst.append(str(equip_str))
    log_lst.append(str(item_str))
    log_lst.append(str(cost_stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(cost_free_draw))
    log_lst.append(str(cur_free_draw))
    log_lst.append(str(total_cost_stone))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['add_monster_list'] = action_base.get_val(log_part_lst, 1, [], True)
    result['add_equip_list'] = action_base.get_val(log_part_lst, 2, [], True)
    result['add_item_list'] = action_base.get_val(log_part_lst, 3, [], True)
    result['cost_stone'] = int(log_part_lst[4])
    result['cur_stone'] = int(log_part_lst[5])
    result['cost_free_draw'] = int(log_part_lst[6])
    result['cur_free_draw'] = int(log_part_lst[7])
    result['total_cost_stone'] = int(log_part_lst[8])
    result['old_stone'] = result['cur_stone'] + result['cost_stone']
    result['old_free_draw'] = result['cur_free_draw'] + result['cost_free_draw']
    return result