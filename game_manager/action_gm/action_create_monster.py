# -*- coding:utf-8 -*-
"""
    添加宠物
"""
from game_manager.action_gm import action_base_gm
from util import game_define


def log(manager, server_id, user_id, monster_uid, monster_tid, star_level, level):
    """
        输出日志
    """
    action = game_define.GM_ACTION_CREATE_MONSTER

    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(server_id))
    log_lst.append(str(user_id))
    log_lst.append(str(monster_uid))
    log_lst.append(str(monster_tid))
    log_lst.append(str(star_level))
    log_lst.append(str(level))

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
    result['mon_uid'] = log_part_lst[3]
    result['mon_tid'] = log_part_lst[4]
    result['star_level'] = log_part_lst[5]
    result['mon_level'] = log_part_lst[6]

    return result