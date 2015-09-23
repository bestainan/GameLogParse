# -*- coding:utf-8 -*-
"""
    修改管理员信息
"""
import datetime

from game_manager.action_gm import action_base_gm
from util import game_define


def log(gm, new_account, new_name, new_permission_name, new_description):
    """
        输出日志
    """
    action = game_define.GM_ACTION_UPDATE_MANAGER_INFO

    log_lst = action_base_gm.log_base(gm)

    log_lst.append(str(action))
    log_lst.append(str(new_account))
    log_lst.append(new_name.encode(encoding='utf8'))
    log_lst.append(str(new_permission_name))
    log_lst.append(new_description.encode(encoding='utf8'))

    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['new_account'] = log_part_lst[1]
    result['new_name'] = log_part_lst[2].decode(encoding='utf8')
    result['new_permission'] = log_part_lst[3]
    result['new_description'] = log_part_lst[4].decode(encoding='utf8')

    return result