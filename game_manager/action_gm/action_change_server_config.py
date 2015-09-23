# -*- coding:utf-8 -*-
"""
    修改游戏配置信息
"""
from game_manager.action_gm import action_base_gm
from util import game_define


def log(manager, need_update_config_dict):
    """
        输出日志
    """
    action = game_define.GM_ACTION_CHANGE_SERVER_CONFIG
    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(need_update_config_dict))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['config'] = log_part_lst[1]

    return result
