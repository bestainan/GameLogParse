# -*- coding:utf-8 -*-
"""
    联盟 领取联盟奖励
"""

from action import action_base
from util import game_define


def log(user, union_uid, union_name, union_level, cost_union_point, cur_union_point, add_gold, add_stone, add_free_draw, item_str, equip_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_UNION_BUY_REWARD
    cur_gold = user.player.get_gold()
    cur_stone = user.player.get_stone()
    cur_free_draw = user.player.get_free_draw_material()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(union_uid))
    log_lst.append(str(union_name))
    log_lst.append(str(union_level))
    log_lst.append(str(cost_union_point))
    log_lst.append(str(cur_union_point))
    log_lst.append(str(add_gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(add_stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(add_free_draw))
    log_lst.append(str(cur_free_draw))
    log_lst.append(str(item_str))
    log_lst.append(str(equip_str))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['union_uid'] = int(log_part_lst[1])
    result['union_name'] = log_part_lst[2].decode('utf-8')
    result['union_level'] = int(log_part_lst[3])
    result['cost_union_point'] = int(log_part_lst[4])
    result['cur_union_point'] = int(log_part_lst[5])
    result['add_gold'] = int(log_part_lst[6])
    result['cur_gold'] = int(log_part_lst[7])
    result['add_stone'] = int(log_part_lst[8])
    result['cur_stone'] = int(log_part_lst[9])
    result['add_free_draw'] = int(log_part_lst[10])
    result['cur_free_draw'] = int(log_part_lst[11])
    result['add_item_list'] = action_base.list_parse(log_part_lst[12])
    result['add_equip_list'] = action_base.list_parse(log_part_lst[13])

    return result