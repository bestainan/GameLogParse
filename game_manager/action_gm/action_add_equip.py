# -*- coding:utf-8 -*-
"""
    添加装备
"""
from game_manager.action_gm import action_base_gm
from util import game_define


def log(manager, server_id, user_id, equip_uid, equip_tid, equip_level):
    """
        输出日志
    """
    action = game_define.GM_ACTION_ADD_EQUIP

    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(server_id))
    log_lst.append(str(user_id))
    log_lst.append(str(equip_uid))
    log_lst.append(str(equip_tid))
    log_lst.append(str(equip_level))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['server_id'] = log_part_lst[1]
    result['user_id'] = log_part_lst[2]
    result['uid'] = log_part_lst[3]
    result['tid'] = log_part_lst[4]
    result['level'] = log_part_lst[5]

    return result
