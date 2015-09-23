# -*- coding:utf-8 -*-
"""
    宝藏 历史好友最高数
"""

from action import action_base
from util import game_define


def log(user, gold, stone, free, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_HISTORY_BUDDY_MAX_REWARD
    cur_gold = user.player.get_gold()
    cur_stone = user.player.get_stone()
    cur_free = user.player.get_free_draw_material()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(free))
    log_lst.append(str(cur_free))
    log_lst.append(str(item_str))

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
    result['add_stone'] = int(log_part_lst[3])
    result['cur_stone'] = int(log_part_lst[4])
    result['add_free_draw'] = int(log_part_lst[5])
    result['cur_free_draw'] = int(log_part_lst[6])
    result['add_item_list'] = action_base.list_parse(log_part_lst[7])
    result['old_gold'] = result['cur_gold'] - result['add_gold']
    result['old_stone'] = result['cur_stone'] - result['add_stone']
    return result