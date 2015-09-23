# -*- coding:utf-8 -*-
"""
    外部充值
"""
import datetime

from action import action_base
from util import game_define


def log(user, order_id, add_stone, shop_index, shop_event, old_rmb, add_rmb, platform_type):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_RECHARGE_PLAYER
    cur_stone = user.player.get_stone()

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(str(order_id))
    log_lst.append(str(add_stone))
    log_lst.append(str(cur_stone))
    log_lst.append(str(shop_index))
    log_lst.append(str(int(shop_event)))
    log_lst.append(str(old_rmb))
    log_lst.append(str(add_rmb))
    log_lst.append(str(platform_type))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['order_id'] = log_part_lst[1]
    result['add_stone'] = int(log_part_lst[2])
    result['cur_stone'] = int(log_part_lst[3])
    result['shop_index'] = int(log_part_lst[4])
    result['shop_event'] = int(log_part_lst[5])
    result['old_rmb'] = int(log_part_lst[6])
    result['add_rmb'] = int(log_part_lst[7])
    result['platform_type'] = log_part_lst[8]
    result['old_stone'] = result['cur_stone'] - result['add_stone']
    result['cur_rmb'] = result['old_rmb'] + result['add_rmb']
    return result