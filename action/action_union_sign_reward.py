# -*- coding:utf-8 -*-
"""
    联盟 玩家获取联盟签到奖励
"""

from action import action_base
from util import game_define


def log(user, union_uid, add_union_point, cur_union_point, add_gold, add_stone, item_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_UNION_SIGN_REWARD
    cur_gold = user.player.get_gold()
    cur_stone = user.player.get_stone()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(union_uid))
    log_lst.append(str(add_union_point))
    log_lst.append(str(cur_union_point))
    log_lst.append(str(add_gold))
    log_lst.append(str(cur_gold))
    log_lst.append(str(add_stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(item_str))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['union_uid'] = int(log_part_lst[1])
    result['add_union_point'] = int(log_part_lst[2])
    result['cur_union_point'] = int(log_part_lst[3])
    result['add_gold'] = int(log_part_lst[4])
    result['cur_gold'] = int(log_part_lst[5])
    result['add_stone'] = int(log_part_lst[6])
    result['cur_stone'] = int(log_part_lst[7])
    result['add_item_list'] = action_base.list_parse(log_part_lst[8])

    return result